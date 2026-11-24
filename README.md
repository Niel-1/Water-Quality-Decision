# 💧 Water Quality & Potability Decision Support System (DSS)

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dy7smhepnatesntag7p8dd.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit UI](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Unit Tests](https://img.shields.io/badge/Tests-5%2F5%20Passed%20(100%25)-success.svg?logo=pytest&logoColor=white)](tests/test_system.py)
[![Academic Project](https://img.shields.io/badge/Universitas%20Udayana-Informatika-003366.svg)](https://if.unud.ac.id/)

> **Final Project — Mata Kuliah Teknologi Logika Fuzzy**  
> Program Studi Informatika, Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Udayana  
> **Dosen Pengampu**: Dr. Made Agung Raharja, S.Si., M.Cs.  
> **Kelompok**: 1 (Satu)

🔗 **Demo aplikasi (live):** [dy7smhepnatesntag7p8dd.streamlit.app](https://dy7smhepnatesntag7p8dd.streamlit.app)

---

## 📌 Daftar Isi
1. [Ikhtisar Proyek](#-ikhtisar-proyek)
2. [Arsitektur Sistem (Two-Stage Pipeline)](#️-arsitektur-sistem-two-stage-pipeline)
3. [Formulasi Matematis & Algoritma](#-formulasi-matematis--algoritma)
   - [Tahap 1: Mesin Inferensi Fuzzy Mamdani](#tahap-1-mesin-inferensi-fuzzy-mamdani)
   - [Tahap 2: Fuzzy-Enhanced KNN Classification](#tahap-2-fuzzy-enhanced-knn-classification)
4. [Hasil Evaluasi & Komparasi Model](#-hasil-evaluasi--komparasi-model)
5. [Fitur Antarmuka GUI (Streamlit 6 Halaman)](#️-fitur-antarmuka-gui-streamlit-6-halaman)
6. [Struktur Direktori](#-struktur-direktori)
7. [Panduan Instalasi & Penggunaan](#-panduan-instalasi--penggunaan)
8. [Pengujian Otomatis](#-pengujian-otomatis)
9. [Anggota Kelompok 1](#-anggota-kelompok-1)

---

## 📖 Ikhtisar Proyek

Penilaian kelayakan air minum (*Potable* vs *Not Potable*) mengacu pada baku mutu fisikokimia dunia (**WHO 2022**) dan nasional (**Permenkes RI No. 2 Tahun 2023**) menggunakan 3 parameter krusial:
- **pH ($X_1$)**: Derajat keasaman $[0.0, 14.0]$ (rentang aman yang umum dipakai: $6.5 - 8.5$).
- **Hardness ($X_2$)**: Kesadahan mineral kalsium & magnesium $[60.0, 300.0]$ mg/L (batas ideal pada sistem ini: $\le 150$ mg/L).
- **Turbidity ($X_3$)**: Kekeruhan akibat partikel tersuspensi $[1.0, 6.0]$ NTU (batas ideal pada sistem ini: $\le 1.0$ NTU).

> **Catatan**: Domain variabel dan batas ideal Hardness serta Turbidity merupakan **asumsi pakar dan batas desain sistem** yang dipakai kelompok untuk merancang fungsi keanggotaan fuzzy. Nilai tersebut tidak dimaksudkan sebagai kutipan langsung batas resmi WHO maupun Permenkes.

### Mengapa Kombinasi Fuzzy Mamdani + KNN?
1. **Kelemahan Ambang Batas Kaku (*Crisp*)**: Batas kelayakan air tidak hitam-putih. Sampel air dengan pH $6.49$ tidak adil divonis gagal total jika kesadahan dan kekeruhannya sangat jernih. Logika Fuzzy memodelkan ketidakpastian dan pengetahuan pakar ini secara kontinu.
2. **Kelemahan KNN Klasik (Model A - 3 Fitur Mentah)**: Jarak Euclidean pada fitur mentah rentan salah klasifikasi di area perbatasan kelas (*decision boundary*).
3. **Inovasi Model B (4 Fitur)**: Skor kualitas air dari Fuzzy Mamdani ($z^*$) disuntikkan sebagai fitur ke-4 $[\text{pH}, \text{Hardness}, \text{Turbidity}, z^*]$. Hasilnya, Model B unggul pada seluruh nilai $K$ yang diuji. Pada $K = 11$, akurasi naik dari **93.33% (Model A) menjadi 97.50% (Model B)**, dan pada $K = 5$ jumlah kesalahan klasifikasi turun dari 9 menjadi 6 sampel (reduksi galat **33.3%**).

---

## ⚙️ Arsitektur Sistem (Two-Stage Pipeline)

```
                     Input Sampel Fisikokimia
                   [pH, Hardness, Turbidity]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  TAHAP 1: FUZZY MAMDANI INFERENCE ENGINE                    │
│  1. Fuzzifikasi: Partisi Segitiga Simetris Ruspini          │
│     - pH:        [Acidic, Neutral, Alkaline]                │
│     - Hardness:  [Soft, Moderate, Hard]                     │
│     - Turbidity: [Clear, Moderate, Turbid]                  │
│  2. Evaluasi 27 Basis Aturan Pakar Lengkap (3 x 3 x 3)      │
│     - Operator Anteseden AND = MIN                          │
│     - Operator Implikasi     = MIN                          │
│  3. Agregasi Kurva Konsekuen = MAX                          │
│     - Output Sets: [Poor, Moderate, Good]                   │
│  4. Defuzzifikasi Centroid Analitik Eksak (Piecewise Linear)│
│     - Menghasilkan: fuzzy_quality_score (z* dalam [0, 100]) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  TAHAP 2: FUZZY-ENHANCED KNN CLASSIFICATION                 │
│  1. Pembentukan Vektor Fitur 4D: [pH, Hardness, Turb, z*]   │
│  2. Min-Max Normalization (Fit murni pada 480 Data Latih)   │
│  3. Perhitungan Jarak Euclidean 4 Dimensi                   │
│  4. Pemilihan K Tetangga Terdekat & Majority Voting         │
│     - Tie-breaking: Rata-rata jarak tetangga terendah       │
│  5. Keputusan Akhir: "Potable" (1) atau "Not Potable" (0)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Formulasi Matematis & Algoritma

Algoritma inti (mesin Mamdani, *scaler*, dan KNN) dibangun **dari awal (*from scratch*)** menggunakan Python (`numpy` dan `pandas`) tanpa library fuzzy eksternal. Library `scikit-learn` hanya dipakai sebagai pembanding verifikasi pada unit test, sedangkan antarmuka memakai Streamlit dan Plotly.

### Tahap 1: Mesin Inferensi Fuzzy Mamdani
* **Fungsi Keanggotaan Segitiga Simetris Ruspini**:
  Memenuhi syarat partisi Ruspini di mana pada setiap titik $x$ berlaku $\sum_{i} \mu_i(x) = 1$. Mendukung kondisi bahu kiri ($a = b$) dan bahu kanan ($b = c$).
  $$\mu(x; a, b, c) = \begin{cases} 0, & x \le a \text{ atau } x \ge c \\ \dfrac{x - a}{b - a}, & a < x \le b \\ \dfrac{c - x}{c - b}, & b < x < c \end{cases}$$
* **Defuzzifikasi Centroid Analitik Eksak**:
  Mengintegrasikan luas ($A_i$) dan momen ($M_i$) secara eksak pada setiap segmen linear $[z_0, z_1]$ tanpa galat diskretisasi numerik:
  $$A_i = \frac{1}{2} \Delta z (y_0 + y_1), \quad M_i = \frac{\Delta z}{6} \left[ y_0 (2 z_0 + z_1) + y_1 (z_0 + 2 z_1) \right]$$
  $$z^* = \frac{\sum M_i}{\sum A_i}$$

### Tahap 2: Fuzzy-Enhanced KNN Classification
* **Min-Max Scaling Bebas Kebocoran Data (*Leakage-Free*)**:
  Parameter $x_{\min}$ dan $x_{\max}$ dihitung khusus dari 480 data latih:
  $$x'_{ij} = \frac{x_{ij} - x_{\min, j}}{x_{\max, j} - x_{\min, j}}$$
* **Jarak Euclidean & Voting**:
  $$d(\mathbf{x}_q, \mathbf{x}_i) = \sqrt{\sum_{j=1}^{d} (x'_{q, j} - x'_{i, j})^2}$$
  Voting mayoritas pada $K$ tetangga terdekat, dengan kesesuaian prediksi 100% identik terhadap `scikit-learn`.

---

## 📊 Hasil Evaluasi & Komparasi Model

Evaluasi komparatif dilakukan pada **120 data uji terstratifikasi** (60 Potable, 60 Not Potable) membandingkan **Model A (Baseline KNN 3 Fitur)** vs **Model B (Fuzzy-Enhanced KNN 4 Fitur)**:

| Nilai $K$ | Akurasi Model A | Akurasi Model B | Peningkatan ($\Delta$) | Macro-F1 Model B | Kesesuaian Sklearn |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $K = 3$ | 92.50% (111/120) | **95.83%** (115/120) | +3.33% | 95.83% | 100.0% |
| $K = 5$ | 92.50% (111/120) | **95.00%** (114/120) | +2.50% | 95.00% | 100.0% |
| $K = 7$ | 93.33% (112/120) | **95.83%** (115/120) | +2.50% | 95.83% | 100.0% |
| $K = 9$ | 91.67% (110/120) | **95.83%** (115/120) | +4.17% | 95.83% | 100.0% |
| $K = 11$ | 93.33% (112/120) | **97.50%** (117/120) | +4.17% | 97.50% | 100.0% |

> **Audit Matriks Konfusi ($K = 5$)**: Model B memangkas kesalahan klasifikasi dari 9 sampel menjadi hanya 6 sampel (reduksi galat sebesar **33.3%**).

---

## 🖥️ Fitur Antarmuka GUI (Streamlit 6 Halaman)

Aplikasi dilengkapi antarmuka grafis interaktif berbasis web (Streamlit) dengan tema *dark-mode* modern dan palet visual presisi. Coba langsung di [demo aplikasi](https://dy7smhepnatesntag7p8dd.streamlit.app).

| Halaman | Judul Menu | Fitur & Visualisasi Utama |
| :---: | :--- | :--- |
| **01** | **Ringkasan Sistem** | KPI metrik dataset, ringkasan alur Two-Stage Pipeline, dan profil Kelompok 1. |
| **02** | **Simulasi & Data** | Preset sampel cepat ($S1 - S5$, $Q^*$), slider parameter manual, pemilihan pool referensi, dan tabel dataset interaktif. |
| **03** | **Bedah Perhitungan** | **Transparansi Matematika (*Whitebox*)**: Substitusi rumus fuzzifikasi, tabel 27 aturan aktif, integral per segmen defuzzifikasi, dan normalisasi jarak KNN. |
| **04** | **Hasil & Ranking** | Gauge skor fuzzy $z^*$, radar profile fisikokimia, ranking tetangga terdekat, dan kartu keputusan kelayakan air minum. |
| **05** | **Evaluasi Model A vs B** | Tabel metrik komparasi lintas $K \in \{3,5,7,9,11\}$, heatmap matriks konfusi, dan grafik peningkatan performa. |
| **06** | **Referensi & Panduan** | Landasan teori, baku mutu WHO/Permenkes, formulasi rumus lengkap, serta petunjuk penggunaan sistem. |

---

## 📁 Struktur Direktori

```
├── app.py                          # Router & Entrypoint utama Streamlit
├── requirements.txt                # Dependensi pustaka Python
├── CODEBASE_DOCUMENTATION.md       # Dokumentasi teknis arsitektur & spesifikasi sistem
├── .gitignore                      # Pengecualian file Python & environment
├── .streamlit/
│   └── config.toml                 # Konfigurasi tema Streamlit
├── data/
│   ├── raw/
│   │   └── water_potability.csv    # Dataset mentah publik Kaggle (3.276 sampel)
│   └── processed/
│       ├── water_potability_clean.csv # 600 sampel seimbang dengan skor fuzzy
│       └── manual_calc_sample.csv  # 5 sampel referensi perhitungan manual (S1 - S5)
├── docs/                           # Skrip presentasi & luaran dokumentasi
├── src/
│   ├── fuzzy_mamdani.py            # Mesin Inferensi Mamdani & Centroid Analitik
│   ├── knn_model.py                # MinMaxScaler & KNN Classifier from Scratch
│   ├── prepare_dataset.py          # Script pembersihan data & penyeimbangan 600 sampel
│   ├── export_report_artifacts.py  # Ekspor artefak evaluasi sistem
│   ├── ui/
│   │   ├── theme.py                # CSS tema dark luxury & font styling
│   │   ├── constants.py            # Palet warna, preset input, dan profil anggota
│   │   ├── components.py           # Widget UI: telemetry tray, KPI grid, badge, tabel
│   │   ├── charts.py               # Visualisasi Plotly: kurva MF, radar, centroid area
│   │   ├── data.py                 # Caching data (@st.cache_data) & evaluasi kueri
│   │   └── pages/                  # 6 Modul halaman navigasi SPA
│   └── utils/
│       ├── generate_presentation.py    # Generator slide presentasi PPTX (20 slides)
│       ├── generate_report_figures.py  # Generator diagram PNG untuk laporan
│       └── export_report_html.py       # Generator laporan HTML standar Universitas Udayana
└── tests/
    └── test_system.py              # Unit test pytest (100% lolos)
```

---

## 🚀 Panduan Instalasi & Penggunaan

### 1. Klon Repositori
```bash
git clone https://github.com/dhikrtika/Water-Quality-Decision.git
cd Water-Quality-Decision
```

### 2. Siapkan Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi Web
```bash
streamlit run app.py
```
Buka browser pada alamat: **`http://localhost:8501`**

> Tidak ingin instalasi lokal? Gunakan versi online di [dy7smhepnatesntag7p8dd.streamlit.app](https://dy7smhepnatesntag7p8dd.streamlit.app).

---

## 🧪 Pengujian Otomatis

Rangkaian unit test dirancang untuk memverifikasi kebenaran matematis algoritma:
```bash
pytest -v tests/test_system.py
```

**Verifikasi Pengujian Meliputi**:
- ✅ Partisi Ruspini ($\sum \mu(x) = 1$) pada berbagai titik uji.
- ✅ Kelengkapan 27 basis aturan pakar ($R01 - R27$).
- ✅ *Zero-Discrepancy* ($0.0000$ selisih) antara perhitungan manual langkah demi langkah vs program pada sampel $S4$ ($z^* = 55.9524$) dan $Q^*$ ($z^* = 54.1667$).
- ✅ Kesesuaian 100% antara `KNNClassifierScratch` terhadap `scikit-learn`.
- ✅ Keunggulan konsisten Model B terhadap Model A pada seluruh $K \in \{3, 5, 7, 9, 11\}$.

---

## 👥 Anggota Kelompok 1

Program Studi Informatika, FMIPA Universitas Udayana:

| No. | Nama Mahasiswa | NIM | Peran & Kontribusi Utama |
| :---: | :--- | :---: | :--- |
| 1 | **Nathanael Adrian Wattimena** | `2408561013` | Perancangan fungsi keanggotaan Ruspini, 27 basis aturan, mesin Centroid analitik Mamdani, dan landasan teori. |
| 2 | **I Wayan Arya Adi Guna** | `2408561019` | Implementasi `MinMaxScalerScratch`, `KNNClassifierScratch`, modul evaluasi komparatif Model A vs B, dan bab penutup. |
| 3 | **Komang Dhika Artika Nurdi** | `2408561055` | Pipeline prapemrosesan dataset 600 sampel, perhitungan manual sampel $S4$ & $Q^*$, dan pengujian `pytest`. |
| 4 | **Kadek Phatra Adisuta Timonuli** | `2408561076` | Pengembangan antarmuka GUI Streamlit 6 halaman, integrasi Plotly interaktif, dan visualisasi *whitebox*. |
| 5 | **I Putu Maichail Ganio Wijaya** | `2408561123` | Integrasi *end-to-end*, validasi selisih nol manual vs program, penyusunan bab pendahuluan, dan penyuntingan teknis. |

---
*© 2026 Kelompok 1 — Teknologi Logika Fuzzy, Program Studi Informatika, FMIPA Universitas Udayana.*
