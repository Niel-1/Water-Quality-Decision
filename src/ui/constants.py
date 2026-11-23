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
    ("dashboard", "01", "Dashboard"),
    ("input", "02", "Input & Dataset"),
    ("whitebox", "03", "Step-by-Step Process"),
    ("results", "04", "Classification Results"),
    ("evaluation", "05", "Model Evaluation"),
    ("docs", "06", "Docs & Guide"),
]

DEFAULT_MANUAL_INPUT = {
    "ph": 5.25,
    "Hardness": 150.0,
    "Turbidity": 2.25,
    "k_neighbors": 3,
    "reference_mode": "manual_5",
}

REFERENCE_MODES = {
    "manual_5": "5 Manual Reference Samples (S1-S5, K<=5)",
    "kaggle_480": "Full Kaggle Train Set (480 Samples)",
}

SAMPLE_PRESETS = {
    "Sample Q* : Agak Asam & Jernih (pH 5.25, Hardness 150.0, Turbidity 2.250)": (5.25, 150.0, 2.250),
    "Sample S1 : Not Potable / Asam Sadah Keruh (pH 3.50, Hardness 240.0, Turbidity 4.750)": (3.50, 240.0, 4.750),
    "Sample S2 : Not Potable / Basa Sadah Keruh (pH 10.50, Hardness 240.0, Turbidity 4.750)": (10.50, 240.0, 4.750),
    "Sample S3 : Not Potable / Borderline (pH 7.00, Hardness 180.0, Turbidity 3.500)": (7.00, 180.0, 3.500),
    "Sample S4 : Potable / Layak Minum Ideal (pH 7.00, Hardness 120.0, Turbidity 2.250)": (7.00, 120.0, 2.250),
    "Sample S5 : Potable / Kualitas Sangat Baik (pH 7.00, Hardness 90.0, Turbidity 1.625)": (7.00, 90.0, 1.625),
    "Custom Input (Manual)": None,
}

TEAM_MEMBERS = [
    {
        "No": 1,
        "Nama Mahasiswa": "Nathanael Adrian Wattimena",
        "NIM": "2408561013",
        "Peran Utama": "Ketua Kelompok, Analisis Masalah & Laporan (BAB I-II)",
    },
    {
        "No": 2,
        "Nama Mahasiswa": "I Wayan Arya Adi Guna",
        "NIM": "2408561019",
        "Peran Utama": "Data Cleaning, Preprocessing & Eksplorasi Dataset",
    },
    {
        "No": 3,
        "Nama Mahasiswa": "Komang Dhika Artika Nurdi",
        "NIM": "2408561055",
        "Peran Utama": "Implementasi Fuzzy Mamdani & Perhitungan Manual",
    },
    {
        "No": 4,
        "Nama Mahasiswa": "Kadek Phatra Adisuta Timonuli",
        "NIM": "2408561076",
        "Peran Utama": "Implementasi KNN, Integrasi & Evaluasi Model",
    },
    {
        "No": 5,
        "Nama Mahasiswa": "I Putu Maichail Ganio Wijaya",
        "NIM": "2408561123",
        "Peran Utama": "Streamlit UI, Visualisasi Chart & Dokumentasi",
    },
]
