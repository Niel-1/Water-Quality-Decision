"""Design tokens, navigation metadata, presets, and team constants."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CLEAN_CSV_PATH = BASE_DIR / "data" / "processed" / "water_potability_clean.csv"
MANUAL_CSV_PATH = BASE_DIR / "data" / "processed" / "manual_calc_sample.csv"

# Core palette tokens (Bathymetric Hydrographic Atlas)
PALETTE = {
    "bg_canvas": "#0d111a",
    "bg_rail": "#090c14",
    "bg_surface": "#131a28",
    "bg_recessed": "#0f1522",
    "bg_hover": "#1a2336",
    "border": "#233047",
    "border_subtle": "#1c2638",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#8192ac",
    "cobalt": "#3b82f6",
    "cobalt_bright": "#60a5fa",
    "cobalt_surface": "#172554",
    "potable": "#10b981",
    "potable_bright": "#34d399",
    "moderate": "#eab308",
    "moderate_bright": "#fbbf24",
    "poor": "#f43f5e",
    "poor_bright": "#fb7185",
    "slate_series": "#64748b",
}

POTABILITY_COLOR_MAP = {
    "Potable": PALETTE["potable"],
    "Not Potable": PALETTE["poor"],
}

QUALITY_COLOR_MAP = {
    "Good": PALETTE["potable"],
    "Moderate": PALETTE["moderate"],
    "Poor": PALETTE["poor"],
}

MF_COLOR_MAP = {
    "Acidic": PALETTE["poor"],
    "Neutral": PALETTE["cobalt_bright"],
    "Alkaline": PALETTE["moderate"],
    "Soft": PALETTE["potable"],
    "Moderate": PALETTE["moderate"],
    "Hard": PALETTE["poor"],
    "Clear": PALETTE["potable"],
    "Turbid": PALETTE["poor"],
    "Poor": PALETTE["poor"],
    "Good": PALETTE["potable"],
}

PLOTLY_FONT_FAMILY = "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
PLOTLY_MONO_FAMILY = "JetBrains Mono, ui-monospace, SFMono-Regular, monospace"

NAV_PAGES = [
    ("dashboard", "01", "Halaman Utama"),
    ("input", "02", "Input & Eksplorasi Dataset"),
    ("whitebox", "03", "Proses White-Box"),
    ("results", "04", "Hasil & Klasifikasi"),
    ("evaluation", "05", "Evaluasi Model A vs B"),
    ("docs", "06", "Informasi & Panduan"),
]

DEFAULT_MANUAL_INPUT = {
    "ph": 5.25,
    "Hardness": 150.0,
    "Turbidity": 2.25,
    "k_neighbors": 3,
    "reference_mode": "manual_5",
}

REFERENCE_MODES = {
    "manual_5": "5 Sampel Referensi Ringkas (S1-S5, K<=5)",
    "kaggle_480": "Dataset Latih Penuh Kaggle (480 Data Latih)",
}

SAMPLE_PRESETS = {
    "Sampel Uji Q* : Air Agak Asam & Jernih (pH 5.25, Hardness 150.0, Turbidity 2.250)": (5.25, 150.0, 2.250),
    "Sampel S1 : Not Potable / Asam Sadah Keruh (pH 3.50, Hardness 240.0, Turbidity 4.750)": (3.50, 240.0, 4.750),
    "Sampel S2 : Not Potable / Basa Sadah Keruh (pH 10.50, Hardness 240.0, Turbidity 4.750)": (10.50, 240.0, 4.750),
    "Sampel S3 : Not Potable / Ambang Transisi (pH 7.00, Hardness 180.0, Turbidity 3.500)": (7.00, 180.0, 3.500),
    "Sampel S4 : Potable / Layak Minum Ideal (pH 7.00, Hardness 120.0, Turbidity 2.250)": (7.00, 120.0, 2.250),
    "Sampel S5 : Potable / Kualitas Sangat Baik (pH 7.00, Hardness 90.0, Turbidity 1.625)": (7.00, 90.0, 1.625),
    "Kustomisasi Bebas (Input Manual)": None,
}

TEAM_MEMBERS = [
    {
        "No": 1,
        "Nama Mahasiswa": "Nathanael Adrian Wattimena",
        "NIM": "2408561013",
        "Peran Utama": "Koordinator, Analisis Masalah & Standar Kualitas Air (BAB I-II)",
    },
    {
        "No": 2,
        "Nama Mahasiswa": "I Wayan Arya Adi Guna",
        "NIM": "2408561019",
        "Peran Utama": "Dataset Engineer, Pembersihan & Eksplorasi Kaggle Water Potability",
    },
    {
        "No": 3,
        "Nama Mahasiswa": "Komang Dhika Artika Nurdi",
        "NIM": "2408561055",
        "Peran Utama": "Arsitek Modul Fuzzy Mamdani & Perhitungan Manual Analitik",
    },
    {
        "No": 4,
        "Nama Mahasiswa": "Kadek Phatra Adisuta Timonuli",
        "NIM": "2408561076",
        "Peran Utama": "Arsitek Modul KNN, Integrasi & Evaluasi Model A vs Model B",
    },
    {
        "No": 5,
        "Nama Mahasiswa": "I Putu Maichail Ganio Wijaya",
        "NIM": "2408561123",
        "Peran Utama": "Pengembang GUI Streamlit, Visualisasi & Dokumentasi Sistem",
    },
]
