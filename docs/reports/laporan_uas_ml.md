**LAPORAN TUGAS AKHIR PEMBELAJARAN MESIN 1**

**(_MACHINE LEARNING I_)**

**(STUDI KASUS: PREDIKSI KESEJAHTERAAN MASYARAKAT JAWA BARAT)**

---

**Disusun Oleh:**

**KELOMPOK [NOMOR KELOMPOK]**

---

**PROGRAM STUDI TEKNIK INFORMATIKA**

**SEKOLAH TINGGI TEKNOLOGI WASTUKANCANA**

**2024/2025**

---

# DAFTAR ISI

- BAB I - PENDAHULUAN
- BAB II - LANDASAN TEORI
- BAB III - DATA UNDERSTANDING
- BAB IV - DATA PREPARATION
- BAB V - MODELING
- BAB VI - EVALUATION
- BAB VII - DEPLOYMENT
- BAB VIII - PENUTUP

---

# BAB I - PENDAHULUAN

## 1.1 Latar Belakang

Kesejahteraan masyarakat merupakan indikator penting dalam pembangunan daerah. Pemerintah Jawa Barat memerlukan sistem yang dapat memprediksi tingkat kesejahteraan untuk membantu pengambilan keputusan dalam program pembangunan.

Proyek ini mengembangkan sistem prediksi kesejahteraan menggunakan Machine Learning dengan algoritma Random Forest, berdasarkan data indikator sosial-ekonomi dari Open Data Jabar periode 2010-2024.

## 1.2 Rumusan Masalah

1. Bagaimana membangun model prediksi kesejahteraan yang akurat?
2. Fitur apa saja yang paling berpengaruh terhadap kesejahteraan?
3. Bagaimana mengimplementasikan model dalam aplikasi web?

## 1.3 Tujuan

1. Membangun model Machine Learning untuk prediksi kesejahteraan dengan akurasi minimal 75%
2. Mengidentifikasi fitur-fitur yang paling berpengaruh
3. Membuat aplikasi web yang dapat diakses secara online

## 1.4 Manfaat

- **Pemerintah**: Membantu identifikasi wilayah yang perlu perhatian khusus
- **Peneliti**: Tools untuk analisis kesejahteraan masyarakat
- **Mahasiswa**: Referensi implementasi Machine Learning

---

# BAB II - LANDASAN TEORI

## 2.1 Machine Learning

Machine Learning adalah cabang AI yang memungkinkan komputer belajar dari data tanpa diprogram secara eksplisit. Dalam proyek ini digunakan untuk memprediksi kategori kesejahteraan berdasarkan data historis.

## 2.2 Random Forest

Random Forest adalah algoritma ensemble yang menggabungkan banyak decision trees untuk menghasilkan prediksi yang lebih akurat dan stabil. Dipilih karena:
- Robust terhadap overfitting
- Dapat menangani data non-linear
- Memberikan informasi feature importance

## 2.3 Metrik Evaluasi

- **Accuracy**: Persentase prediksi yang benar
- **Precision**: Ketepatan prediksi positif
- **Recall**: Kemampuan mendeteksi kelas tertentu
- **F1-Score**: Keseimbangan precision dan recall

---

# BAB III - DATA UNDERSTANDING

## 3.1 Sumber Data

Data diperoleh dari **Open Data Jawa Barat** (opendata.jabarprov.go.id) dengan 6 dataset:

1. **Jumlah Penduduk** (OD_2374)
2. **Jumlah Penduduk Miskin** (OD_2331)
3. **Jumlah Pengangguran Terbuka** (OD_2332)
4. **PDRB Total ADHK** (OD_2323)
5. **Harapan Lama Sekolah** (OD_2328)
6. **Skor Kesejahteraan** (hasil perhitungan manual)

**Periode**: 2010-2024  
**Cakupan**: 27 Kabupaten/Kota di Jawa Barat  
**Total Data**: 405 observasi

## 3.2 Kategori Kesejahteraan

Dataset memiliki 5 kategori target:
1. **Sangat Sejahtera**: Kondisi ekonomi sangat baik
2. **Sejahtera**: Kondisi baik
3. **Cukup**: Kondisi moderat
4. **Tidak Sejahtera**: Perlu perhatian
5. **Sangat Tidak Sejahtera**: Perlu intervensi segera

## 3.3 Struktur Data Akhir

Setelah penggabungan semua dataset:
- **Jumlah Baris**: 405
- **Jumlah Fitur**: 4 fitur + 1 target
- **Format**: CSV

