# 💧 Water Quality & Potability Decision Support System (DSS)

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dy7smhepnatesntag7p8dd.streamlit.app)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit UI](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Unit Tests](https://img.shields.io/badge/Tests-5%2F5%20Passed%20(100%25)-success.svg?logo=pytest&logoColor=white)](tests/test_system.py)
[![Academic Project](https://img.shields.io/badge/Universitas%20Udayana-Informatika-003366.svg)](https://if.unud.ac.id/)

> **Final Project, Mata Kuliah Teknologi Logika Fuzzy**  
> **Sistem Pendukung Keputusan Penentuan Kualitas dan Kelayakan Air Minum Menggunakan Kombinasi Metode Fuzzy Mamdani dan K-Nearest Neighbor (KNN)**  
> Program Studi Informatika, Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Udayana  
> **Dosen Pengampu**: Dr. Made Agung Raharja, S.Si., M.Cs.  
> **Kelompok**: 1 (Satu)

🔗 **Demo aplikasi (live):** [dy7smhepnatesntag7p8dd.streamlit.app](https://dy7smhepnatesntag7p8dd.streamlit.app)

---

## Daftar Isi
1. [Ikhtisar Proyek](#ikhtisar-proyek)
2. [Dataset & Prapemrosesan](#dataset--prapemrosesan)
3. [Arsitektur Sistem (Two-Stage Pipeline)](#arsitektur-sistem-two-stage-pipeline)
4. [Formulasi Matematis & Algoritma](#formulasi-matematis--algoritma)
   - [Tahap 1: Mesin Inferensi Fuzzy Mamdani](#tahap-1-mesin-inferensi-fuzzy-mamdani)
   - [Basis Aturan Lengkap (27 Aturan)](#basis-aturan-lengkap-27-aturan)
   - [Tahap 2: Fuzzy-Enhanced KNN Classification](#tahap-2-fuzzy-enhanced-knn-classification)
5. [Verifikasi Perhitungan Manual](#verifikasi-perhitungan-manual)
6. [Hasil Evaluasi & Komparasi Model](#hasil-evaluasi--komparasi-model)
7. [Fitur Antarmuka GUI (Streamlit 6 Halaman)](#fitur-antarmuka-gui-streamlit-6-halaman)
8. [Implementasi & Struktur Direktori](#implementasi--struktur-direktori)
9. [Panduan Instalasi & Penggunaan](#panduan-instalasi--penggunaan)
10. [Pengujian Otomatis](#pengujian-otomatis)
11. [Kelebihan & Batasan Sistem](#kelebihan--batasan-sistem)
12. [Kesimpulan & Saran](#kesimpulan--saran)
13. [Referensi](#referensi)
14. [Anggota Kelompok 1](#anggota-kelompok-1)

---

## Ikhtisar Proyek

Air minum yang aman dikonsumsi (*potable water*) merupakan kebutuhan dasar yang berkaitan langsung dengan kesehatan masyarakat. Proyek ini menilai kelayakan air (*Potable* vs *Not Potable*) dari tiga parameter fisik-kimia yang relatif mudah diukur sehingga sering dipakai untuk skrining awal:

| Parameter | Satuan | Domain pada sistem | Dampak jika menyimpang |
| :--- | :---: | :---: | :--- |
| **pH** ($X_1$) | pH | $[0.0, 14.0]$ | Air terlalu asam memicu korosi pipa; terlalu basa menimbulkan rasa pahit dan kerak. |
| **Hardness** ($X_2$) | mg/L | $[60.0, 300.0]$ | Kesadahan tinggi menimbulkan endapan kapur. |
| **Turbidity** ($X_3$) | NTU | $[1.0, 6.0]$ | Kekeruhan tinggi mengindikasikan partikel tersuspensi dan dapat menjadi tempat berkembangnya mikroorganisme. |

> Domain pH mengikuti skala pH, sedangkan domain Hardness dan Turbidity **ditetapkan oleh tim**. Data di luar domain tersebut dikeluarkan pada tahap prapemrosesan.

### Mengapa Kombinasi Fuzzy Mamdani + KNN?

1. **Kelemahan ambang batas tegas (*crisp threshold*)**: perubahan nilai yang sangat kecil di sekitar batas transisi dapat membalik keputusan secara drastis, dan kualitas air ditentukan oleh interaksi antarparameter sehingga satu parameter yang ideal tidak menjamin air layak bila parameter lain menyimpang jauh. Logika fuzzy (Zadeh, 1965) menyatakan nilai parameter sebagai derajat keanggotaan pada himpunan linguistik, lalu sistem inferensi Mamdani (Mamdani & Assilian, 1975) mengolahnya bersama aturan pakar menjadi skor kualitas air kontinu (`fuzzy_quality_score`) pada rentang 0-100.
2. **Kelemahan KNN pada fitur mentah**: KNN (Cover & Hart, 1967) mengklasifikasikan data berdasarkan kemiripan dengan data historis menggunakan jarak Euclidean. Namun, KNN yang hanya memakai fitur mentah dapat kurang optimal di dekat batas antarkelas, terutama bila kelas saling tumpang tindih pada ruang fitur.
3. **Model B (4 fitur)**: Fuzzy Mamdani berperan sebagai pembentuk fitur berbasis pengetahuan pakar, dan skornya ($z^*$) ditambahkan sebagai fitur ke-4 sehingga vektor fitur menjadi $[\text{pH}, \text{Hardness}, \text{Turbidity}, z^*]$ sebelum klasifikasi KNN. Pendekatan hibrida dua tahap (*two-stage feature enrichment*) ini menggabungkan transparansi pengetahuan pakar dari logika fuzzy dengan kemampuan pengenalan pola dari data historis KNN. Model B unggul pada seluruh nilai $K$ yang diuji. Pada $K = 11$, akurasi naik dari **93.33% (Model A) menjadi 97.50% (Model B)**, dan pada $K = 5$ jumlah kesalahan klasifikasi turun dari 9 menjadi 6 sampel (pengurangan **33.3%**).

### Rumusan Masalah

1. Bagaimana merancang Sistem Inferensi Fuzzy Mamdani dengan fungsi keanggotaan segitiga simetris Ruspini dan 27 basis aturan untuk menghasilkan `fuzzy_quality_score` dari parameter pH, Hardness, dan Turbidity?
2. Bagaimana mengintegrasikan `fuzzy_quality_score` ke dalam ruang fitur 4 dimensi pada algoritma KNN berbasis normalisasi Min-Max dan jarak Euclidean secara *from scratch*?
3. Apakah keluaran program Python konsisten dengan hasil perhitungan manual langkah demi langkah pada sampel referensi S4 dan kasus uji baru $Q^*$?
4. Seberapa besar peningkatan performa klasifikasi Model B (Fuzzy-Enhanced KNN 4 fitur) dibandingkan Model A (Baseline KNN 3 fitur) pada berbagai nilai $K$?

### Tujuan Pengembangan

- Merancang dan mengimplementasikan mesin inferensi Fuzzy Mamdani (fuzzifikasi, 27 aturan, implikasi MIN, agregasi MAX, dan defuzzifikasi Centroid analitik) secara mandiri di Python.
- Membangun pipeline klasifikasi hibrida Fuzzy-KNN dengan fitur tambahan `fuzzy_quality_score` dan memvalidasinya terhadap perhitungan manual langkah demi langkah.
- Mengevaluasi akurasi, precision, recall, F1-score, dan matriks konfusi antara Baseline KNN (Model A, 3 fitur) dan Fuzzy-Enhanced KNN (Model B, 4 fitur) untuk $K \in \lbrace 3, 5, 7, 9, 11 \rbrace$.
- Menyediakan aplikasi Sistem Pendukung Keputusan interaktif berbasis Streamlit yang memudahkan simulasi prediksi, eksplorasi aturan fuzzy, dan verifikasi perhitungan.

### Manfaat

- **Akademik**: studi kasus terapan integrasi logika fuzzy Mamdani dengan algoritma pembelajaran mesin KNN, lengkap dengan pembuktian analitiknya.
- **Praktis**: membantu pengguna atau penguji kualitas air melakukan skrining awal kelayakan air minum secara cepat, transparan, dan mudah dipahami.
- **Pengembangan**: arsitektur kode Python modular yang dapat dikembangkan dengan tambahan parameter kualitas air lain maupun metode klasifikasi lanjutan.

### Penelitian Terkait

| Referensi | Metode utama | Perbedaan dengan proyek ini |
| :--- | :--- | :--- |
| Kusumadewi & Purnomo (2010) | Fuzzy Mamdani pada sistem pendukung keputusan | Proyek ini memakai keluaran Mamdani sebagai fitur tambahan bagi klasifikasi KNN. |
| Keller et al. (1985) | Fuzzy KNN (FKNN), memberi derajat keanggotaan kelas pada data uji berdasarkan jarak ke tetangga terdekat | Proyek ini memisahkan ekstraksi pengetahuan pakar (Mamdani) sebelum klasifikasi KNN, lalu menguji langsung dampak fitur `fuzzy_quality_score` terhadap akurasi KNN pada data kualitas air. |

---

## Dataset & Prapemrosesan

Dataset mentah berasal dari repositori Kaggle *Water Quality and Potability* (Kadiwal, 2021) dengan **3.276 sampel**, sebagian berisi nilai kosong dan kelas tidak seimbang. Tahap prapemrosesan pada `src/prepare_dataset.py`:

1. Menghapus baris dengan nilai kosong (*missing values*).
2. Menyaring data ke domain variabel yang digunakan (pH 0-14, Hardness 60-300 mg/L, Turbidity 1-6 NTU).
3. Menghitung `fuzzy_quality_score` untuk setiap sampel.
4. Menerapkan penyaringan konsistensi fisikokimia: skor $\ge 47.2$ untuk *Potable* dan $< 47.2$ untuk *Not Potable*.
5. Menyusun **600 sampel seimbang** (300 *Potable* dan 300 *Not Potable*) melalui pengambilan acak dengan `random_state = 59`.
6. Membagi data 80:20 secara terstratifikasi pada tahap yang sama: 480 baris pertama menjadi **480 data latih** (240 / 240) dan 120 baris terakhir menjadi **120 data uji** (60 / 60).

Label kelayakan mengikuti label pada dataset sumber. Lima sampel referensi perhitungan manual (S1-S5) pada `data/processed/manual_calc_sample.csv` disusun **secara sintetis** dengan nilai yang dipilih agar perhitungan manual dapat dilakukan secara eksak, sehingga bukan cuplikan langsung dari dataset Kaggle.

**Statistik deskriptif dataset bersih** (`water_potability_clean.csv`, $N = 600$):

| Variabel | Satuan | Min | Q1 (25%) | Median | Mean | Q3 (75%) | Max | Std Dev |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pH ($X_1$) | pH (0-14) | 1.4318 | 6.0696 | 7.0393 | 7.1165 | 8.0883 | 13.3499 | 1.7151 |
| Hardness ($X_2$) | mg/L | 73.4922 | 175.6315 | 197.2792 | 195.2735 | 217.4722 | 286.5680 | 34.0901 |
| Turbidity ($X_3$) | NTU | 1.8444 | 3.4430 | 3.9646 | 3.9713 | 4.5113 | 5.9568 | 0.7570 |
| Solids | ppm | 1372.0900 | 16134.7500 | 21384.6400 | 22237.8212 | 27125.6475 | 55334.7000 | 8482.9323 |
| Chloramines | ppm | 2.4586 | 6.2837 | 7.3009 | 7.2088 | 8.1549 | 13.1270 | 1.6174 |
| Conductivity | μS/cm | 201.6200 | 365.6750 | 424.3900 | 424.4471 | 479.5575 | 753.3400 | 79.6734 |
| `fuzzy_quality_score` ($Y$) | Skor (0-100) | 20.3883 | 44.3975 | 47.2159 | 46.3661 | 49.2897 | 60.0580 | 4.8023 |

---

## Arsitektur Sistem (Two-Stage Pipeline)

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
│     - K bernilai ganjil agar tidak terjadi hasil seri       │
│  5. Keputusan Akhir: "Potable" (1) atau "Not Potable" (0)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Formulasi Matematis & Algoritma

Algoritma inti (mesin Mamdani, *scaler*, dan KNN) dibangun **dari awal (*from scratch*)** dengan Python (`numpy` dan `pandas`) tanpa library fuzzy eksternal. Antarmuka memakai Streamlit dan Plotly, sedangkan grafik laporan memakai Matplotlib.

### Tahap 1: Mesin Inferensi Fuzzy Mamdani

Sistem memiliki 3 variabel input (pH, Hardness, Turbidity) dan 1 variabel output (`water_quality_score`). Inferensi Mamdani berjalan dalam empat tahap: fuzzifikasi, evaluasi aturan dan implikasi (MIN), agregasi (MAX), dan defuzzifikasi Centroid.

**1. Fungsi keanggotaan segitiga simetris Ruspini** dengan parameter $(a, b, c)$, $a \le b \le c$, di mana $b$ adalah titik puncak ($\mu(b) = 1$):

$$
\mu(x; a, b, c) =
\begin{cases}
0, & x \le a \text{ atau } x \ge c \\
\dfrac{x - a}{b - a}, & a < x \le b \\
\dfrac{c - x}{c - b}, & b < x < c
\end{cases}
$$

Pada partisi Ruspini (Ruspini, 1969) berlaku $\sum_{i} \mu_i(x) = 1$ di setiap titik $x$ pada domain. Himpunan tepi kiri memiliki $a = b$ (bahu kiri bernilai 1 untuk $x \le b$) dan himpunan tepi kanan memiliki $b = c$ (bahu kanan bernilai 1 untuk $x \ge b$).

| Variabel | Domain | Himpunan fuzzy dan parameter $(a, b, c)$ |
| :--- | :---: | :--- |
| pH ($X_1$) | $[0, 14]$ | Acidic $(0, 0, 7)$, Neutral $(0, 7, 14)$, Alkaline $(7, 14, 14)$ |
| Hardness ($X_2$) | $[60, 300]$ | Soft $(60, 60, 180)$, Moderate $(60, 180, 300)$, Hard $(180, 300, 300)$ |
| Turbidity ($X_3$) | $[1, 6]$ | Clear $(1, 1, 3.5)$, Moderate $(1, 3.5, 6)$, Turbid $(3.5, 6, 6)$ |
| `water_quality_score` ($Y$) | $[0, 100]$ | Poor $(0, 0, 50)$, Moderate $(0, 50, 100)$, Good $(50, 100, 100)$ |

**2. Evaluasi aturan dan implikasi MIN.** Setiap aturan berbentuk *IF* $X_1$ is $A_1$ *AND* $X_2$ is $A_2$ *AND* $X_3$ is $A_3$ *THEN* $Y$ is $B$. Kekuatan penyulutan (*firing strength*) dihitung dengan operator MIN:

$$
\alpha_r = \min\left(\mu_{A_{r1}}(x_1),\ \mu_{A_{r2}}(x_2),\ \mu_{A_{r3}}(x_3)\right)
$$

Kurva konsekuen kemudian dipotong setinggi $\alpha_r$:

$$
\mu_{B'_r}(z) = \min\left(\alpha_r,\ \mu_{B_r}(z)\right)
$$

**3. Agregasi MAX** menggabungkan seluruh kurva konsekuen hasil implikasi menjadi satu kurva:

$$
\mu_{agg}(z) = \max_{r}\ \mu_{B'_r}(z)
$$

**4. Defuzzifikasi Centroid (Center of Area)** pada domain output $[0, 100]$:

$$
z^* = \frac{\int_{0}^{100} z \cdot \mu_{agg}(z)\, dz}{\int_{0}^{100} \mu_{agg}(z)\, dz}
$$

Karena kurva agregasi linear per segmen (*piecewise linear*), luas ($A_i$) dan momen ($M_i$) diintegrasikan secara **analitik eksak** pada setiap segmen $[z_0, z_1]$ dengan $\Delta z = z_1 - z_0$ tanpa galat diskretisasi numerik:

$$
A_i = \frac{1}{2}\, \Delta z\, (y_0 + y_1), \qquad
M_i = \frac{\Delta z}{6} \left[ y_0 (2 z_0 + z_1) + y_1 (z_0 + 2 z_1) \right]
$$

$$
z^* = \frac{\sum_i M_i}{\sum_i A_i}
$$

### Basis Aturan Lengkap (27 Aturan)

Kombinasi seluruh himpunan fuzzy dari 3 variabel input menghasilkan $3^3 = 27$ aturan (R01 sampai R27) yang terdiri atas 3 aturan *Good*, 9 aturan *Moderate*, dan 15 aturan *Poor*. Konsekuen *Good* hanya diberikan bila pH netral dan kombinasi kesadahan-kekeruhan adalah *Soft-Clear*, *Soft-Moderate*, atau *Moderate-Clear*.

Basis aturan disusun berdasarkan prinsip bahwa penyimpangan pada setiap parameter menurunkan kualitas air. Setiap himpunan diberi tingkat penalti:

- pH: *Neutral* bernilai 0, sedangkan *Acidic* atau *Alkaline* bernilai 1.
- Hardness: *Soft* / *Moderate* / *Hard* bernilai 0 / 1 / 2.
- Turbidity: *Clear* / *Moderate* / *Turbid* bernilai 0 / 1 / 2.

Pada pH netral, total penalti $\le 1$ menghasilkan *Good*, total 2 menghasilkan *Moderate*, dan total $\ge 3$ menghasilkan *Poor*. Pada pH asam atau basa, konsekuen *Good* tidak diberikan; total penalti $\le 2$ menghasilkan *Moderate* dan total $\ge 3$ menghasilkan *Poor*.

| Rule | pH ($X_1$) | Hardness ($X_2$) | Turbidity ($X_3$) | Output ($Y$) |
| :---: | :--- | :--- | :--- | :---: |
| R01 | Acidic | Soft | Clear | Moderate |
| R02 | Acidic | Soft | Moderate | Moderate |
| R03 | Acidic | Soft | Turbid | Poor |
| R04 | Acidic | Moderate | Clear | Moderate |
| R05 | Acidic | Moderate | Moderate | Poor |
| R06 | Acidic | Moderate | Turbid | Poor |
| R07 | Acidic | Hard | Clear | Poor |
| R08 | Acidic | Hard | Moderate | Poor |
| R09 | Acidic | Hard | Turbid | Poor |
| R10 | Neutral | Soft | Clear | Good |
| R11 | Neutral | Soft | Moderate | Good |
| R12 | Neutral | Soft | Turbid | Moderate |
| R13 | Neutral | Moderate | Clear | Good |
| R14 | Neutral | Moderate | Moderate | Moderate |
| R15 | Neutral | Moderate | Turbid | Poor |
| R16 | Neutral | Hard | Clear | Moderate |
| R17 | Neutral | Hard | Moderate | Poor |
| R18 | Neutral | Hard | Turbid | Poor |
| R19 | Alkaline | Soft | Clear | Moderate |
| R20 | Alkaline | Soft | Moderate | Moderate |
| R21 | Alkaline | Soft | Turbid | Poor |
| R22 | Alkaline | Moderate | Clear | Moderate |
| R23 | Alkaline | Moderate | Moderate | Poor |
| R24 | Alkaline | Moderate | Turbid | Poor |
| R25 | Alkaline | Hard | Clear | Poor |
| R26 | Alkaline | Hard | Moderate | Poor |
| R27 | Alkaline | Hard | Turbid | Poor |

### Tahap 2: Fuzzy-Enhanced KNN Classification

Skor kualitas air fuzzy digabungkan dengan ketiga fitur fisik-kimia asli menjadi vektor 4 dimensi $\mathbf{x} = [X_1, X_2, X_3, Y]$, kemudian dinormalisasi dengan Min-Max Scaling dan diklasifikasikan oleh KNN.

**Min-Max scaling bebas kebocoran data (*leakage-free*)**: setiap fitur ke-$j$ dinormalisasi ke rentang $[0, 1]$ karena skala fitur sangat berbeda (misalnya pH 0-14 sedangkan Hardness hingga 300 mg/L). Parameter $x_{\min, j}$ dan $x_{\max, j}$ dihitung hanya dari 480 data latih, lalu diterapkan pada data uji:

$$
x'_{ij} = \frac{x_{ij} - x_{\min, j}}{x_{\max, j} - x_{\min, j}}
$$

**Jarak Euclidean** antara vektor data uji ternormalisasi $\mathbf{x}'_q$ dan data latih $\mathbf{x}'_i$ pada ruang berdimensi $d$:

$$
d(\mathbf{x}'_q, \mathbf{x}'_i) = \sqrt{\sum_{j=1}^{d} \left(x'_{qj} - x'_{ij}\right)^2}
$$

**Voting mayoritas**: seluruh jarak diurutkan dari terkecil ke terbesar, diambil $K$ tetangga terdekat, dan kelas prediksi ditetapkan dari mayoritas kelas pada $K$ tetangga tersebut. Nilai $K$ dipilih ganjil untuk mencegah hasil seri pada klasifikasi biner.

---

## Verifikasi Perhitungan Manual

Untuk memverifikasi kebenaran implementasi, disiapkan 5 sampel referensi sintetis (S1-S5) pada `data/processed/manual_calc_sample.csv`:

| Kode | Sample ID | pH ($X_1$) | Hardness ($X_2$) | Turbidity ($X_3$) | `fuzzy_quality_score` ($Y$) | Kelas aktual |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| S1 | WQP-M01 | 3.50 | 240.0 | 4.750 | 44.0476 | Not Potable (0) |
| S2 | WQP-M02 | 10.50 | 240.0 | 4.750 | 44.0476 | Not Potable (0) |
| S3 | WQP-M03 | 7.00 | 180.0 | 3.500 | 50.0000 | Not Potable (0) |
| S4 | WQP-M04 | 7.00 | 120.0 | 2.250 | 55.9524 | Potable (1) |
| S5 | WQP-M05 | 7.00 | 90.0 | 1.625 | 64.6739 | Potable (1) |

Perhitungan manual langkah demi langkah dilakukan pada dua kasus: sampel referensi **S4** dan kasus uji baru **$Q^*$**. Keluaran program dibandingkan dengan hasil manual dan seluruhnya identik (selisih $0.0000$).

| Kasus | Input (pH, Hardness, Turbidity) | Aturan aktif | $[\alpha_{Poor}, \alpha_{Mod}, \alpha_{Good}]$ | $\sum A$ | $\sum M$ | $z^*$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S4** (sampel referensi) | $(7.00,\ 120.0,\ 2.25)$ | 4 aturan | $[0.0000,\ 0.5000,\ 0.5000]$ | 43.7500 | 2447.9167 | **55.9524** |
| **$Q^*$** (kasus uji baru) | $(5.25,\ 150.0,\ 2.25)$ | 8 aturan | $[0.2500,\ 0.5000,\ 0.5000]$ | 45.3125 | 2454.4271 | **54.1667** |

**Contoh S4**: kurva agregasi terdiri atas dua segmen, yaitu garis naik $\mu(z) = 0.02z$ pada $[0, 25]$ dan garis mendatar $\mu(z) = 0.50$ pada $[25, 100]$.

| Segmen | Interval $z$ | $\mu_{agg}(z)$ | Luas $A_i$ | Momen $M_i$ |
| :--- | :---: | :---: | :---: | :---: |
| Segmen 1 | $[0, 25]$ | $0.02z$ | 6.2500 | 104.1667 |
| Segmen 2 | $[25, 100]$ | $0.50$ | 37.5000 | 2343.7500 |
| **Total** | $[0, 100]$ | | **43.7500** | **2447.9167** |

$$
z^*_{S4} = \frac{2447.9167}{43.7500} = 55.9524
$$

**Contoh $Q^*$**: kurva agregasi terdiri atas tiga segmen.

| Segmen | Interval $z$ | $\mu_{agg}(z)$ | Luas $A_i$ | Momen $M_i$ |
| :--- | :---: | :---: | :---: | :---: |
| Segmen 1 | $[0, 12.5]$ | $0.25$ | 3.1250 | 19.5312 |
| Segmen 2 | $[12.5, 25]$ | $0.02z$ | 4.6875 | 91.1458 |
| Segmen 3 | $[25, 100]$ | $0.50$ | 37.5000 | 2343.7500 |
| **Total** | $[0, 100]$ | | **45.3125** | **2454.4271** |

$$
z^*_{Q^*} = \frac{2454.4271}{45.3125} = 54.1667
$$

**Klasifikasi KNN ($K = 3$) untuk $Q^*$** memakai 5 sampel referensi. Parameter Min-Max dihitung dari kelima sampel tersebut:

| Parameter | pH ($X_1$) | Hardness ($X_2$) | Turbidity ($X_3$) | `fuzzy_quality_score` ($Y$) |
| :--- | :---: | :---: | :---: | :---: |
| Minimum | 3.5000 | 90.0000 | 1.6250 | 44.0476 |
| Maksimum | 10.5000 | 240.0000 | 4.7500 | 64.6739 |
| Rentang | 7.0000 | 150.0000 | 3.1250 | 20.6263 |

Vektor $Q^* = [5.25,\ 150.0,\ 2.25,\ 54.1667]$ menjadi $\mathbf{x}'_{Q^*} = [0.2500,\ 0.4000,\ 0.2000,\ 0.4906]$. Hasil jarak Euclidean 4 dimensi dan peringkat tetangga:

| Peringkat | Sampel | Vektor ternormalisasi | $\sum \Delta^2$ | Jarak | Kelas aktual | Status ($K=3$) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | S4 | $[0.5000,\ 0.2000,\ 0.2000,\ 0.5772]$ | 0.1100 | 0.3317 | Potable | Tetangga #1 |
| 2 | S3 | $[0.5000,\ 0.6000,\ 0.6000,\ 0.2886]$ | 0.3033 | 0.5507 | Not Potable | Tetangga #2 |
| 3 | S5 | $[0.5000,\ 0.0000,\ 0.0000,\ 1.0000]$ | 0.5220 | 0.7225 | Potable | Tetangga #3 |
| 4 | S1 | $[0.0000,\ 1.0000,\ 1.0000,\ 0.0000]$ | 1.3032 | 1.1416 | Not Potable | Di luar $K=3$ |
| 5 | S2 | $[1.0000,\ 1.0000,\ 1.0000,\ 0.0000]$ | 1.8032 | 1.3428 | Not Potable | Di luar $K=3$ |

Dari 3 tetangga terdekat (S4, S3, S5) diperoleh suara 2 *Potable* berbanding 1 *Not Potable*, sehingga $Q^*$ diprediksi **Potable (Layak Minum)**.

---

## Hasil Evaluasi & Komparasi Model

Evaluasi dilakukan pada **120 data uji terstratifikasi** (60 *Potable*, 60 *Not Potable*), membandingkan **Model A (Baseline KNN 3 fitur)** dengan **Model B (Fuzzy-Enhanced KNN 4 fitur)**. Penambahan fitur `fuzzy_quality_score` secara konsisten meningkatkan akurasi dan Macro F1-Score pada seluruh nilai $K$ yang diuji:

| Nilai $K$ | Akurasi Model A | Akurasi Model B | $\Delta$ Akurasi | Macro-F1 A | Macro-F1 B | Salah Prediksi B |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $K = 3$ | 92.50% (111/120) | 95.83% (115/120) | +3.33% | 92.50% | 95.83% | 5 / 120 |
| $K = 5$ | 92.50% (111/120) | 95.00% (114/120) | +2.50% | 92.50% | 95.00% | 6 / 120 |
| $K = 7$ | 93.33% (112/120) | 95.83% (115/120) | +2.50% | 93.33% | 95.83% | 5 / 120 |
| $K = 9$ | 91.67% (110/120) | 95.83% (115/120) | +4.17% | 91.66% | 95.83% | 5 / 120 |
| $K = 11$ | 93.33% (112/120) | 97.50% (117/120) | +4.17% | 93.33% | 97.50% | 3 / 120 |

**Metrik per kelas pada $K = 5$:**

| Kelas kelayakan | Support | Precision A | Precision B | Recall A | Recall B | F1-Score A | F1-Score B |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Not Potable (0) | 60 | 90.48% | 93.55% | 95.00% | 96.67% | 92.68% | 95.08% |
| Potable (1) | 60 | 94.74% | 96.55% | 90.00% | 93.33% | 92.31% | 94.92% |
| Rata-rata | 120 | 92.61% | 95.05% | 92.50% | 95.00% | 92.50% | 95.00% |

**Matriks konfusi pada $K = 5$:**

| Model | TN | FP | FN | TP | Total kesalahan | Akurasi |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Model A (3 fitur) | 57 | 3 | 6 | 54 | 9 sampel | 92.50% |
| Model B (4 fitur) | 58 | 2 | 4 | 56 | 6 sampel | 95.00% |

Pada ruang 3 dimensi asli, jarak Euclidean memperlakukan pH, Hardness, dan Turbidity secara terpisah sehingga dua sampel dengan interaksi risiko berbeda dapat terlihat berdekatan. Penambahan dimensi keempat berupa `fuzzy_quality_score` menyuntikkan informasi non-linear dari 27 aturan pakar ke dalam metrik jarak KNN. Dampaknya, sampel di daerah batas keputusan (*decision boundary*) lebih jelas terpisah berdasarkan indeks kelayakan menyeluruhnya, sehingga kesalahan *False Positive* maupun *False Negative* berkurang.

---

## Fitur Antarmuka GUI (Streamlit 6 Halaman)

Aplikasi web interaktif dengan tema *dark-mode* dan navigasi sidebar. Pemisahan halaman memudahkan pengguna berpindah dari simulasi prediksi langsung hingga penelusuran matematis tanpa tampilan yang padat. Coba langsung di [demo aplikasi](https://dy7smhepnatesntag7p8dd.streamlit.app).

| Halaman | Judul Menu | Fitur Utama |
| :---: | :--- | :--- |
| **01** | **Ringkasan Sistem** | Gambaran permasalahan, alur arsitektur dua tahap (Fuzzy Mamdani + KNN), metrik utama, distribusi 600 sampel seimbang, dan profil Kelompok 1. |
| **02** | **Simulasi & Data** | Simulasi 1 sampel (preset $Q^*$ / S1-S5 atau input manual pH, Hardness, Turbidity dengan validasi batas), pemilihan data referensi KNN, dan unggah CSV kustom. |
| **03** | **Bedah Perhitungan** | Penelusuran matematis 4 desimal dalam 3 tab: kurva keanggotaan, substitusi fuzzifikasi dan 27 aturan; kurva agregasi MAX dan integral Centroid ($z^*$); serta normalisasi dan jarak Euclidean KNN. |
| **04** | **Hasil & Ranking** | Klasifikasi dan pemeringkatan seluruh 600 sampel, interpretasi otomatis, sorotan Top 5 terbaik vs 5 paling berisiko, filter kelas/skor, grafik sebaran, dan ekspor CSV. |
| **05** | **Evaluasi Model A vs B** | Perbandingan performa Model A (3 fitur) vs Model B (4 fitur + skor Fuzzy) lintas $K = 3, \dots, 11$, pilihan normalisasi Min-Max/Z-Score, matriks konfusi, metrik per kelas, dan analisis batasan. |
| **06** | **Referensi & Panduan** | Spesifikasi variabel dan titik kurva $[a, b, c]$, rumus matematis Mamdani dan KNN, filter 27 basis aturan, peran library Python, dan panduan penggunaan 6 halaman. |

---

## Implementasi & Struktur Direktori

Sistem dikembangkan pada Python 3.10+. Seluruh logika inti Fuzzy Mamdani dan KNN diimplementasikan secara mandiri menggunakan NumPy.

| Komponen / Library | Fungsi utama dalam sistem |
| :--- | :--- |
| Python 3.10+ | Bahasa pemrograman utama untuk seluruh modul Fuzzy Mamdani dan KNN *from scratch*. |
| `numpy` & `pandas` | Pengolahan matriks fitur, prapemrosesan dataset CSV, dan komputasi vektor jarak Euclidean. |
| `streamlit` & `plotly` | Membangun aplikasi GUI interaktif 6 halaman beserta grafik kurva keanggotaan dan heatmap. |
| `matplotlib` | Menghasilkan grafik statis resolusi tinggi (kurva keanggotaan, perbandingan akurasi, dan matriks konfusi) untuk laporan. |
| `pytest` | Menjalankan rangkaian unit test otomatis untuk seluruh modul inti sistem. |

```
├── app.py                          # Router & entrypoint utama Streamlit (GUI 6 halaman)
├── requirements.txt                # Dependensi pustaka Python
├── CODEBASE_DOCUMENTATION.md       # Dokumentasi teknis arsitektur & spesifikasi sistem
├── .gitignore                      # Pengecualian file Python & environment
├── .streamlit/
│   └── config.toml                 # Konfigurasi tema Streamlit
├── data/
│   ├── raw/
│   │   └── water_potability.csv    # Dataset mentah Kaggle (3.276 sampel)
│   └── processed/
│       ├── water_potability_clean.csv # 600 sampel seimbang dengan skor fuzzy
│       └── manual_calc_sample.csv  # 5 sampel referensi perhitungan manual (S1 - S5)
├── docs/                           # Skrip presentasi & luaran dokumentasi
├── src/
│   ├── fuzzy_mamdani.py            # Fungsi keanggotaan, 27 aturan, inferensi MIN-MAX, Centroid analitik
│   ├── knn_model.py                # MinMaxScalerScratch, ZScoreScalerScratch, KNNClassifierScratch, evaluasi A vs B
│   ├── prepare_dataset.py          # Pembersihan data, penyeimbangan 600 sampel, manual_calc_sample.csv
│   ├── export_report_artifacts.py  # Ekspor hasil eksperimen (JSON/Markdown) & gambar laporan
│   ├── ui/
│   │   ├── theme.py                # CSS tema dark & font
│   │   ├── constants.py            # Palet warna, preset input, dan profil anggota
│   │   ├── components.py           # Widget UI: telemetry tray, KPI grid, badge, tabel
│   │   ├── charts.py               # Visualisasi Plotly: kurva MF, radar, centroid area
│   │   ├── data.py                 # Caching data (@st.cache_data) & evaluasi kueri
│   │   └── pages/                  # 6 modul halaman (dashboard, input_dataset, whitebox, results, evaluation, documentation)
│   └── utils/
│       ├── generate_presentation.py    # Generator slide presentasi PPTX
│       ├── generate_report_figures.py  # Generator grafik untuk laporan
│       └── export_report_html.py       # Generator laporan HTML
└── tests/
    └── test_system.py              # Unit test pytest (5 kasus uji)
```

---

## Panduan Instalasi & Penggunaan

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

### 4. Menjalankan Pengujian Otomatis (opsional)
```bash
python3 -m pytest -q
```

### 5. Menjalankan Aplikasi Web
```bash
streamlit run app.py
```
Buka browser pada alamat **`http://localhost:8501`**. Tidak ingin instalasi lokal? Gunakan versi online di [dy7smhepnatesntag7p8dd.streamlit.app](https://dy7smhepnatesntag7p8dd.streamlit.app).

---

## Pengujian Otomatis

```bash
pytest -v tests/test_system.py
```

Pengujian dilakukan pada tiga lapis:

1. Validasi *zero-discrepancy* antara perhitungan manual dan keluaran kode Python.
2. Pengujian unit otomatis (`pytest`, 5 kasus uji, seluruhnya lulus 100%) untuk memastikan kebenaran fungsi keanggotaan, 27 aturan, defuzzifikasi Centroid, dan jarak Euclidean KNN.
3. Uji komparatif Model A (3 fitur) vs Model B (4 fitur) pada 120 data uji untuk $K \in \lbrace 3, 5, 7, 9, 11 \rbrace$ dengan metrik Accuracy, Precision, Recall, F1-Score, dan Confusion Matrix.

Hasil verifikasi manual vs program (selisih $0.0000$ pada seluruh tahap):

| Kasus | Tahapan / besaran yang diuji | Hasil manual | Hasil program | Status |
| :---: | :--- | :---: | :---: | :---: |
| S4 | Agregasi $[\alpha_{Poor}, \alpha_{Mod}, \alpha_{Good}]$ | $[0.0000,\ 0.5000,\ 0.5000]$ | $[0.0000,\ 0.5000,\ 0.5000]$ | ✅ Identik |
| S4 | Total luas $\sum A$ dan momen $\sum M$ | 43.7500 & 2447.9167 | 43.7500 & 2447.9167 | ✅ Identik |
| S4 | `fuzzy_quality_score` ($z^*$) | 55.9524 | 55.9524 | ✅ Identik |
| $Q^*$ | Agregasi $[\alpha_{Poor}, \alpha_{Mod}, \alpha_{Good}]$ | $[0.2500,\ 0.5000,\ 0.5000]$ | $[0.2500,\ 0.5000,\ 0.5000]$ | ✅ Identik |
| $Q^*$ | Total luas $\sum A$ dan momen $\sum M$ | 45.3125 & 2454.4271 | 45.3125 & 2454.4271 | ✅ Identik |
| $Q^*$ | `fuzzy_quality_score` ($z^*$) | 54.1667 | 54.1667 | ✅ Identik |
| $Q^*$ | Jarak 3 tetangga terdekat (S4, S3, S5) | 0.3317, 0.5507, 0.7225 | 0.3317, 0.5507, 0.7225 | ✅ Identik |
| $Q^*$ | Prediksi KNN ($K = 3$) | Potable (2 : 1) | Potable (2 : 1) | ✅ Identik |

---

## Kelebihan & Batasan Sistem

**Kelebihan**
- Transparansi penuh (*white-box*) karena seluruh tahap Fuzzy Mamdani dan KNN dibangun *from scratch*.
- Akurasi klasifikasi yang konsisten meningkat (+2.50% hingga +4.17%) dibanding Baseline KNN.
- Antarmuka Streamlit yang interaktif untuk simulasi, penelusuran perhitungan, dan evaluasi.

**Batasan**
- Dataset bersumber dari Kaggle dan dibersihkan menjadi 600 sampel seimbang (300 *Potable*, 300 *Not Potable*). Evaluasi memakai pembagian terstratifikasi 80:20 (480 data latih, 120 data uji) dengan normalisasi Min-Max yang dihitung khusus dari data latih agar bebas kebocoran data.
- Input Fuzzy Mamdani dibatasi pada tiga parameter fisik-kimia dasar (pH, Hardness, Turbidity) yang lazim diukur dan tersedia lengkap pada dataset. Karena itu, sistem ditujukan sebagai **alat skrining awal** dan bukan pengganti uji laboratorium menyeluruh.
- Fungsi keanggotaan memakai kurva segitiga simetris Ruspini dengan 3 himpunan linguistik per variabel, sehingga membentuk tepat $3^3 = 27$ basis aturan.
- Parameter fungsi keanggotaan ditetapkan manual dengan partisi seragam pada domain data (titik puncak himpunan tengah berada di titik tengah domain) dan belum dioptimasi secara otomatis terhadap data lapangan.
- Label kelayakan mengikuti label pada dataset sumber.
- Data latih hanya mencakup nilai di dalam domain (pH 0-14, Hardness 60-300 mg/L, Turbidity 1-6 NTU), sehingga hasil sistem tidak dapat diandalkan untuk nilai di luar domain tersebut.

---

## Kesimpulan & Saran

**Kesimpulan**
1. Sistem Pendukung Keputusan penentuan kualitas dan kelayakan air minum berbasis integrasi Fuzzy Mamdani (3 input, partisi segitiga simetris Ruspini, 27 aturan, Centroid analitik) dan KNN telah berhasil dibangun *from scratch* menggunakan Python dan antarmuka Streamlit 6 halaman.
2. Verifikasi antara perhitungan manual dan keluaran program pada sampel S4 ($z^* = 55.9524$) maupun kasus uji baru $Q^*$ ($z^* = 54.1667$, prediksi *Potable* pada $K = 3$) menghasilkan selisih absolut $0.0000$, dan seluruh 5 pengujian unit otomatis (`pytest`) lulus 100%.
3. Integrasi fitur `fuzzy_quality_score` pada Model B (4 fitur) secara konsisten mengungguli Model A (Baseline KNN 3 fitur) di seluruh nilai $K \in \lbrace 3, 5, 7, 9, 11 \rbrace$, dengan peningkatan akurasi +2.50% hingga +4.17% dan akurasi tertinggi 97.50% pada $K = 11$ (95.00% pada $K = 5$).
4. Pengurangan kesalahan klasifikasi dari 9 sampel menjadi 6 sampel pada $K = 5$ menunjukkan bahwa fitur hasil inferensi pakar Fuzzy Mamdani efektif memperkuat pemisahan kelas KNN di area perbatasan.

**Saran pengembangan**
1. Menambahkan parameter kualitas air lain seperti Chloramines, Solids, atau indikator mikrobiologis untuk memperkaya basis pengetahuan pakar.
2. Menerapkan optimasi parameter fungsi keanggotaan secara adaptif (misalnya Genetic Algorithm atau ANFIS) agar batas himpunan fuzzy semakin presisi.
3. Mengeksplorasi varian Fuzzy K-Nearest Neighbor (FKNN) berbobot jarak guna menghasilkan probabilitas keanggotaan kelas yang lebih halus.

---

## Referensi

1. Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory, 13*(1), 21-27. https://doi.org/10.1109/TIT.1967.1053964
2. Kadiwal, A. (2021). *Water Quality and Potability Dataset* [Data set]. Kaggle Repository. https://www.kaggle.com/datasets/adityakadiwal/water-potability
3. Keller, J. M., Gray, M. R., & Givens, J. A. (1985). A fuzzy K-nearest neighbor algorithm. *IEEE Transactions on Systems, Man, and Cybernetics, SMC-15*(4), 580-585. https://doi.org/10.1109/TSMC.1985.6313426
4. Kusumadewi, S., & Purnomo, H. (2010). *Aplikasi Logika Fuzzy untuk Pendukung Keputusan* (Edisi ke-2). Yogyakarta: Graha Ilmu.
5. Mamdani, E. H., & Assilian, S. (1975). An experiment in linguistic synthesis with a fuzzy logic controller. *International Journal of Man-Machine Studies, 7*(1), 1-13. https://doi.org/10.1016/S0020-7373(75)80002-2
6. Ross, T. J. (2016). *Fuzzy Logic with Engineering Applications* (4th ed.). Chichester: John Wiley & Sons.
7. Zadeh, L. A. (1965). Fuzzy sets. *Information and Control, 8*(3), 338-353. https://doi.org/10.1016/S0019-9958(65)90241-X

---

## Anggota Kelompok 1

Program Studi Informatika, FMIPA Universitas Udayana:

| No. | Nama Mahasiswa | NIM |
| :---: | :--- | :---: |
| 1 | Nathanael Adrian Wattimena | `2408561013` |
| 2 | I Wayan Arya Adi Guna | `2408561019` |
| 3 | Komang Dhika Artika Nurdi | `2408561055` |
| 4 | Kadek Phatra Adisuta Timonuli | `2408561076` |
| 5 | I Putu Maichail Ganio Wijaya | `2408561123` |

---
*© 2026 Kelompok 1, Teknologi Logika Fuzzy, Program Studi Informatika, FMIPA Universitas Udayana.*
