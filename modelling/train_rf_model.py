#!/usr/bin/env python3
"""
Random Forest Classifier Training Script
Author: Machine Learning Team - Magang PSI STT Wastukancana
Date: December 2025
Description: This script trains a Random Forest classifier for welfare prediction
             with comprehensive analysis and visualization capabilities for Streamlit app
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import plot_tree
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('default')
sns.set_palette("husl")

class RandomForestAnalyzer:
    """
    Comprehensive Random Forest Analyzer with visualization capabilities
    """
    
    def __init__(self, data_path, model_save_path, metrics_save_path, img_dir):
        """
        Initialize the analyzer
        
        Args:
            data_path (str): Path to the preprocessed dataset
            model_save_path (str): Where to save the model
            metrics_save_path (str): Where to save evaluation metrics
            img_dir (str): Directory to save visualization images
        """
        self.data_path = data_path
        self.model_save_path = model_save_path
        self.metrics_save_path = metrics_save_path
        self.img_dir = img_dir
        self.label_encoder = None
        self.scaler = None
        self.model = None
        self.mapping = {}
        
        # Create images directory if it doesn't exist
        os.makedirs(self.img_dir, exist_ok=True)
    
    def load_and_prepare_data(self):
        """
        Load and prepare the dataset for training
        """
        print("="*60)
        print("LOADING AND PREPARING DATA")
        print("="*60)
        
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset tidak ditemukan di: {self.data_path}")
        
        df = pd.read_csv(self.data_path)
        print(f"Data dimensi: {df.shape}")
        print(f"Jumlah fitur: {df.shape[1] - 1}")
        print(f"Target distribution:\n{df['kesejahteraan'].value_counts()}")
        
        # Separate features and target
        X = df.drop('kesejahteraan', axis=1)
        y_raw = df['kesejahteraan']
        
        # Encode target variable
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y_raw)
        
        # Store label mapping
        self.mapping = {int(i): label for i, label in enumerate(self.label_encoder.classes_)}
        print(f"\nLabel mapping: {self.mapping}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Train set size: {X_train.shape[0]} ({X_train.shape[0]/len(X)*100:.1f}%)")
        print(f"Test set size: {X_test.shape[0]} ({X_test.shape[0]/len(X)*100:.1f}%)")
        
        return X_train, X_test, y_train, y_test, X.columns.tolist()
    
    def train_model(self, X_train, y_train):
        """
        Train the Random Forest model with scaling
        """
        print("\n" + "="*60)
        print("TRAINING RANDOM FOREST MODEL")
        print("="*60)
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Random Forest with optimized parameters
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'  # Handle imbalanced classes
        )
        
        print("Training model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Calculate training accuracy
        train_pred = self.model.predict(X_train_scaled)
        train_acc = accuracy_score(y_train, train_pred)
        print(f"Training accuracy: {train_acc:.4f}")
        
        return X_train_scaled
    
    def evaluate_model(self, X_test, y_test, feature_names):
        """
        Evaluate the model and create visualizations
        """
        print("\n" + "="*60)
        print("EVALUATING MODEL")
        print("="*60)
        
        # Transform test data
        X_test_scaled = self.scaler.transform(X_test)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Test Accuracy: {accuracy:.4f}")
        
        if accuracy >= 0.75:
            print("✅ Akurasi model memenuhi target (> 0.75)")
        else:
            print("⚠️  Akurasi model di bawah target (< 0.75)")
            print(f"   Pertimbangkan untuk menyesuaikan parameter model")
        
        # Generate detailed classification report
        report = classification_report(
            y_test, 
            y_pred, 
            target_names=self.label_encoder.classes_,
            output_dict=True
        )
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))
        
        # Create visualizations
        self.create_visualizations(
            y_test, y_pred, feature_names, X_test_scaled
        )
        
        return {
            'accuracy': accuracy,
            'classification_report': report
        }
    
    def create_visualizations(self, y_test, y_pred, feature_names, X_test_scaled):
        """
        Create comprehensive visualizations for model evaluation
        """
        print("\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60)
        
        # 1. Confusion Matrix
        print("Creating Confusion Matrix...")
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.label_encoder.classes_,
            yticklabels=self.label_encoder.classes_
        )
        plt.title('Confusion Matrix - Random Forest Classifier', fontsize=16, pad=20)
        plt.ylabel('Actual Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        cm_path = os.path.join(self.img_dir, 'confusion_matrix.png')
        plt.savefig(cm_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved to: {cm_path}")
        
        # 2. Feature Importance
        print("Creating Feature Importance Plot...")
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(12, 8))
        plt.title('Feature Importance - Random Forest Classifier', fontsize=16, pad=20)
        bars = plt.barh(range(len(indices)), importances[indices], align="center", alpha=0.8)
        
        # Color bars differently for better aesthetics
        colors = plt.cm.viridis(np.linspace(0, 1, len(indices)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
            
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.gca().invert_yaxis()
        plt.xlabel('Importance Score', fontsize=12)
        plt.tight_layout()
        fi_path = os.path.join(self.img_dir, 'feature_importance.png')
        plt.savefig(fi_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved to: {fi_path}")
        
        # 3. Individual Tree Visualization (first tree in the forest)
        print("Creating Tree Visualization...")
        fig, ax = plt.subplots(figsize=(20, 12))
        
        # Plot the first decision tree from the forest
        plot_tree(
            self.model.estimators_[0],
            max_depth=3,  # Limit depth for readability
            feature_names=feature_names,
            class_names=self.label_encoder.classes_,
            filled=True,
            rounded=True,
            fontsize=10
        )
        plt.title('Decision Tree Visualization (First Tree)', fontsize=16, pad=20)
        plt.tight_layout()
        tree_path = os.path.join(self.img_dir, 'decision_tree_viz.png')
        plt.savefig(tree_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved to: {tree_path}")
        
        # 4. Model Performance Summary
        print("Creating Performance Summary...")
        report = classification_report(y_test, y_pred, output_dict=True)

        # Exclude 'accuracy', 'macro avg', 'weighted avg' from class names
        classes = [cls for cls in self.label_encoder.classes_ if cls in report]
        precision_scores = [report[cls]['precision'] for cls in classes]
        recall_scores = [report[cls]['recall'] for cls in classes]
        f1_scores = [report[cls]['f1-score'] for cls in classes]

        # Create grouped bar chart
        x = np.arange(len(classes))
        width = 0.25

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.bar(x - width, precision_scores, width, label='Precision', alpha=0.8)
        ax.bar(x, recall_scores, width, label='Recall', alpha=0.8)
        ax.bar(x + width, f1_scores, width, label='F1-Score', alpha=0.8)

        ax.set_xlabel('Classes')
        ax.set_ylabel('Score')
        ax.set_title('Model Performance Metrics by Class', fontsize=16, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(classes, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        # Set y-axis limits to ensure readability
        ax.set_ylim([0, 1.1])

        plt.tight_layout()
        perf_path = os.path.join(self.img_dir, 'performance_metrics.png')
        plt.savefig(perf_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved to: {perf_path}")
    
    def save_model_and_metrics(self, metrics, feature_names):
        """
        Save the trained model and evaluation metrics
        """
        print("\n" + "="*60)
        print("SAVING MODEL AND METRICS")
        print("="*60)

        # Create artifacts dictionary
        artifacts = {
            'model': self.model,
            'scaler': self.scaler,
            'mapping': self.mapping,
            'features': feature_names
        }

        # Save model artifacts
        joblib.dump(artifacts, self.model_save_path)
        print(f"✓ Model saved to: {os.path.abspath(self.model_save_path)}")

        # Save metrics
        with open(self.metrics_save_path, 'w') as f:
            json.dump(metrics, f, indent=4)
        print(f"✓ Metrics saved to: {os.path.abspath(self.metrics_save_path)}")
    
    def run_complete_analysis(self):
        """
        Run the complete analysis pipeline
        """
        print("🚀 STARTING RANDOM FOREST ANALYSIS PIPELINE")
        print("="*60)
        
        # Step 1: Load and prepare data
        X_train, X_test, y_train, y_test, feature_names = self.load_and_prepare_data()
        
        # Step 2: Train model
        X_train_scaled = self.train_model(X_train, y_train)
        
        # Step 3: Evaluate model
        metrics = self.evaluate_model(X_test, y_test, feature_names)
        
        # Step 4: Save model and metrics
        self.save_model_and_metrics(metrics, feature_names)
        
        print("\n" + "="*60)
        print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        return {
            'model': self.model,
            'scaler': self.scaler,
            'mapping': self.mapping,
            'accuracy': metrics['accuracy'],
            'feature_names': feature_names
        }


def main():
    """
    Main execution function
    """
    # Configuration
    DATA_PATH = '../preprocessing/dataset_preprocessed.csv'
    MODEL_PATH = 'rf_model_kesejahteraan.pkl'
    METRICS_PATH = 'metrics.json'
    IMG_DIR = '.'
    
    # Create analyzer instance
    analyzer = RandomForestAnalyzer(
        data_path=DATA_PATH,
        model_save_path=MODEL_PATH,
        metrics_save_path=METRICS_PATH,
        img_dir=IMG_DIR
    )
    
    # Run complete analysis
    results = analyzer.run_complete_analysis()
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Model Accuracy: {results['accuracy']:.4f}")
    print(f"   Number of Features: {len(results['feature_names'])}")
    print(f"   Number of Classes: {len(results['mapping'])}")


if __name__ == "__main__":
    main()