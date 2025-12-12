import json

# Read the notebook
notebook_path = '/media/boba/DATA/STT Wastukancana/SEMESTER 5/MACHINE LEARNINGGGGG/TUGAS/UAS/prediksi_kesejahteraan/preprocessing/preprocessing.ipynb'

with open(notebook_path, 'r') as f:
    notebook = json.load(f)

# Find the save cell and update the output path
for cell in notebook['cells']:
    if 'save_preprocessed_data' in cell.get('id', ''):
        # Update the source code to use 'dataset_preprocessed.csv'
        cell['source'] = [
            "# Save the preprocessed dataset to CSV in the preprocessing folder\n",
            "output_path = 'dataset_preprocessed.csv'\n",
            "df_model.to_csv(output_path, index=False)\n",
            "print(f'Preprocessed dataset saved to {output_path}')\n"
        ]
        break

# Save the updated notebook
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=2)

print("✓ Berhasil mengupdate preprocessing.ipynb!")
print("✓ Data preprocessed akan disimpan sebagai 'dataset_preprocessed.csv' di folder preprocessing/")
print("\nUntuk menjalankan preprocessing, buka preprocessing.ipynb dan jalankan semua cell")
