"""
Script untuk menjalankan Random Forest Classifier Model
Mengikuti tahapan dari Modul Decision Tree
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import plot_tree

# Konfigurasi
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

print("="*70)
print("PREDIKSI TINGKAT KESEJAHTERAAN MENGGUNAKAN RANDOM FOREST CLASSIFIER")
print("="*70)

# 1. Load Dataset
print("\n[1] LOAD DATASET")
print("-"*70)
df = pd.read_csv("../preprocessing/dataset_preprocessed.csv")
print(f"✓ Dataset dimuat: {df.shape[0]} baris, {df.shape[1]} kolom\n")

# 2. Exploratory Data Analysis
print("[2] EXPLORATORY DATA ANALYSIS")
print("-"*70)
print("\nDistribusi Kelas Kesejahteraan:")
print(df['kesejahteraan'].value_counts())

# Visualisasi distribusi kelas
plt.figure(figsize=(10, 5))
df['kesejahteraan'].value_counts().plot(kind='bar', color='steelblue')
plt.title('Distribusi Kelas Kesejahteraan', fontsize=14, fontweight='bold')
plt.xlabel('Kategori Kesejahteraan')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('distribusi_kelas.png', dpi=300, bbox_inches='tight')
print("✓ Visualisasi distribusi kelas disimpan ke: distribusi_kelas.png")

# 3. Pemisahan Fitur dan Target
print("\n[3] PEMISAHAN FITUR DAN TARGET")
print("-"*70)
X = df[['jumlah_penduduk_miskin', 'jumlah_pengangguran_terbuka', 'pdrb_total_adhk', 'harapan_lama_sekolah']]
y = df['kesejahteraan_encoded']

print(f"Jumlah fitur: {X.shape[1]}")
print(f"Jumlah sampel: {X.shape[0]}")
print(f"Fitur: {list(X.columns)}")

# 4. Split Data
print("\n[4] SPLIT DATA (80% TRAINING, 20% TESTING)")
print("-"*70)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Data Training: {X_train.shape[0]} sampel")
print(f"Data Testing: {X_test.shape[0]} sampel")

# 5. Training Model Random Forest
print("\n[5] TRAINING MODEL RANDOM FOREST")
print("-"*70)
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

print("Training model...")
rf_model.fit(X_train, y_train)
print("✓ Training selesai!")

# 6. Evaluasi Model
print("\n[6] EVALUASI MODEL")
print("-"*70)
y_train_pred = rf_model.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)

y_test_pred = rf_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"Akurasi Training: {train_accuracy*100:.2f}%")
print(f"Akurasi Testing: {test_accuracy*100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Random Forest Classifier', fontsize=14, fontweight='bold')
plt.ylabel('Aktual')
plt.xlabel('Prediksi')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✓ Confusion matrix disimpan ke: confusion_matrix.png")

# 7. Feature Importance
print("\n[7] FEATURE IMPORTANCE")
print("-"*70)
feature_importance = pd.DataFrame({
    'Fitur': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print(feature_importance.to_string(index=False))

# Visualisasi Feature Importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Fitur'], feature_importance['Importance'], color='coral')
plt.xlabel('Importance Score', fontsize=12)
plt.title('Feature Importance - Random Forest Classifier', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
print("✓ Feature importance disimpan ke: feature_importance.png")

# 8. Visualisasi Decision Tree
print("\n[8] VISUALISASI DECISION TREE")
print("-"*70)
plt.figure(figsize=(20, 10))
plot_tree(
    rf_model.estimators_[0],
    feature_names=X.columns,
    class_names=[str(c) for c in sorted(y.unique())],
    filled=True,
    rounded=True,
    fontsize=10,
    max_depth=3
)
plt.title('Visualisasi Salah Satu Decision Tree dari Random Forest', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('decision_tree_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualisasi decision tree disimpan ke: decision_tree_visualization.png")

# 9. Prediksi Data Baru (Contoh)
print("\n[9] PREDIKSI DATA BARU (CONTOH)")
print("-"*70)
data_baru = pd.DataFrame({
    'jumlah_penduduk_miskin': [300000, 100000],
    'jumlah_pengangguran_terbuka': [400000, 150000],
    'pdrb_total_adhk': [50000000000, 150000000000],
    'harapan_lama_sekolah': [3, 4]
})

prediksi = rf_model.predict(data_baru)
label_mapping = df.groupby('kesejahteraan_encoded')['kesejahteraan'].first().to_dict()

print("\nHasil Prediksi:")
for i, pred in enumerate(prediksi):
    print(f"\nData ke-{i+1}:")
    print(f"  - Jumlah Penduduk Miskin: {data_baru.iloc[i]['jumlah_penduduk_miskin']:,}")
    print(f"  - Jumlah Pengangguran Terbuka: {data_baru.iloc[i]['jumlah_pengangguran_terbuka']:,}")
    print(f"  - PDRB Total ADHK: Rp {data_baru.iloc[i]['pdrb_total_adhk']:,.0f}")
    print(f"  - Harapan Lama Sekolah: {data_baru.iloc[i]['harapan_lama_sekolah']} tahun")
    print(f"  → Prediksi: {label_mapping[pred]}")

print("\n" + "="*70)
print("PROSES SELESAI!")
print("="*70)
print("\nFile yang dihasilkan:")
print("1. distribusi_kelas.png")
print("2. confusion_matrix.png")
print("3. feature_importance.png")
print("4. decision_tree_visualization.png")
