# 🌟 Prediksi Kesejahteraan Daerah

Aplikasi ini adalah **Sistem Prediksi Kesejahteraan Daerah** berbasis Machine Learning yang dibangun menggunakan **Python** dan **Streamlit**. Aplikasi ini membantu menganalisis indikator sosial-ekonomi untuk memprediksi tingkat kesejahteraan suatu wilayah.

## 🚀 Fitur Utama
- **Prediksi Real-Time**: Input data indikator dan dapatkan status kesejahteraan secara instan.
- **Visualisasi Interaktif**: Eksplorasi dataset dan performa model (Confusion Matrix, Feature Importance).
- **Akurasi Tinggi**: Menggunakan algoritma **Random Forest Classifier** dengan akurasi teruji (> 90%).
- **Antarmuka Premium**: Desain modern dan responsif dengan navigasi intuitif.

## 📂 Struktur Project
```
prediksi_kesejahteraan/
├── dataset/
│   └── dataset_akhir/
│       └── dataset_final.csv      # Raw Data
├── preprocessing/
│   ├── preprocessing.py           # Script pembersihan & persiapan data
│   └── dataset_preprocessed.csv   # Data siap latih
├── modelling/
│   ├── modelling.py               # Script training model
│   ├── rf_model_kesejahteraan.pkl # Model Random Forest
│   ├── metrics.json               # Metrik performa
│   ├── label_mapping.pkl          # Mapping label prediksi
│   └── *.png                      # Gambar hasil evaluasi
├── streamlit/
│   └── app.py                     # Source code aplikasi web
├── requirements.txt               # Dependencies
└── README.md                      # Dokumentasi
```

## 🛠️ Instalasi & Menjalankan Aplikasi

### 1. Persiapan Lingkungan
Pastikan Python 3 sudah terinstall. Disarankan menggunakan virtual environment.

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Pipeline Data (Optional)
Jika ingin melatih ulang model dari awal:

```bash
# 1. Jalankan Preprocessing
python preprocessing/preprocessing.py

# 2. Jalankan Training Model
python modelling/modelling.py
```

### 3. Menjalankan Aplikasi
```bash
streamlit run streamlit/app.py
```
Aplikasi akan terbuka otomatis di browser Anda (biasanya di `http://localhost:8501`).

## 📊 Tentang Model
Model menggunakan **Random Forest Classifier** dengan parameter yang dioptimalkan.
- **Input Features**: Jumlah Penduduk Miskin, Pengangguran Terbuka, PDRB Total ADHK, Harapan Lama Sekolah.
- **Output Classes**: Sangat Sejahtera, Sejahtera, Cukup, Kurang Sejahtera, Tidak Sejahtera (sesuai data).

---
© 2025 Magang PSI STT Wastukancana
