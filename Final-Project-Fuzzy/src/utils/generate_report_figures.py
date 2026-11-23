"""
Menghasilkan 5 gambar grafik/diagram berkualitas publikasi (200 DPI)
untuk Laporan Resmi Final Project TLF Kelompok 1 (Water Quality & Potability).
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.fuzzy_mamdani import MF_PARAMS, triangular_mf_array

OUT_DIR = PROJECT_ROOT / "docs" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams["axes.edgecolor"] = "#1f2937"
plt.rcParams["axes.linewidth"] = 1.0


def generate_gambar_3_1():
    """Gambar 3.1: 4-panel Fungsi Keanggotaan Segitiga Simetris Ruspini."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.2), dpi=200)
    fig.patch.set_facecolor("white")

    panels = [
        ("ph", "Variabel Input 1: pH (Tingkat Keasaman Air)", "Nilai pH", ["#c0392b", "#1e8449", "#2471a3"]),
        ("Hardness", "Variabel Input 2: Hardness (Kesadahan Air, mg/L)", "Hardness (mg/L)", ["#1e8449", "#d68910", "#c0392b"]),
        ("Turbidity", "Variabel Input 3: Turbidity (Kekeruhan Air, NTU)", "Turbidity (NTU)", ["#1e8449", "#d68910", "#c0392b"]),
        ("water_quality_score", "Variabel Output: water_quality_score (Skor Kualitas Air)", "Skor Kualitas Air (0–100)", ["#c0392b", "#d68910", "#1e8449"]),
    ]

    for ax, (var_key, title, xlabel, colors) in zip(axes.flat, panels):
        cfg = MF_PARAMS[var_key]
        lo, hi = cfg["domain"]
        xs = np.linspace(lo, hi, 400)
        for (set_name, (a, b, c)), col in zip(cfg["sets"].items(), colors):
            ys = triangular_mf_array(xs, a, b, c)
            ax.plot(xs, ys, label=f"{set_name} ({a:g}, {b:g}, {c:g})", color=col, linewidth=2.2)
            ax.fill_between(xs, 0, ys, color=col, alpha=0.09)
            # Annotate peak
            ax.scatter([b], [1.0], color=col, s=26, zorder=5)

        ax.set_title(title, fontsize=10.5, fontweight="bold", pad=8, color="#111827")
        ax.set_xlabel(xlabel, fontsize=9.5, color="#1f2937")
        ax.set_ylabel("Derajat Keanggotaan μ(x)", fontsize=9.5, color="#1f2937")
        ax.set_xlim(lo, hi)
        ax.set_ylim(-0.04, 1.15)
        ax.grid(True, linestyle="--", alpha=0.35, color="#9ca3af")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.01), ncol=3, fontsize=8.0, frameon=True, facecolor="white", edgecolor="#d1d5db")
        ax.tick_params(labelsize=8.8)

    fig.suptitle(
        "Kurva Fungsi Keanggotaan Segitiga Simetris Ruspini (Σμ = 1)\nSistem Inferensi Fuzzy Mamdani — Kualitas dan Kelayakan Air Minum",
        fontsize=12,
        fontweight="bold",
        y=0.98,
        color="#111827",
    )
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    out_path = OUT_DIR / "gambar_3_1_membership_functions.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] {out_path}")


def draw_box(ax, x, y, w, h, text, fc="#f8fafc", ec="#1e3a5f", tc="#111827", fontsize=8.8, bold=False, lw=1.4):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fontsize,
        fontweight="bold" if bold else "normal", color=tc, zorder=4, linespacing=1.3
    )


def draw_arrow(ax, x1, y1, x2, y2, label=None, lx=None, ly=None):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>,head_width=0.25,head_length=0.45", color="#1e3a5f", lw=1.4),
        zorder=2
    )
    if label:
        ax.text(
            lx if lx is not None else (x1 + x2) / 2,
            ly if ly is not None else (y1 + y2) / 2 + 0.08,
            label, ha="center", va="center", fontsize=8.0, color="#374151", style="italic"
        )


