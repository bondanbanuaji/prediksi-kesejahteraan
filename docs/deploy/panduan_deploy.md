# 🚀 Panduan Deployment Aplikasi Streamlit
## Prediksi Kesejahteraan Masyarakat Jawa Barat

Panduan ini menjelaskan langkah-langkah untuk menjalankan aplikasi secara lokal dan mendepoy ke Streamlit Cloud.

---

### 📋 Persiapan Awal
Pastikan Anda memiliki file berikut dalam struktur proyek Anda:
1.  `streamlit/app.py` (File utama aplikasi)
2.  `streamlit/requirements.txt` (Daftar library yang dibutuhkan)
3.  `streamlit/src/` & `streamlit/views/` (Folder source code)
4.  `modelling/rf_model_kesejahteraan.pkl` (File model)
5.  `preprocessing/dataset_preprocessed.csv` (File dataset)

---

### 💻 1. Menjalankan Aplikasi Secara Lokal (Localhost)

1.  **Buka Terminal** dan arahkan ke folder proyek:
    ```bash
    cd /path/to/project/prediksi_kesejahteraan
    ```

2.  **Buat Virtual Environment** (Opsional tapi disarankan):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    ```

3.  **Install Library**:
    ```bash
    pip install -r streamlit/requirements.txt
    ```

4.  **Jalankan Aplikasi**:
    ```bash
    streamlit run streamlit/app.py
    ```

---

### ☁️ 2. Deploy ke Streamlit Cloud (Gratis)

Streamlit Cloud adalah cara termudah untuk mempublikasikan aplikasi ini agar bisa diakses orang lain.

#### Langkah 1: Push Kode ke GitHub
Pastikan seluruh folder proyek `prediksi_kesejahteraan` sudah di-upload ke repository GitHub Anda. Pastikan struktur foldernya benar.

#### Langkah 2: Buat Akun Streamlit Cloud
1.  Buka [share.streamlit.io](https://share.streamlit.io/).
2.  Login menggunakan akun GitHub Anda.

#### Langkah 3: Deploy App
1.  Klik tombol **"New app"**.
2.  Pilih **Repository**, **Branch**, dan **Main file path**.
    *   **Repository**: Pilih repo proyek Anda.
    *   **Branch**: `main` (atau branch utama Anda).
    *   **Main file path**: `streamlit/app.py`.
3.  Klik **"Deploy!"**.

#### Penting: Konfigurasi Path
Karena aplikasi ini menggunakan struktur folder tertentu, pastikan kode memuat file model & dataset dengan path relatif yang benar. Aplikasi ini sudah dikonfigurasi menggunakan `os.path` di `src/config.py` sehingga seharusnya berjalan lancar di mana saja.

---

### 🛠️ Troubleshooting

**Error: Model not found / FileNotFoundError**
*   Cek apakah file `.pkl` dan `.csv` ikut terupload ke GitHub.
*   Pastikan path di `src/config.py` sudah benar.

**Error: Module not found**
*   Pastikan semua library terdaftar di `streamlit/requirements.txt`.

**Tampilan Berantakan**
*   Aplikasi ini menggunakan Dark Mode secara default. Streamlit Cloud biasanya mengikuti pengaturan sistem pengguna, tapi CSS khusus (`src/styles.py`) akan memaksa tampilan agar konsisten.

---
*Dibuat untuk Tugas UAS Machine Learning - STT Wastukancana*