| Fitur | Tipe | Keterangan |
|-------|------|------------|
| jumlah_penduduk_miskin | Numerik | Jumlah penduduk miskin (jiwa) |
| jumlah_pengangguran_terbuka | Numerik | Jumlah pengangguran (jiwa) |
| pdrb_total_adhk | Numerik | PDRB (rupiah) |
| harapan_lama_sekolah | Numerik | Skor pendidikan (1-4) |
| kesejahteraan | Kategori | Target label (5 kelas) |

---

# BAB IV - DATA PREPARATION

## 4.1 Penggabungan Dataset

6 dataset dari Open Data Jabar digabungkan berdasarkan tahun dan nama kabupaten/kota. Proses ini menghasilkan satu dataset final dengan 405 baris.

## 4.2 Preprocessing

Tahapan preprocessing yang dilakukan:

**1. Handling Missing Values**
- Mengisi nilai kosong dengan median
- Median dipilih karena robust terhadap outlier

**2. Feature Selection**
- Memilih 4 fitur utama yang relevan
- Menghapus kolom metadata (tahun, nama wilayah)
- **Tidak menggunakan** kolom skor dan jumlah_penduduk untuk menghindari data leakage

**3. Output Preprocessing**
- File: `dataset_preprocessed.csv`
- Shape: (405, 5) = 405 data × 5 kolom

**Catatan**: Scaling dan encoding dilakukan di tahap modeling, bukan preprocessing.

## 4.3 Pembagian Fitur

**Fitur Input (X):**
1. Jumlah Penduduk Miskin → indikator negatif
2. Jumlah Pengangguran Terbuka → indikator negatif
3. PDRB Total ADHK → indikator positif (ekonomi kuat)
4. Harapan Lama Sekolah → indikator positif (pendidikan)

**Target (y):**
- Kategori Kesejahteraan (5 kelas)

---

# BAB V - MODELING

## 5.1 Algoritma yang Digunakan

**Random Forest Classifier** dipilih dengan konfigurasi:
- Jumlah trees: 100
- Max depth: 10
- Random state: 42 (untuk reproducibility)
- Class weight: balanced (menangani imbalance)

## 5.2 Tahapan Modeling

**1. Load Data**
- Memuat dataset_preprocessed.csv

**2. Encoding Target**
- Mengubah kategori text menjadi numerik (0-4)

**3. Train-Test Split**
- Training: 80% (324 data)
- Testing: 20% (81 data)

**4. Scaling**
- Menggunakan StandardScaler
- Fit pada training, transform pada testing

**5. Training Model**
- Melatih Random Forest dengan training data
- Waktu training: < 1 detik

## 5.3 Hasil Training

| Metric | Nilai |
|--------|-------|
| **Test Accuracy** | **93.83%** |
| Training Accuracy | ~98% |
| Prediksi Benar | 76 dari 81 |
| Prediksi Salah | 5 dari 81 |

## 5.4 Feature Importance

Kontribusi masing-masing fitur terhadap prediksi:

1. **PDRB** → 40-45% (paling penting)
2. **Jumlah Penduduk Miskin** → 25-30%
3. **Jumlah Pengangguran** → 20-25%
4. **Harapan Lama Sekolah** → 10-15%

**Kesimpulan**: PDRB (indikator ekonomi) adalah faktor paling berpengaruh terhadap kesejahteraan.

## 5.5 Model Artifacts

Model yang sudah dilatih disimpan dalam file:
- `rf_model_kesejahteraan.pkl` (ukuran ~1-2 MB)
- `metrics.json` (hasil evaluasi)
- Visualisasi (confusion matrix, feature importance)

---

# BAB VI - EVALUATION

## 6.1 Hasil Evaluasi

**Akurasi: 93.83%** ✅ (Target minimal: 75%)

Model berhasil memprediksi dengan benar 76 dari 81 data testing.

## 6.2 Metrik Detail Per Kelas

| Kelas | Support | Precision | Recall | F1-Score |
|-------|---------|-----------|--------|----------|
| Cukup | 10 | 83% | 100% | 91% |
| Sangat Sejahtera | 24 | 100% | 100% | 100% |
| Sangat Tidak Sejahtera | 27 | 100% | 89% | 94% |
| Sejahtera | 3 | 100% | 67% | 80% |
| Tidak Sejahtera | 17 | 84% | 94% | 89% |

**Rata-rata Weighted**: Precision 95%, Recall 94%, F1 94%

