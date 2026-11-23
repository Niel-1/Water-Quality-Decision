"""Cohesive dark-slate Plotly chart builders for the Water Quality & Potability DSS."""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.fuzzy_mamdani import MF_PARAMS, triangular_mf_array
from src.knn_model import CLASS_ORDER
from src.ui.constants import (
    MF_COLOR_MAP,
    PALETTE,
    PLOTLY_FONT_FAMILY,
    PLOTLY_MONO_FAMILY,
    POTABILITY_COLOR_MAP,
)


def apply_atlas_layout(
    fig: go.Figure,
    title: str,
    height: int = 330,
    show_legend: bool = True,
    xaxis_title: Optional[str] = None,
    yaxis_title: Optional[str] = None,
) -> go.Figure:
    """Apply consistent dark-slate typography, gridlines, hover styling, and margins."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family=PLOTLY_FONT_FAMILY, size=13, color=PALETTE["text_primary"]),
            x=0.01,
            xanchor="left",
            y=0.96,
        ),
        font=dict(family=PLOTLY_FONT_FAMILY, size=12, color=PALETTE["text_secondary"]),
        height=height,
        margin=dict(l=48, r=18, t=52, b=46),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PALETTE["bg_recessed"],
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color=PALETTE["text_secondary"]),
            title_text="",
        ),
        hoverlabel=dict(
            bgcolor=PALETTE["bg_rail"],
            bordercolor=PALETTE["cobalt"],
            font=dict(family=PLOTLY_MONO_FAMILY, size=12, color=PALETTE["text_primary"]),
        ),
    )
    fig.update_xaxes(
        title_text=xaxis_title,
        title_font=dict(size=12, color=PALETTE["text_secondary"]),
        tickfont=dict(family=PLOTLY_MONO_FAMILY, size=11, color=PALETTE["text_secondary"]),
        gridcolor="rgba(148, 163, 184, 0.12)",
        zerolinecolor="rgba(148, 163, 184, 0.22)",
        linecolor=PALETTE["border"],
        showline=True,
    )
    fig.update_yaxes(
        title_text=yaxis_title,
        title_font=dict(size=12, color=PALETTE["text_secondary"]),
        tickfont=dict(family=PLOTLY_MONO_FAMILY, size=11, color=PALETTE["text_secondary"]),
        gridcolor="rgba(148, 163, 184, 0.12)",
        zerolinecolor="rgba(148, 163, 184, 0.22)",
        linecolor=PALETTE["border"],
        showline=True,
    )
    return fig


def plot_class_distribution(df: pd.DataFrame) -> go.Figure:
    """Bar chart of Potable vs Not Potable counts on the active dataset."""
    cls_counts = (
        df["potability_label"].value_counts().reindex(CLASS_ORDER, fill_value=0).reset_index()
    )
    cls_counts.columns = ["Kelas Kelayakan Air", "Jumlah Sampel"]

    fig = px.bar(
        cls_counts,
        x="Kelas Kelayakan Air",
        y="Jumlah Sampel",
        color="Kelas Kelayakan Air",
        color_discrete_map=POTABILITY_COLOR_MAP,
        text="Jumlah Sampel",
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        textfont=dict(family=PLOTLY_MONO_FAMILY, size=12, color=PALETTE["text_primary"]),
        width=0.48,
    )
    apply_atlas_layout(
        fig,
        title=f"Distribusi Kelas Air ({len(df)} Sampel)",
        height=280,
        show_legend=False,
        xaxis_title="Kelas Kelayakan Air",
        yaxis_title="Jumlah Sampel",
    )
    max_y = max(int(cls_counts["Jumlah Sampel"].max()), 1)
    fig.update_yaxes(range=[0, max_y * 1.2])
    return fig


def plot_fuzzy_score_boxplot(df: pd.DataFrame) -> go.Figure:
    """Box plot showing separation of Fuzzy Water Quality Score per actual potability class."""
    fig = px.box(
        df,
        x="potability_label",
        y="fuzzy_quality_score",
        color="potability_label",
        category_orders={"potability_label": CLASS_ORDER},
        color_discrete_map=POTABILITY_COLOR_MAP,
        points="outliers",
    )
    fig.update_traces(line_width=2)
    apply_atlas_layout(
        fig,
        title="Sebaran Skor Fuzzy per Kelas Aktual",
        height=285,
        show_legend=False,
        xaxis_title="Kelas Kelayakan Aktual",
        yaxis_title="Fuzzy Water Quality Score (0-100)",
    )
    fig.update_yaxes(range=[0, 102])
    return fig


def plot_membership_functions(
    var_key: str, title: str, x_label: str, current_val: Optional[float] = None
) -> go.Figure:
    """Plot Ruspini triangular membership functions with an optional live crisp input marker."""
    info = MF_PARAMS[var_key]
    lo, hi = info["domain"]
    x_grid = np.linspace(lo, hi, 400)

    fig = go.Figure()
    for set_name, params in info["sets"].items():
        y_vals = triangular_mf_array(x_grid, *params)
        color = MF_COLOR_MAP.get(set_name, PALETTE["cobalt_bright"])
        fig.add_trace(
            go.Scatter(
                x=x_grid,
                y=y_vals,
                mode="lines",
                name=set_name,
                line=dict(color=color, width=2.5),
                fill="tozeroy",
                fillcolor=f"rgba({int(color[1:3],16)}, {int(color[3:5],16)}, {int(color[5:7],16)}, 0.12)",
                hovertemplate=f"<b>{set_name}</b><br>{x_label}: %{{x:.3f}}<br>μ: %{{y:.4f}}<extra></extra>",
            )
        )

    if current_val is not None:
        val_clamped = float(np.clip(current_val, lo, hi))
        fig.add_vline(
            x=val_clamped,
            line_width=2,
            line_dash="dot",
            line_color="#f8fafc",
            annotation_text=f"Input = {current_val:.3f}",
            annotation_position="top",
            annotation_font=dict(family=PLOTLY_MONO_FAMILY, size=11, color="#f8fafc"),
            annotation_bgcolor=PALETTE["cobalt_surface"],
            annotation_bordercolor=PALETTE["cobalt"],
            annotation_borderpad=3,
        )

    apply_atlas_layout(
        fig,
        title=title,
        height=295,
        show_legend=True,
        xaxis_title=x_label,
        yaxis_title="Derajat Keanggotaan (μ)",
    )
    fig.update_yaxes(range=[-0.04, 1.15])
    return fig


def plot_aggregated_centroid(fuzzy_res: Dict[str, Any]) -> go.Figure:
    """Plot clipped Mamdani output sets, MAX aggregation polygon, and exact centroid z*."""
    z_grid = fuzzy_res["z_grid"]
    mu_grid = fuzzy_res["mu_grid"]
    z_star = fuzzy_res["water_quality_score"]
    agg = fuzzy_res["aggregated_alpha"]

    fig = go.Figure()
    out_sets = MF_PARAMS["water_quality_score"]["sets"]

    for set_name, params in out_sets.items():
        base_y = triangular_mf_array(z_grid, *params)
        color = MF_COLOR_MAP.get(set_name, PALETTE["slate_series"])
        fig.add_trace(
            go.Scatter(
                x=z_grid,
                y=base_y,
                mode="lines",
                name=f"{set_name} (α={agg[set_name]:.4f})",
                line=dict(color=color, width=1.4, dash="dash"),
                opacity=0.65,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=z_grid,
            y=mu_grid,
            mode="lines",
            name="Kurva Agregasi MAX μ_agg(z)",
            line=dict(color=PALETTE["cobalt_bright"], width=3),
            fill="tozeroy",
            fillcolor="rgba(59, 130, 246, 0.24)",
            hovertemplate="z = %{x:.2f}<br>μ_agg(z) = %{y:.4f}<extra></extra>",
        )
    )

    fig.add_vline(
        x=z_star,
        line_width=2.5,
        line_color="#fbbf24",
        annotation_text=f"Centroid z* = {z_star:.4f}",
        annotation_position="top right",
        annotation_font=dict(family=PLOTLY_MONO_FAMILY, size=12, color="#fef3c7"),
        annotation_bgcolor="#451a03",
        annotation_bordercolor="#f59e0b",
        annotation_borderpad=4,
    )

    apply_atlas_layout(
        fig,
        title="Kurva Agregasi MAX & Centroid (z*)",
        height=355,
        show_legend=True,
        xaxis_title="Domain Output Water Quality Score (z ∈ [0, 100])",
        yaxis_title="Derajat Keanggotaan μ_agg(z)",
    )
    fig.update_yaxes(range=[-0.04, 1.15])
    return fig


def plot_results_histogram(df_filtered: pd.DataFrame) -> go.Figure:
    """Histogram of Fuzzy Water Quality Score split by KNN predicted potability."""
    fig = px.histogram(
        df_filtered,
        x="fuzzy_quality_score",
        color="predicted_potability_knn",
        category_orders={"predicted_potability_knn": CLASS_ORDER},
        color_discrete_map=POTABILITY_COLOR_MAP,
        nbins=24,
        barmode="overlay",
        opacity=0.78,
    )
    apply_atlas_layout(
        fig,
        title="Skor Fuzzy per Kelas Prediksi KNN",
        height=350,
        show_legend=True,
        xaxis_title="Fuzzy Water Quality Score (0-100)",
        yaxis_title="Frekuensi Sampel",
    )
    return fig


def plot_physicochemical_scatter(df_filtered: pd.DataFrame) -> go.Figure:
    """Scatter map of pH vs Hardness sized by Turbidity and colored by predicted class."""
    fig = px.scatter(
        df_filtered,
        x="ph",
        y="Hardness",
        size="Turbidity",
        color="predicted_potability_knn",
        category_orders={"predicted_potability_knn": CLASS_ORDER},
        color_discrete_map=POTABILITY_COLOR_MAP,
        hover_data=["sample_id", "fuzzy_quality_score", "Turbidity"],
        opacity=0.84,
    )
    fig.update_traces(marker=dict(line=dict(width=0.6, color="#0d111a")))
    apply_atlas_layout(
        fig,
        title="Peta Fisikokimia (pH vs Hardness)",
        height=350,
        show_legend=True,
        xaxis_title="pH (Tingkat Keasaman Air)",
        yaxis_title="Hardness / Kesadahan (mg/L)",
    )
    return fig


def plot_k_sensitivity(
    k_list: List[int],
    vals_a: List[float],
    vals_b: List[float],
    metric_label: str,
    color_b: str,
) -> go.Figure:
    """Line chart comparing Model A (Baseline) vs Model B (Fuzzy-Enhanced) across K values."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=k_list,
            y=vals_a,
            mode="lines+markers",
            name="Model A (Baseline KNN · 3 Fitur)",
            line=dict(color="#94a3b8", width=2.2, dash="dash"),
            marker=dict(size=7, color="#94a3b8"),
            hovertemplate="K=%{x}<br>Model A: %{y:.2f}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=k_list,
            y=vals_b,
            mode="lines+markers",
            name="Model B (Fuzzy-Enhanced KNN · 4 Fitur)",
            line=dict(color=color_b, width=3.2),
            marker=dict(size=9, color=color_b, line=dict(width=1.5, color="#0d111a")),
            hovertemplate="K=%{x}<br>Model B: %{y:.2f}%<extra></extra>",
        )
    )
    apply_atlas_layout(
        fig,
        title=f"Sensitivitas Nilai K terhadap {metric_label} (%)",
        height=340,
        show_legend=True,
        xaxis_title="Nilai Parameter K",
        yaxis_title=f"{metric_label} (%)",
    )
    fig.update_xaxes(tickmode="array", tickvals=k_list)
    min_val = min(min(vals_a), min(vals_b))
    fig.update_yaxes(range=[max(0, min_val - 4), 101])
    return fig


