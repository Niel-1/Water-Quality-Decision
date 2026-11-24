"""Entrypoint Streamlit untuk routing halaman aplikasi Water Quality & Potability DSS."""

import streamlit as st

from src.fuzzy_mamdani import compute_fuzzy_mamdani
from src.ui.components import render_sidebar_brand, render_sidebar_telemetry
from src.ui.constants import DEFAULT_MANUAL_INPUT, NAV_PAGES, TEAM_MEMBERS
from src.ui.data import load_default_datasets
from src.ui.pages.dashboard import render_dashboard
from src.ui.pages.documentation import render_documentation
from src.ui.pages.evaluation import render_evaluation
from src.ui.pages.input_dataset import render_input_dataset
from src.ui.pages.results import render_results
from src.ui.pages.whitebox import render_whitebox
from src.ui.theme import inject_theme

st.set_page_config(
    page_title="Water Quality & Potability DSS · Kelompok 1 Unud",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="auto",
)


def _init_session_state(df_default) -> None:
    """Initialize durable session state for dataset and active simulation sample."""
    if "active_dataset" not in st.session_state:
        st.session_state["active_dataset"] = df_default.copy()
    if "dataset_source_name" not in st.session_state:
        st.session_state["dataset_source_name"] = (
            "Kaggle Water Potability Clean Dataset (600 Samples)"
        )
    if "manual_input" not in st.session_state or "ph" not in st.session_state["manual_input"]:
        st.session_state["manual_input"] = dict(DEFAULT_MANUAL_INPUT)


def _render_sidebar(df_active) -> str:
    """Render the dark navigation rail, live telemetry tray, and team credits."""
    with st.sidebar:
        render_sidebar_brand()

        page_ids = [item[0] for item in NAV_PAGES]
        page_labels = {item[0]: f"{item[1]} · {item[2]}" for item in NAV_PAGES}

        q_page = st.query_params.get("page", "")
        default_idx = page_ids.index(q_page) if q_page in page_ids else 0

        selected_page = st.radio(
            "Navigation",
            options=page_ids,
            index=default_idx,
            format_func=lambda pid: page_labels[pid],
        )

        inp = st.session_state["manual_input"]
        fuzzy_live = compute_fuzzy_mamdani(
            inp["ph"], inp["Hardness"], inp["Turbidity"], method="analytic"
        )
        render_sidebar_telemetry(
            ph=inp["ph"],
            hardness=inp["Hardness"],
            turbidity=inp["Turbidity"],
            z_star=fuzzy_live["water_quality_score"],
            k_neighbors=inp["k_neighbors"],
            dataset_rows=len(df_active),
            quality_label=fuzzy_live["quality_linguistic"],
        )

        with st.expander("Kelompok 1 & Dosen Pengampu", expanded=False):
            lines = [
                f"**{m['No']}. {m['Nama Mahasiswa']}** (`{m['NIM']}`)"
                for m in TEAM_MEMBERS
            ]
            st.markdown("\n\n".join(lines))
            st.caption(
                "Dosen Pengampu: Dr. Made Agung Raharja, S.Si., M.Cs. · Program Studi Informatika, FMIPA Universitas Udayana"
            )

    return selected_page


def main() -> None:
    inject_theme()
    df_default, df_manual = load_default_datasets()
    _init_session_state(df_default)

    df_active = st.session_state["active_dataset"]
    selected_page = _render_sidebar(df_active)

    if selected_page == "dashboard":
        render_dashboard(df_active, st.session_state["dataset_source_name"])
    elif selected_page == "input":
        render_input_dataset(df_default, df_active, df_manual)
    elif selected_page == "whitebox":
        render_whitebox(df_active, df_manual)
    elif selected_page == "results":
        render_results(df_active)
    elif selected_page == "evaluation":
        render_evaluation(df_active)
    elif selected_page == "docs":
        render_documentation()


if __name__ == "__main__":
    main()