## 6.3 Analisis

**Kekuatan:**
- Akurasi sangat tinggi (93.83%)
- Tidak overfitting (gap training-testing hanya ~4%)
- Performa baik di semua kelas, terutama "Sangat Sejahtera" (perfect score)

**Kelemahan:**
- Kelas "Sejahtera" recall agak rendah (67%) karena data sedikit (3 sampel)

## 6.4 Confusion Matrix

Total kesalahan hanya **5 prediksi** dari 81:
- 3 data "Sangat Tidak Sejahtera" diprediksi sebagai "Tidak Sejahtera"
- 1 data "Sejahtera" salah prediksi
- 1 data minor lainnya

Kesalahan terjadi pada kelas yang berdekatan (overlap karakteristik).

---

# BAB VII - DEPLOYMENT

## 7.1 Platform

Aplikasi dideploy menggunakan **Streamlit Community Cloud**:
- Gratis untuk public repository
- Mudah digunakan
- Terintegrasi dengan GitHub
- Auto-update saat ada perubahan kode

## 7.2 URL Aplikasi

🌐 **Link Deployment:**  
https://prediksi-kesejahteraan-masyarakat-jawa-barat.streamlit.app/

**Status**: Online 24/7

## 7.3 Fitur Aplikasi

Aplikasi memiliki 5 halaman:

**1. Home** 🏠
- Pengenalan sistem
- Informasi project

**2. Prediksi** 🎯
- Input data indikator sosial-ekonomi
- Prediksi kategori kesejahteraan
- Confidence score

**3. Dataset** 📊
- Preview dataset training
- Statistik data

**4. Evaluasi** 📈
- Confusion matrix
- Classification report
- Feature importance chart
- Metrik performa

**5. About** ℹ️
- Informasi tim
- Metodologi
- Kontak

## 7.4 Cara Menggunakan

1. Buka link aplikasi di browser
2. Pilih menu "Prediksi" di sidebar
3. Isi form dengan data:
   - Jumlah Penduduk Miskin
   - Jumlah Pengangguran
   - PDRB
   - Harapan Lama Sekolah
4. Klik tombol "Prediksi"
5. Lihat hasil prediksi dan confidence score

## 7.5 Teknologi

- **Backend**: Python, Streamlit
- **Model**: Random Forest (scikit-learn)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Deployment**: Streamlit Cloud
- **Version Control**: GitHub

---

# BAB VIII - PENUTUP

## 8.1 Kesimpulan

1. **Model Berhasil Dibangun**
   - Random Forest Classifier dengan 4 fitur input
   - Akurasi 93.83% (melampaui target 75%)
   - Training cepat (< 1 detik)

2. **Fitur Penting Teridentifikasi**
   - PDRB adalah faktor paling berpengaruh (40-45%)
   - Kemiskinan dan pengangguran juga signifikan (45-55% total)
   - Pendidikan berkontribusi moderat (10-15%)

3. **Aplikasi Web Berhasil Dideploy**
   - Online dan dapat diakses publik
   - Interface user-friendly
   - Response time cepat (< 2 detik)

4. **Kontribusi Praktis**
   - Membantu pemerintah identifikasi wilayah prioritas
   - Tools analisis untuk peneliti
   - Demonstrasi implementasi ML untuk mahasiswa

## 8.2 Saran

**Untuk Pengembangan Selanjutnya:**

1. **Data**
   - Tambah jumlah data (target 1000+ sampel)
   - Tambah fitur (kesehatan, infrastruktur, lingkungan)
   - Update data secara berkala

2. **Model**
   - Coba algoritma lain (XGBoost, Neural Network)
   - Hyperparameter tuning untuk optimasi
   - Cross-validation yang lebih komprehensif

3. **Aplikasi**
   - Tambah fitur batch prediction (upload CSV)
   - Visualisasi map Jawa Barat
   - Export hasil ke PDF
   - API untuk integrasi sistem lain

4. **Validasi**
   - Test dengan data provinsi lain
   - User testing dengan stakeholder
   - Monitor performa model secara berkala

---

# DAFTAR PUSTAKA

1. Open Data Jawa Barat. (2024). Dataset Kesejahteraan Masyarakat. https://opendata.jabarprov.go.id/
2. Scikit-learn Documentation. (2024). Random Forest Classifier. https://scikit-learn.org/
3. Streamlit Documentation. (2024). Streamlit Cloud Deployment. https://streamlit.io/
4. Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.
5. Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning.

---

**END OF REPORT**