def plot_confusion_matrix(
    cm: np.ndarray,
    model_title: str,
    accuracy_pct: float,
    is_model_b: bool = False,
) -> go.Figure:
    """Dark-themed Confusion Matrix heatmap with sharp numerical annotations."""
    colorscale = (
        ["#0f172a", "#1e3a8a", "#2563eb", "#60a5fa"]
        if is_model_b
        else ["#0f172a", "#1e293b", "#475569", "#94a3b8"]
    )
    fig = px.imshow(
        cm,
        text_auto=True,
        x=CLASS_ORDER,
        y=CLASS_ORDER,
        color_continuous_scale=colorscale,
        labels=dict(x="Kelas Prediksi", y="Kelas Aktual", color="Jumlah"),
    )
    fig.update_traces(
        textfont=dict(family=PLOTLY_MONO_FAMILY, size=18, color="#f8fafc"),
        hovertemplate="Aktual: %{y}<br>Prediksi: %{x}<br>Jumlah: %{z}<extra></extra>",
    )
    apply_atlas_layout(
        fig,
        title=f"{model_title} · Acc {accuracy_pct:.2f}%",
        height=335,
        show_legend=False,
        xaxis_title="Kelas Prediksi",
        yaxis_title="Kelas Aktual",
    )
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig
