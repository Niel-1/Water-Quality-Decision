# Hasil Eksperimen & Perhitungan Manual Presisi (Untuk Laporan TLF)

**Judul Proyek:** Water Quality & Potability Decision Support System menggunakan Kombinasi Metode Fuzzy Mamdani dan K-Nearest Neighbor (KNN)  
**Kelompok 1 - Teknologi Logika Fuzzy (Informatika Universitas Udayana):**
1. Nathanael Adrian Wattimena (2408561013)
2. I Wayan Arya Adi Guna (2408561019)
3. Komang Dhika Artika Nurdi (2408561055)
4. Kadek Phatra Adisuta Timonuli (2408561076)
5. I Putu Maichail Ganio Wijaya (2408561123)

---

## 1. Statistik Dataset Bersih (`water_potability_clean.csv`)
- **Sumber Dataset Publik (100% Bahasa Inggris):** Kaggle — *Water Quality and Potability* (`adityakadiwal/water-potability`, `data/raw/water_potability.csv`, 3.276 baris, 10 kolom bahasa Inggris).
- **Jumlah Total Baris Pengamatan Bersih:** `600` baris
- **Distribusi Kelas Target (`potability_label`):** `Not Potable (0)` = 300, `Potable (1)` = 300 (Seimbang 1:1)

### Tabel Statistik Deskriptif Variabel Numerik
| Variabel | Satuan | Min | Q1 (25%) | Median (50%) | Mean | Q3 (75%) | Max | Std Dev |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `ph` | pH (0-14) | 1.4318 | 6.0696 | 7.0393 | 7.1165 | 8.0883 | 13.3499 | 1.7151 |
| `Hardness` | mg/L | 73.4922 | 175.6315 | 197.2792 | 195.2735 | 217.4722 | 286.5680 | 34.0901 |
| `Turbidity` | NTU | 1.8444 | 3.4430 | 3.9646 | 3.9713 | 4.5113 | 5.9568 | 0.7570 |
| `Solids` | ppm (mg/L) | 1372.0900 | 16134.7500 | 21384.6400 | 22237.8212 | 27125.6475 | 55334.7000 | 8482.9323 |
| `Chloramines` | ppm (mg/L) | 2.4586 | 6.2837 | 7.3009 | 7.2088 | 8.1549 | 13.1270 | 1.6174 |
| `Conductivity` | μS/cm | 201.6200 | 365.6750 | 424.3900 | 424.4471 | 479.5575 | 753.3400 | 79.6734 |
| `fuzzy_quality_score` | Skor (0-100) | 20.3883 | 44.3975 | 47.2159 | 46.3661 | 49.2897 | 60.0580 | 4.8023 |

---

## 2. Desain Fungsi Keanggotaan & 27 Rule Base Fuzzy Mamdani

### 2.1 Parameter Fungsi Keanggotaan Segitiga Simetris Ruspini $(a, b, c)$
- **Variabel Input 1 (`ph`, $X_1$, Tingkat Keasaman Air, Domain $[0, 14]$):**
  - `Acidic` (Asam): Segitiga $(0, 0, 7)$
  - `Neutral` (Netral / Ideal WHO): Segitiga $(0, 7, 14)$
  - `Alkaline` (Basa): Segitiga $(7, 14, 14)$
- **Variabel Input 2 (`Hardness`, $X_2$, Kesadahan Air dalam mg/L, Domain $[60, 300]$):**
  - `Soft` (Lunak): Segitiga $(60, 60, 180)$
  - `Moderate` (Sedang / Ideal): Segitiga $(60, 180, 300)$
  - `Hard` (Sadah Tinggi): Segitiga $(180, 300, 300)$
- **Variabel Input 3 (`Turbidity`, $X_3$, Kekeruhan Air dalam NTU, Domain $[1, 6]$):**
  - `Clear` (Jernih): Segitiga $(1.0, 1.0, 3.5)$
  - `Moderate` (Agak Keruh): Segitiga $(1.0, 3.5, 6.0)$
  - `Turbid` (Keruh): Segitiga $(3.5, 6.0, 6.0)$
- **Variabel Output (`water_quality_score`, $Y$, Skor Kualitas Air Fuzzy, Domain $[0, 100]$):**
  - `Poor` (Buruk): Segitiga $(0, 0, 50)$
  - `Moderate` (Sedang): Segitiga $(0, 50, 100)$
  - `Good` (Baik / Layak): Segitiga $(50, 100, 100)$

### 2.2 Tabel Lengkap 27 Aturan Fuzzy Mamdani ($3 \times 3 \times 3$)
| Kode | IF pH ($X_1$) | AND Hardness ($X_2$) | AND Turbidity ($X_3$) | THEN Water Quality Score ($Y$) |
| :---: | :---: | :---: | :---: | :---: |
| **R01** | Acidic | Soft | Clear | **Moderate** |
| **R02** | Acidic | Soft | Moderate | **Moderate** |
| **R03** | Acidic | Soft | Turbid | **Poor** |
| **R04** | Acidic | Moderate | Clear | **Moderate** |
| **R05** | Acidic | Moderate | Moderate | **Poor** |
| **R06** | Acidic | Moderate | Turbid | **Poor** |
| **R07** | Acidic | Hard | Clear | **Poor** |
| **R08** | Acidic | Hard | Moderate | **Poor** |
| **R09** | Acidic | Hard | Turbid | **Poor** |
| **R10** | Neutral | Soft | Clear | **Good** |
| **R11** | Neutral | Soft | Moderate | **Good** |
| **R12** | Neutral | Soft | Turbid | **Moderate** |
| **R13** | Neutral | Moderate | Clear | **Good** |
| **R14** | Neutral | Moderate | Moderate | **Moderate** |
| **R15** | Neutral | Moderate | Turbid | **Poor** |
| **R16** | Neutral | Hard | Clear | **Moderate** |
| **R17** | Neutral | Hard | Moderate | **Poor** |
| **R18** | Neutral | Hard | Turbid | **Poor** |
| **R19** | Alkaline | Soft | Clear | **Moderate** |
| **R20** | Alkaline | Soft | Moderate | **Moderate** |
| **R21** | Alkaline | Soft | Turbid | **Poor** |
| **R22** | Alkaline | Moderate | Clear | **Moderate** |
| **R23** | Alkaline | Moderate | Moderate | **Poor** |
| **R24** | Alkaline | Moderate | Turbid | **Poor** |
| **R25** | Alkaline | Hard | Clear | **Poor** |
| **R26** | Alkaline | Hard | Moderate | **Poor** |
| **R27** | Alkaline | Hard | Turbid | **Poor** |

---

## 3. Contoh Perhitungan Manual Langkah demi Langkah (Selisih 0 / 100% Identik)

### 3.1 Tabel 5 Sampel Referensi Perhitungan Manual (`manual_calc_sample.csv`)
| Kode | Sample ID | pH ($X_1$) | Hardness ($X_2$) | Turbidity ($X_3$) | Fuzzy Quality Score ($Y$) | Solids (ppm) | Chloramines (ppm) | Kelas Kelayakan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **S1** | `WQP-M01` | 3.50 | 240.0 mg/L | 4.750 NTU | **44.0476** | 28450.0 | 8.20 | **Not Potable** |
| **S2** | `WQP-M02` | 10.50 | 240.0 mg/L | 4.750 NTU | **44.0476** | 26120.0 | 7.85 | **Not Potable** |
| **S3** | `WQP-M03` | 7.00 | 180.0 mg/L | 3.500 NTU | **50.0000** | 21500.0 | 7.10 | **Not Potable** |
| **S4** | `WQP-M04` | 7.00 | 120.0 mg/L | 2.250 NTU | **55.9524** | 16800.0 | 6.80 | **Potable** |
| **S5** | `WQP-M05` | 7.00 | 90.0 mg/L | 1.625 NTU | **64.6739** | 14200.0 | 6.50 | **Potable** |

### 3.2 Perhitungan Manual Fuzzy Mamdani Kasus 1: Sampel `S4` ($X_1 = 7.00$, $X_2 = 120.0\text{ mg/L}$, $X_3 = 2.25\text{ NTU}$)

#### Tahap 1: Fuzzifikasi Input
1. **pH ($X_1 = 7.00$):**
   - $\mu_{\text{Acidic}}(7.00) = 0.0000$ (karena $7.00 \ge 7.00$)
   - $\mu_{\text{Neutral}}(7.00) = 1.0000$ (tepat di titik puncak $b = 7.00$)
   - $\mu_{\text{Alkaline}}(7.00) = 0.0000$ (karena $7.00 \le 7.00$)
2. **Hardness ($X_2 = 120.0$ mg/L):**
   - $\mu_{\text{Soft}}(120.0) = \frac{180 - 120}{180 - 60} = \frac{60}{120} = 0.5000$
   - $\mu_{\text{Moderate}}(120.0) = \frac{120 - 60}{180 - 60} = \frac{60}{120} = 0.5000$
   - $\mu_{\text{Hard}}(120.0) = 0.0000$ (karena $120.0 \le 180.0$)
3. **Turbidity ($X_3 = 2.25$ NTU):**
   - $\mu_{\text{Clear}}(2.25) = \frac{3.50 - 2.25}{3.50 - 1.00} = \frac{1.25}{2.50} = 0.5000$
   - $\mu_{\text{Moderate}}(2.25) = \frac{2.25 - 1.00}{3.50 - 1.00} = \frac{1.25}{2.50} = 0.5000$
   - $\mu_{\text{Turbid}}(2.25) = 0.0000$ (karena $2.25 \le 3.50$)

#### Tahap 2 & 3: Evaluasi Rule Aktif (AND = MIN) & Implikasi (MIN)
| Rule | Kondisi Anteseden ($X_1, X_2, X_3$) | $\mu(X_1)$ | $\mu(X_2)$ | $\mu(X_3)$ | $\alpha = \min(\mu_1, \mu_2, \mu_3)$ | Output Konsekuen ($Y$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **R10** | (Neutral, Soft, Clear) | 1.0000 | 0.5000 | 0.5000 | **0.5000** | **Good** |
| **R11** | (Neutral, Soft, Moderate) | 1.0000 | 0.5000 | 0.5000 | **0.5000** | **Good** |
| **R13** | (Neutral, Moderate, Clear) | 1.0000 | 0.5000 | 0.5000 | **0.5000** | **Good** |
| **R14** | (Neutral, Moderate, Moderate) | 1.0000 | 0.5000 | 0.5000 | **0.5000** | **Moderate** |

#### Tahap 4: Agregasi Antar-Aturan (MAX)
- $\alpha_{\text{Poor}} = 0.0000$
- $\alpha_{\text{Moderate}} = 0.5000$ (dari R14)
- $\alpha_{\text{Good}} = 0.5000$ (dari R10, R11, R13)

#### Tahap 5: Defuzzifikasi Centroid Analitik Per Segmen
| Segmen | Batas $z \in [z_0, z_1]$ | Persamaan Kurva $\mu_{\text{agg}}(z)$ | Luas Segmen $A_i = \int_{z_0}^{z_1} \mu(z) dz$ | Momen Segmen $M_i = \int_{z_0}^{z_1} z \cdot \mu(z) dz$ |
| :---: | :---: | :--- | :---: | :---: |
| **Segmen 1** | $[0.00, 25.00]$ | `μ(z) = 0.0200z` | `6.2500` | `104.1667` |
| **Segmen 2** | $[25.00, 100.00]$ | `μ(z) = 0.5000` | `37.5000` | `2343.7500` |

- **Total Luas ($\sum A_i$):** `43.7500`
- **Total Momen ($\sum M_i$):** `2447.9167`
- **Titik Pusat Massa (Centroid $z^*$):**
  $$z^* = \frac{2447.9167}{43.7500} = \frac{1175}{21} = 55.9524$$

---

### 3.3 Perhitungan Manual Kasus Uji Baru $Q^*$ ($X_1 = 5.25$, $X_2 = 150.0\text{ mg/L}$, $X_3 = 2.25\text{ NTU}$) dari Fuzzifikasi hingga Klasifikasi KNN

#### A. Tahap Fuzzy Mamdani untuk Kasus Uji $Q^*$
1. **Fuzzifikasi Input:**
   - $X_1 = 5.25 \implies \mu_{\text{Acidic}} = \frac{7.00 - 5.25}{7.00} = 0.2500, \; \mu_{\text{Neutral}} = \frac{5.25 - 0}{7.00} = 0.7500, \; \mu_{\text{Alkaline}} = 0.0000$
   - $X_2 = 150.0 \implies \mu_{\text{Soft}} = \frac{180 - 150}{120} = 0.2500, \; \mu_{\text{Moderate}} = \frac{150 - 60}{120} = 0.7500, \; \mu_{\text{Hard}} = 0.0000$
   - $X_3 = 2.25 \implies \mu_{\text{Clear}} = \frac{3.50 - 2.25}{2.50} = 0.5000, \; \mu_{\text{Moderate}} = \frac{2.25 - 1.00}{2.50} = 0.5000, \; \mu_{\text{Turbid}} = 0.0000$

2. **Evaluasi Rule Aktif & Agregasi:**
| Rule | Kondisi Anteseden ($X_1, X_2, X_3$) | $\mu(X_1)$ | $\mu(X_2)$ | $\mu(X_3)$ | $\alpha = \min(\mu_1, \mu_2, \mu_3)$ | Output ($Y$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **R01** | (Acidic, Soft, Clear) | 0.2500 | 0.2500 | 0.5000 | **0.2500** | **Moderate** |
| **R02** | (Acidic, Soft, Moderate) | 0.2500 | 0.2500 | 0.5000 | **0.2500** | **Moderate** |
| **R04** | (Acidic, Moderate, Clear) | 0.2500 | 0.7500 | 0.5000 | **0.2500** | **Moderate** |
| **R05** | (Acidic, Moderate, Moderate) | 0.2500 | 0.7500 | 0.5000 | **0.2500** | **Poor** |
| **R10** | (Neutral, Soft, Clear) | 0.7500 | 0.2500 | 0.5000 | **0.2500** | **Good** |
| **R11** | (Neutral, Soft, Moderate) | 0.7500 | 0.2500 | 0.5000 | **0.2500** | **Good** |
| **R13** | (Neutral, Moderate, Clear) | 0.7500 | 0.7500 | 0.5000 | **0.5000** | **Good** |
| **R14** | (Neutral, Moderate, Moderate) | 0.7500 | 0.7500 | 0.5000 | **0.5000** | **Moderate** |

- **Hasil Agregasi (MAX):** $\alpha_{\text{Poor}} = 0.2500$, $\alpha_{\text{Moderate}} = 0.5000$, $\alpha_{\text{Good}} = 0.5000$

3. **Defuzzifikasi Centroid Analitik Per Segmen untuk $Q^*$:**
| Segmen | Batas $z \in [z_0, z_1]$ | Persamaan Kurva $\mu_{\text{agg}}(z)$ | Luas Segmen $A_i$ | Momen Segmen $M_i$ |
| :---: | :---: | :--- | :---: | :---: |
| **Segmen 1** | $[0.00, 12.50]$ | `μ(z) = 0.2500` | `3.1250` | `19.5312` |
| **Segmen 2** | $[12.50, 25.00]$ | `μ(z) = 0.0200z` | `4.6875` | `91.1458` |
| **Segmen 3** | $[25.00, 100.00]$ | `μ(z) = 0.5000` | `37.5000` | `2343.7500` |

- **Total Luas ($\sum A_i$):** `45.3125`
- **Total Momen ($\sum M_i$):** `2454.4271`
- **Skor Kualitas Air Fuzzy ($z^*$):** `54.1667` ($\frac{650}{12} = 54.1667$)

#### B. Tahap Perhitungan Jarak Euclidean KNN ($K = 3$) terhadap 5 Sampel Referensi (`S1` s.d. `S5`)
- **Vektor Fitur Mentah $Q^*$ (4 Fitur Model B):** `[5.25, 150.0, 2.25, 54.1667]`
- **Batas Minimum Data Referensi (`S1`..`S5`):** `[3.5, 90.0, 1.625, 44.0476]`
- **Batas Maksimum Data Referensi (`S1`..`S5`):** `[10.5, 240.0, 4.75, 64.6739]`
- **Rentang (Max - Min):** `[7.0, 150.0, 3.125, 20.6263]`
- **Vektor Fitur Ternormalisasi Min-Max $Q^*$:** `[0.25, 0.4, 0.2, 0.4906]`

| Peringkat | Sampel | Fitur Mentah $[X_1, X_2, X_3, Y]$ | Fitur Ternormalisasi $[X'_1, X'_2, X'_3, Y']$ | Selisih Kuadrat $\sum (x'_{qj} - x'_{ij})^2$ | Jarak Euclidean $d(Q^*, S_i)$ | Kelas |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **S4** | `[7.0, 120.0, 2.25, 55.9524]` | `[0.5, 0.2, 0.2, 0.5772]` | `0.1100` | **0.3317** | **Potable** |
| **2** | **S3** | `[7.0, 180.0, 3.5, 50.0]` | `[0.5, 0.6, 0.6, 0.2886]` | `0.3033` | **0.5507** | **Not Potable** |
| **3** | **S5** | `[7.0, 90.0, 1.625, 64.6739]` | `[0.5, 0.0, 0.0, 1.0]` | `0.5220` | **0.7225** | **Potable** |
| **4** | **S1** | `[3.5, 240.0, 4.75, 44.0476]` | `[0.0, 1.0, 1.0, 0.0]` | `1.3032` | **1.1416** | **Not Potable** |
| **5** | **S2** | `[10.5, 240.0, 4.75, 44.0476]` | `[1.0, 1.0, 1.0, 0.0]` | `1.8032` | **1.3428** | **Not Potable** |

- **3 Tetangga Terdekat ($K=3$):** `['S4 (Potable)', 'S3 (Not Potable)', 'S5 (Potable)']`
- **Hasil Voting Mayoritas ($K=3$):** `{'Not Potable': 1, 'Potable': 2}` $\implies$ **Kelas Prediksi = `Potable`**

---

## 4. Hasil Evaluasi Eksperimen Model A (Baseline KNN) vs Model B (Fuzzy-Enhanced KNN)

- **Strategi Pembagian Data:** Stratified Ordered Split bebas kebocoran data (*leakage-free*), 80% Data Latih (`480` baris) dan 20% Data Uji (`120` baris).
- **Distribusi Kelas Data Latih (480 baris):** `{'Potable': 240, 'Not Potable': 240}`
- **Distribusi Kelas Data Uji (120 baris):** `{'Potable': 60, 'Not Potable': 60}`
- **Metode Normalisasi:** Min-Max Scaling (`fit` hanya pada 480 data latih, `transform` pada 120 data uji).

### 4.1 Tabel Perbandingan Metrik Evaluasi pada Berbagai Nilai $K$ ($K = 3, 5, 7, 9, 11$)
| Nilai $K$ | Acc Model A (%) | Acc Model B (%) | $\Delta$ Acc (%) | Macro-F1 Model A (%) | Macro-F1 Model B (%) | Weighted-F1 Model A (%) | Weighted-F1 Model B (%) | Kesesuaian Scratch vs Sklearn |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **K = 3** | 92.50% | **95.83%** | **+3.33%** | 92.50% | **95.83%** | 92.50% | **95.83%** | 100.0% |
| **K = 5** | 92.50% | **95.00%** | **+2.50%** | 92.50% | **95.00%** | 92.50% | **95.00%** | 100.0% |
| **K = 7** | 93.33% | **95.83%** | **+2.50%** | 93.33% | **95.83%** | 93.33% | **95.83%** | 100.0% |
| **K = 9** | 91.67% | **95.83%** | **+4.17%** | 91.66% | **95.83%** | 91.66% | **95.83%** | 100.0% |
| **K = 11** | 93.33% | **97.50%** | **+4.17%** | 93.33% | **97.50%** | 93.33% | **97.50%** | 100.0% |

### 4.2 Rincian Metrik Per Kelas pada $K = 5$
| Kelas Kelayakan Air | Support (Data Uji) | Precision Model A | Precision Model B | Recall Model A | Recall Model B | F1-Score Model A | F1-Score Model B |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Not Potable** | 60 | 90.48% | **93.55%** | 95.00% | **96.67%** | 92.68% | **95.08%** |
| **Potable** | 60 | 94.74% | **96.55%** | 90.00% | **93.33%** | 92.31% | **94.92%** |

### 4.3 Matriks Konfusi (Confusion Matrix) pada $K = 5$ (120 Data Uji)

#### Model A (Baseline KNN - 3 Fitur `[ph, Hardness, Turbidity]`):
| Aktual \ Prediksi | Prediksi: Not Potable | Prediksi: Potable |
| :--- | :---: | :---: |
| **Aktual: Not Potable** | **57** | 3 |
| **Aktual: Potable** | 6 | **54** |

#### Model B (Fuzzy-Enhanced KNN - 4 Fitur `[ph, Hardness, Turbidity, fuzzy_quality_score]`):
| Aktual \ Prediksi | Prediksi: Not Potable | Prediksi: Potable |
| :--- | :---: | :---: |
| **Aktual: Not Potable** | **58** | 2 |
| **Aktual: Potable** | 4 | **56** |