def generate_gambar_3_2():
    """Gambar 3.2: Diagram Arsitektur Pipeline Sistem Hibrida Fuzzy Mamdani + KNN."""
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    ax.text(6.0, 5.1, "Arsitektur Pipeline Sistem Pendukung Keputusan Hibrida Fuzzy Mamdani + KNN",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#111827")

    # Container 1: Input
    c1 = patches.FancyBboxPatch((0.2, 1.0), 2.1, 3.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor="#eff6ff", edgecolor="#1d4ed8", lw=1.3, linestyle="--", zorder=1)
    ax.add_patch(c1)
    ax.text(1.25, 4.35, "1. Input Fisik-Kimia", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#1e40af")
    draw_box(ax, 0.4, 3.35, 1.7, 0.65, "pH (X₁)\nDomain [0, 14]", fc="white", ec="#2563eb", fontsize=8.5)
    draw_box(ax, 0.4, 2.35, 1.7, 0.65, "Hardness (X₂)\n[60, 300] mg/L", fc="white", ec="#2563eb", fontsize=8.5)
    draw_box(ax, 0.4, 1.35, 1.7, 0.65, "Turbidity (X₃)\n[1, 6] NTU", fc="white", ec="#2563eb", fontsize=8.5)

    # Container 2: Tahap 1 Fuzzy Mamdani
    c2 = patches.FancyBboxPatch((2.7, 1.0), 3.2, 3.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor="#fefce8", edgecolor="#b45309", lw=1.3, linestyle="--", zorder=1)
    ax.add_patch(c2)
    ax.text(4.3, 4.35, "2. Tahap I: FIS Mamdani", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#92400e")
    draw_box(ax, 2.95, 3.55, 2.7, 0.52, "Fuzzifikasi Segitiga Ruspini (μ)", fc="white", ec="#d97706", fontsize=8.3)
    draw_box(ax, 2.95, 2.80, 2.7, 0.52, "27 Basis Aturan & Implikasi MIN", fc="white", ec="#d97706", fontsize=8.3)
    draw_box(ax, 2.95, 2.05, 2.7, 0.52, "Agregasi Antar-Aturan (MAX)", fc="white", ec="#d97706", fontsize=8.3)
    draw_box(ax, 2.95, 1.25, 2.7, 0.58, "Defuzzifikasi Centroid Analitik\n→ fuzzy_quality_score (Y)", fc="#fef3c7", ec="#b45309", fontsize=8.3, bold=True)
    draw_arrow(ax, 4.3, 3.55, 4.3, 3.32)
    draw_arrow(ax, 4.3, 2.80, 4.3, 2.57)
    draw_arrow(ax, 4.3, 2.05, 4.3, 1.83)

    # Container 3: Tahap 2 Feature Augmentation + KNN
    c3 = patches.FancyBboxPatch((6.35, 1.0), 3.15, 3.6, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor="#ecfdf5", edgecolor="#047857", lw=1.3, linestyle="--", zorder=1)
    ax.add_patch(c3)
    ax.text(7.925, 4.35, "3. Tahap II: KNN (4 Fitur)", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#065f46")
    draw_box(ax, 6.6, 3.45, 2.65, 0.62, "Pengayaan Vektor Fitur 4D\n[X₁, X₂, X₃, Y_fuzzy]", fc="white", ec="#059669", fontsize=8.3, bold=True)
    draw_box(ax, 6.6, 2.60, 2.65, 0.58, "Normalisasi Min-Max [0, 1]\n(Fit pada Data Latih)", fc="white", ec="#059669", fontsize=8.3)
    draw_box(ax, 6.6, 1.85, 2.65, 0.52, "Jarak Euclidean 4 Dimensi", fc="white", ec="#059669", fontsize=8.3)
    draw_box(ax, 6.6, 1.15, 2.65, 0.52, "Sorting & Majority Voting (K)", fc="white", ec="#059669", fontsize=8.3)
    draw_arrow(ax, 7.925, 3.45, 7.925, 3.18)
    draw_arrow(ax, 7.925, 2.60, 7.925, 2.37)
    draw_arrow(ax, 7.925, 1.85, 7.925, 1.67)

    # Container 4: Output
    c4 = patches.FancyBboxPatch((9.9, 1.4), 1.9, 2.8, boxstyle="round,pad=0.05,rounding_size=0.1",
                                facecolor="#f5f3ff", edgecolor="#6d28d9", lw=1.3, linestyle="--", zorder=1)
    ax.add_patch(c4)
    ax.text(10.85, 3.95, "4. Keputusan", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#5b21b6")
    draw_box(ax, 10.1, 2.85, 1.5, 0.78, "Potable (1)\nLayak Minum", fc="#dcfce7", ec="#15803d", tc="#14532d", fontsize=8.5, bold=True)
    draw_box(ax, 10.1, 1.70, 1.5, 0.78, "Not Potable (0)\nTidak Layak", fc="#fee2e2", ec="#b91c1c", tc="#7f1d1d", fontsize=8.5, bold=True)

    # Inter-container arrows
    draw_arrow(ax, 2.1, 3.68, 2.95, 3.81)
    draw_arrow(ax, 2.1, 2.68, 2.95, 3.68)
    draw_arrow(ax, 2.1, 1.68, 2.95, 3.58)

    # Bypass arrow X1,X2,X3 directly to 4D vector (bottom rail)
    ax.plot([1.25, 1.25, 6.12, 6.12, 6.6], [1.0, 0.48, 0.48, 3.85, 3.85], color="#1e3a5f", lw=1.4, zorder=2)
    draw_arrow(ax, 6.45, 3.85, 6.6, 3.85)
    ax.text(3.68, 0.22, "Fitur Asli [pH, Hardness, Turbidity] diteruskan langsung ke Vektor Fitur 4D",
            ha="center", va="center", fontsize=8.0, style="italic", color="#1e3a5f")

    # Y_fuzzy -> 4D vector
    ax.plot([5.65, 6.25, 6.25, 6.6], [1.54, 1.54, 3.62, 3.62], color="#b45309", lw=1.5, zorder=2)
    draw_arrow(ax, 6.45, 3.62, 6.6, 3.62)

    # KNN -> Decision
    draw_arrow(ax, 9.25, 1.41, 10.1, 2.09)
    draw_arrow(ax, 9.25, 1.41, 10.1, 3.24)

    out_path = OUT_DIR / "gambar_3_2_arsitektur_sistem.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] {out_path}")


def generate_gambar_3_3():
    """Gambar 3.3: Flowchart Alur Komputasi End-to-End Fuzzy Mamdani + KNN."""
    fig, ax = plt.subplots(figsize=(8.6, 10.6), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 11.2)
    ax.axis("off")

    ax.text(4.3, 10.85, "Flowchart Alur Komputasi End-to-End Algoritma Hibrida Fuzzy Mamdani + KNN",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color="#111827")

    steps = [
        (9.95, 0.55, "MULAI (Start)", "#1e3a5f", "#1e3a5f", "white", True),
        (9.00, 0.65, "Input Data Kualitas Air: pH (X₁), Hardness (X₂), Turbidity (X₃)\ndan Parameter Jumlah Tetangga K (Default K = 5)", "#eff6ff", "#1d4ed8", "#111827", False),
        (7.98, 0.68, "Tahap 1 — Fuzzifikasi: Hitung derajat keanggotaan μ(X₁), μ(X₂), μ(X₃)\nmenggunakan fungsi segitiga simetris Ruspini", "#fefce8", "#b45309", "#111827", False),
        (6.95, 0.68, "Tahap 2 & 3 — Evaluasi 27 Rule Base & Implikasi MIN:\nαₖ = min(μ_pH, μ_Hardness, μ_Turbidity) untuk setiap rule aktif (αₖ > 0)", "#fefce8", "#b45309", "#111827", False),
        (5.95, 0.65, "Tahap 4 — Agregasi (MAX): Gabungkan hasil clipping per kategori output\nμ_agg(Poor), μ_agg(Moderate), μ_agg(Good)", "#fefce8", "#b45309", "#111827", False),
        (4.92, 0.68, "Tahap 5 — Defuzzifikasi Centroid Analitik Per Segmen:\nz* = [∫ z · μ_agg(z) dz] / [∫ μ_agg(z) dz]  →  fuzzy_quality_score (Y)", "#fef3c7", "#92400e", "#111827", True),
        (3.90, 0.65, "Pengayaan Fitur (Feature Augmentation) & Normalisasi Min-Max [0, 1]:\nBentuk vektor 4D terstandarisasi [X₁', X₂', X₃', Y']", "#ecfdf5", "#047857", "#111827", False),
        (2.88, 0.65, "Hitung Jarak Euclidean 4D ke Seluruh Data Latih (N = 480):\nd(Q*, Sᵢ) = √[ Σ (q'ⱼ − s'ᵢⱼ)² ]  lalu urutkan jarak menaik", "#ecfdf5", "#047857", "#111827", False),
        (1.88, 0.65, "Ambil K Tetangga Terdekat & Lakukan Majority Voting:\nHitung suara kelas Potable (1) vs Not Potable (0)", "#ecfdf5", "#047857", "#111827", True),
    ]

    w = 6.8
    for i, (y, h, txt, fc, ec, tc, bld) in enumerate(steps):
        bw = 2.6 if i == 0 else w
        bx = (8.6 - bw) / 2
        draw_box(ax, bx, y, bw, h, txt, fc=fc, ec=ec, tc=tc, fontsize=8.8, bold=bld)
        if i < len(steps) - 1:
            ny, nh = steps[i + 1][0], steps[i + 1][1]
            draw_arrow(ax, 4.3, y, 4.3, ny + nh)

    # Decision outputs (left/right)
    draw_box(ax, 0.9, 0.85, 2.8, 0.65, "Prediksi: POTABLE (1)\n(Air Layak Minum)", fc="#dcfce7", ec="#15803d", tc="#14532d", fontsize=8.8, bold=True)
    draw_box(ax, 4.9, 0.85, 2.8, 0.65, "Prediksi: NOT POTABLE (0)\n(Air Tidak Layak Minum)", fc="#fee2e2", ec="#b91c1c", tc="#7f1d1d", fontsize=8.8, bold=True)
    draw_arrow(ax, 3.5, 1.88, 2.3, 1.50, label="Suara Potable ≥ Not Potable", lx=1.75, ly=1.73)
    draw_arrow(ax, 5.1, 1.88, 6.3, 1.50, label="Suara Not Potable > Potable", lx=6.85, ly=1.73)

    draw_box(ax, 3.0, 0.08, 2.6, 0.48, "SELESAI (End)", fc="#1e3a5f", ec="#1e3a5f", tc="white", fontsize=8.8, bold=True)
    draw_arrow(ax, 2.3, 0.85, 3.8, 0.56)
    draw_arrow(ax, 6.3, 0.85, 4.8, 0.56)

    out_path = OUT_DIR / "gambar_3_3_flowchart_algoritma.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] {out_path}")


def generate_gambar_4_1_and_4_2():
    """Gambar 4.1 (Perbandingan K) dan Gambar 4.2 (Confusion Matrix K=5) dari experiment_results.json."""
    with open(PROJECT_ROOT / "docs" / "experiment_results.json", encoding="utf-8") as f:
        data = json.load(f)

    eval_data = data["evaluation_stratified_ordered"]["results_by_k"]
    ks = [3, 5, 7, 9, 11]
    acc_a = [eval_data[str(k)]["model_a"]["accuracy"] * 100 for k in ks]
    acc_b = [eval_data[str(k)]["model_b"]["accuracy"] * 100 for k in ks]
    f1_a = [eval_data[str(k)]["model_a"]["f1_macro"] * 100 for k in ks]
    f1_b = [eval_data[str(k)]["model_b"]["f1_macro"] * 100 for k in ks]

    # Gambar 4.1: Accuracy & F1-Score side-by-side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4), dpi=200)
    fig.patch.set_facecolor("white")

    x = np.arange(len(ks))
    width = 0.35

    bars1a = ax1.bar(x - width / 2, acc_a, width, label="Model A: Baseline KNN (3 Fitur)", color="#64748b", edgecolor="#1f2937", linewidth=0.8)
    bars1b = ax1.bar(x + width / 2, acc_b, width, label="Model B: Fuzzy-Enhanced KNN (4 Fitur)", color="#0f766e", edgecolor="#1f2937", linewidth=0.8)
    ax1.set_title("Perbandingan Akurasi (%) pada Berbagai Nilai K", fontsize=10.5, fontweight="bold", pad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"K = {k}" for k in ks], fontsize=9.2)
    ax1.set_ylabel("Akurasi (%)", fontsize=9.5)
    ax1.set_ylim(85, 101)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.legend(loc="lower right", fontsize=8.3, frameon=True)
    for bar in list(bars1a) + list(bars1b):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.35, f"{h:.2f}%", ha="center", va="bottom", fontsize=7.6, fontweight="bold")

    bars2a = ax2.bar(x - width / 2, f1_a, width, label="Model A: Baseline KNN (3 Fitur)", color="#64748b", edgecolor="#1f2937", linewidth=0.8)
    bars2b = ax2.bar(x + width / 2, f1_b, width, label="Model B: Fuzzy-Enhanced KNN (4 Fitur)", color="#1d4ed8", edgecolor="#1f2937", linewidth=0.8)
    ax2.set_title("Perbandingan Macro F1-Score (%) pada Berbagai Nilai K", fontsize=10.5, fontweight="bold", pad=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"K = {k}" for k in ks], fontsize=9.2)
    ax2.set_ylabel("Macro F1-Score (%)", fontsize=9.5)
    ax2.set_ylim(85, 101)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.legend(loc="lower right", fontsize=8.3, frameon=True)
    for bar in list(bars2a) + list(bars2b):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.35, f"{h:.2f}%", ha="center", va="bottom", fontsize=7.6, fontweight="bold")

    fig.suptitle("Evaluasi Head-to-Head Model A vs Model B pada 120 Data Uji (Split 80:20 Terstratifikasi)",
                 fontsize=11.5, fontweight="bold", y=1.01)
    plt.tight_layout()
    out_41 = OUT_DIR / "gambar_4_1_perbandingan_model_k.png"
    fig.savefig(out_41, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] {out_41}")

    # Gambar 4.2: Confusion Matrices at K=5
    cm_a = np.array(eval_data["5"]["model_a"]["confusion_matrix"])
    cm_b = np.array(eval_data["5"]["model_b"]["confusion_matrix"])
    labels = ["Not Potable (0)", "Potable (1)"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=200)
    fig.patch.set_facecolor("white")

    for ax, cm, title, cmap in [
        (ax1, cm_a, "Model A: Baseline KNN (3 Fitur, K = 5)\nAkurasi = 92,50% | Total Error = 9 Sampel", "Blues"),
        (ax2, cm_b, "Model B: Fuzzy-Enhanced KNN (4 Fitur, K = 5)\nAkurasi = 95,00% | Total Error = 6 Sampel", "Greens"),
    ]:
        im = ax.imshow(cm, cmap=cmap, vmin=0, vmax=62)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_yticklabels(labels, fontsize=9)
        ax.set_xlabel("Label Prediksi", fontsize=9.5, fontweight="bold")
        ax.set_ylabel("Label Aktual", fontsize=9.5, fontweight="bold")
        ax.set_title(title, fontsize=9.8, fontweight="bold", pad=10)
        for r in range(2):
            for c in range(2):
                val = cm[r, c]
                tag = ["TN", "FP", "FN", "TP"][r * 2 + c]
                txt_col = "white" if val > 30 else "#111827"
                ax.text(c, r, f"{val}\n({tag})", ha="center", va="center", color=txt_col, fontsize=12, fontweight="bold")

    fig.suptitle("Perbandingan Matriks Konfusi (Confusion Matrix) pada 120 Data Uji (K = 5)",
                 fontsize=11.5, fontweight="bold", y=1.02)
    plt.tight_layout()
    out_42 = OUT_DIR / "gambar_4_2_confusion_matrix.png"
    fig.savefig(out_42, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[OK] {out_42}")


if __name__ == "__main__":
    generate_gambar_3_1()
    generate_gambar_3_2()
    generate_gambar_3_3()
    generate_gambar_4_1_and_4_2()
    print("[DONE] Seluruh 5 gambar laporan selesai dibuat di docs/figures/")
