# Water Quality & Potability Decision Support System
**Kombinasi Metode Fuzzy Mamdani + K-Nearest Neighbor (KNN)**  
**Mata Kuliah:** Teknologi Logika Fuzzy  
**Dosen Pengampu:** Dr. Made Agung Raharja, S.Si., M.Cs.  
**Program Studi Informatika, Fakultas MIPA, Universitas Udayana**

---

## Identitas Kelompok 1
1. **Nathanael Adrian Wattimena** (`2408561013`)
2. **I Wayan Arya Adi Guna** (`2408561019`)
3. **Komang Dhika Artika Nurdi** (`2408561055`)
4. **Kadek Phatra Adisuta Timonuli** (`2408561076`)
5. **I Putu Maichail Ganio Wijaya** (`2408561123`)

---

## Deskripsi Singkat Proyek
**Water Quality & Potability Decision Support System** adalah aplikasi cerdas pendukung keputusan berbasis Python dan Streamlit yang mengintegrasikan **Logika Fuzzy Mamdani (White-Box / From Scratch)** dengan algoritma klasifikasi **K-Nearest Neighbor (KNN)** untuk mengevaluasi kualitas fisikokimia air serta menentukan kelayakan konsumsi air minum (`Potable` vs `Not Potable`).

- **Sumber Dataset Publik (100% Bahasa Inggris):** Kaggle — *Water Quality and Potability* (`adityakadiwal/water-potability`, `data/raw/water_potability.csv`, 3.276 baris, 10 kolom bahasa Inggris: `ph`, `Hardness`, `Solids`, `Chloramines`, `Sulfate`, `Conductivity`, `Organic_carbon`, `Trihalomethanes`, `Turbidity`, `Potability`).
- **Metode Integrasi:**
  1. **Fuzzy Mamdani (From Scratch / White-Box):** Mengolah 3 parameter fisikokimia utama sesuai standar WHO / Permenkes (`ph` $X_1 \in [0, 14]$, `Hardness` $X_2 \in [60, 300]$ mg/L, `Turbidity` $X_3 \in [1, 6]$ NTU) menggunakan fungsi keanggotaan segitiga simetris (partisi Ruspini $\sum \mu = 1$), 27 aturan ($3 \times 3 \times 3$), operator AND = MIN, implikasi MIN, agregasi MAX, dan defuzzifikasi **Centroid Analitik Per Segmen** (100% identik dengan integral kalkulus manual, selisih `0.0000`) untuk menghasilkan `fuzzy_quality_score` ($Y \in [0, 100]$).
  2. **Fuzzy-Enhanced KNN (From Scratch & Pembanding Scikit-Learn):** Mengklasifikasikan kelayakan air minum (`Not Potable` vs `Potable`) menggunakan 4 fitur $[X_1, X_2, X_3, Y]$ dengan normalisasi Min-Max bebas *data leakage* (fit hanya pada 480 *training set*) dan jarak Euclidean.

---

## Struktur Direktori Proyek
```text
Final-Project-Fuzzy/
├── app.py                                      # Aplikasi GUI Streamlit (6 Halaman Lengkap - Desain Impeccable)
├── requirements.txt                            # Daftar pustaka Python
├── README.md                                   # Dokumentasi proyek
├── data/
│   ├── raw/
│   │   └── water_potability.csv                # Dataset asli Kaggle (3.276 baris, 10 kolom Bahasa Inggris)
│   └── processed/
│       ├── water_potability_clean.csv          # 600 baris pengamatan bersih & seimbang (300 Not Potable, 300 Potable)
│       └── manual_calc_sample.csv              # 5 baris sampel referensi perhitungan manual (S1-S5)
├── src/
│   ├── __init__.py
│   ├── prepare_dataset.py                      # Pipeline pembersihan dataset Kaggle & ekstraksi skor Fuzzy
│   ├── fuzzy_mamdani.py                        # Implementasi Fuzzy Mamdani From Scratch (Analitik & Diskrit)
│   ├── knn_model.py                            # Implementasi KNN & Scaler From Scratch + Evaluasi
│   └── export_report_artifacts.py              # Script ekspor angka presisi & hitungan manual laporan
├── tests/
│   └── test_system.py                          # Unit tests verifikasi Fuzzy Mamdani & KNN
└── docs/
    ├── experiment_results.json                 # Hasil eksperimen lengkap dalam format JSON
    └── experiment_results_for_report.md        # Ringkasan tabel metrik & hitungan manual untuk laporan TLF
```

---

## Cara Menjalankan Aplikasi & Eksperimen

### 1. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Pemrosesan Dataset & Ekspor Artefak Laporan
```bash
python3 src/prepare_dataset.py
python3 src/export_report_artifacts.py
```

### 3. Menjalankan Unit Tests
```bash
pytest
```

### 4. Menjalankan Aplikasi GUI Streamlit
```bash
streamlit run app.py
```

---

## Ringkasan Hasil Eksperimen (Model A vs Model B)
Pada pembagian data **Stratified Ordered Split** bebas *leakage* (`480` data latih, `120` data uji) dengan normalisasi Min-Max:

| Nilai $K$ | Accuracy Model A (Baseline 3 Fitur) | Accuracy Model B (Fuzzy-Enhanced 4 Fitur) | $\Delta$ Accuracy | Macro-F1 Model A | Macro-F1 Model B | Kesesuaian Scratch vs Sklearn |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **K = 3** | 92.50% | **95.83%** | **+3.33%** | 92.50% | **95.83%** | 100.0% |
| **K = 5** | 92.50% | **95.00%** | **+2.50%** | 92.50% | **95.00%** | 100.0% |
| **K = 7** | 93.33% | **95.83%** | **+2.50%** | 93.33% | **95.83%** | 100.0% |
| **K = 9** | 91.67% | **95.83%** | **+4.17%** | 91.66% | **95.83%** | 100.0% |
| **K = 11** | 93.33% | **97.50%** | **+4.17%** | 93.33% | **97.50%** | 100.0% |
