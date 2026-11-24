"""Definisi stylesheet CSS untuk tampilan antarmuka Streamlit."""

import streamlit as st


APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Public+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-canvas: #0d111a;
    --bg-rail: #090c14;
    --bg-surface: #131a28;
    --bg-recessed: #0f1522;
    --bg-hover: #1a2438;
    --border: #233047;
    --border-subtle: #1c2638;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #8192ac;
    --cobalt: #3b82f6;
    --cobalt-bright: #60a5fa;
    --cobalt-surface: #172554;
    --potable: #34d399;
    --potable-bg: #0b2922;
    --potable-border: #165242;
    --moderate: #fbbf24;
    --moderate-bg: #2c200b;
    --moderate-border: #593f14;
    --poor: #fb7185;
    --poor-bg: #2e121b;
    --poor-border: #632236;
    --font-sans: 'Public Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
    --radius-sm: 8px;
    --radius-md: 12px;
}

/* Global canvas, typography & browser surfaces */
html, body, [class*="css"], .stApp {
    font-family: var(--font-sans);
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    caret-color: var(--cobalt-bright);
}

* {
    scrollbar-width: thin;
    scrollbar-color: #233047 #090c14;
}

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-rail);
}

::-webkit-scrollbar-thumb {
    background-color: var(--border);
    border-radius: 999px;
    border: 2px solid var(--bg-rail);
}

::-webkit-scrollbar-thumb:hover {
    background-color: #36496b;
}

a {
    color: var(--cobalt-bright);
    text-underline-offset: 0.2em;
}

:focus-visible {
    outline: 2px solid var(--cobalt);
    outline-offset: 2px;
}

::selection {
    background-color: rgba(59, 130, 246, 0.35);
    color: #f8fafc;
}

/* Hide distracting default Streamlit chrome while keeping sidebar toggle */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
div[data-testid="stAppDeployButton"],
div[data-testid="stToolbarActions"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: rgba(13, 17, 26, 0.85);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border-subtle);
}

/* Main workspace rhythm */
.block-container {
    max-width: 1280px;
    padding-top: 3.6rem;
    padding-bottom: 3.25rem;
    padding-left: 2.25rem;
    padding-right: 2.25rem;
}

/* Headings */
h1, h2, h3, h4 {
    font-family: var(--font-sans);
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

div[data-testid="stHeading"] h2 {
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    margin-top: 1.4rem !important;
    margin-bottom: 0.55rem !important;
}

div[data-testid="stHeading"] h3 {
    font-size: 1.04rem !important;
    font-weight: 700 !important;
    margin-top: 1.15rem !important;
    margin-bottom: 0.45rem !important;
}

div[data-testid="stHeading"] h4 {
    font-size: 0.94rem !important;
    font-weight: 700 !important;
    margin-top: 0.25rem !important;
    margin-bottom: 0.5rem !important;
}

p, li {
    color: #cbd5e1;
    line-height: 1.6;
}

/* Override Streamlit default green inline code across all containers */
code,
div[data-testid="stMarkdownContainer"] code,
.atlas-notice code,
.stage-desc code,
.atlas-table code,
.atlas-card code {
    font-family: var(--font-mono) !important;
    font-size: 0.83em !important;
    background-color: var(--bg-recessed) !important;
    color: #93c5fd !important;
    padding: 0.14rem 0.42rem !important;
    border-radius: 5px !important;
    border: 1px solid var(--border-subtle) !important;
}

hr {
    border: none;
    border-top: 1px solid var(--border-subtle);
    margin: 1.4rem 0;
}

/* Sidebar Rail */
section[data-testid="stSidebar"] {
    background-color: var(--bg-rail);
    border-right: 1px solid var(--border-subtle);
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.15rem;
    padding-left: 0.95rem;
    padding-right: 0.95rem;
}

/* Sidebar Brand */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 0.72rem;
    padding: 0.25rem 0.25rem 1rem 0.25rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 0.9rem;
}

.sb-brand-icon {
    width: 36px;
    height: 36px;
    border-radius: 9px;
    background-color: var(--cobalt-surface);
    border: 1px solid #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: #93c5fd;
}

.sb-brand-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.sb-brand-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.15rem;
}

/* Navigation Radio styled as clean full-width modern sidebar rail */
section[data-testid="stSidebar"] div[data-testid="stRadio"],
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    width: 100% !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 0.28rem !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"],
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    width: 100% !important;
    max-width: 100% !important;
    display: flex !important;
    align-items: center !important;
    box-sizing: border-box !important;
    padding: 0.56rem 0.8rem !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
    transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease;
    margin: 0 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child:not(:has(p)) {
    display: none !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #121a2a !important;
    color: var(--text-primary) !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background-color: var(--cobalt-surface) !important;
    border-color: #2563eb !important;
    color: #dbeafe !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:focus-visible) {
    outline: 2px solid var(--cobalt) !important;
    outline-offset: 1px !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 0.84rem;
    font-weight: 600;
    color: inherit;
    margin: 0;
}

/* Recessed sidebar telemetry tray */
.sb-tray {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.85rem 0.95rem;
    margin-top: 1rem;
}

.sb-tray-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.55rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-subtle);
}

.sb-tray-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-primary);
}

.sb-kv {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.32rem 0;
    border-bottom: 1px solid #182133;
    font-size: 0.79rem;
}

.sb-kv:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.sb-kv .k {
    color: var(--text-secondary);
}

.sb-kv .v {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    color: var(--text-primary);
}

/* Page Header */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1.25rem;
    padding-bottom: 1rem;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
}

@media (max-width: 860px) {
    .page-header {
        flex-direction: column;
        align-items: flex-start;
    }
}

.page-header-copy {
    min-width: 0;
    flex: 1;
}

div[data-testid="stMarkdownContainer"] h1.page-title,
div[data-testid="stMarkdownContainer"] .page-title,
.page-header .page-title {
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.025em !important;
    line-height: 1.22 !important;
    margin: 0 !important;
    padding: 0 !important;
}

@media (max-width: 640px) {
    .block-container {
        padding-left: 1.05rem !important;
        padding-right: 1.05rem !important;
    }
    div[data-testid="stMarkdownContainer"] h1.page-title,
    div[data-testid="stMarkdownContainer"] .page-title,
    .page-header .page-title {
        font-size: 1.26rem !important;
    }
}

.page-subtitle {
    font-size: 0.89rem;
    color: var(--text-secondary);
    margin: 0.32rem 0 0 0;
    max-width: 72ch;
}

.header-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.42rem 0.85rem;
    border-radius: var(--radius-sm);
    background-color: var(--cobalt-surface);
    border: 1px solid #2563eb;
    color: #bfdbfe;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: var(--font-mono);
    white-space: nowrap;
    flex-shrink: 0;
    margin-top: 0.15rem;
}

/* KPI Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.95rem;
    margin-bottom: 1.25rem;
}

@media (max-width: 960px) {
    .kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 560px) {
    .kpi-grid {
        grid-template-columns: 1fr;
    }
}

.kpi-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1rem 1.15rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 112px;
}

.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.kpi-value {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 0.35rem;
    line-height: 1.15;
}

.kpi-meta {
    font-size: 0.76rem;
    font-weight: 600;
    margin-top: 0.45rem;
    color: var(--cobalt-bright);
    font-variant-numeric: tabular-nums;
}

.kpi-meta.potable { color: var(--potable); }
.kpi-meta.moderate { color: var(--moderate); }
.kpi-meta.poor { color: var(--poor); }
.kpi-meta.muted { color: var(--text-secondary); }

/* Surface Cards & Recessed Trays */
.atlas-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.35rem;
    margin-bottom: 1rem;
}

.atlas-card-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.75rem 0;
}

.stage-tray {
    background-color: var(--bg-recessed);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 0.95rem 1.05rem;
    margin-bottom: 0.75rem;
}

.stage-tray:last-child {
    margin-bottom: 0;
}

.stage-tray-head {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.4rem;
}

.stage-num {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: #93c5fd;
    background-color: var(--cobalt-surface);
    border: 1px solid #2563eb;
    padding: 0.14rem 0.5rem;
    border-radius: 5px;
    white-space: nowrap;
    flex-shrink: 0;
}

.stage-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--text-primary);
}

.stage-desc {
    font-size: 0.85rem;
    color: #cbd5e1;
    margin: 0;
    line-height: 1.58;
}

/* Banner notifikasi */
.atlas-notice {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.95rem 1.15rem;
    margin-bottom: 1.1rem;
    font-size: 0.87rem;
    color: #cbd5e1;
    line-height: 1.6;
}

.atlas-notice.accent {
    background-color: #111c33;
    border-color: #244073;
}

.atlas-notice strong {
    color: var(--text-primary);
}

/* Strip indikator rentang parameter fisikokimia */
.spectrum-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
    margin-bottom: 1.15rem;
}

@media (max-width: 768px) {
    .spectrum-grid {
        grid-template-columns: 1fr;
    }
}

.spectrum-card {
    background-color: var(--bg-recessed);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1rem;
}

.spectrum-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.45rem;
}

.spectrum-name {
    font-size: 0.79rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.spectrum-val {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
}

.spectrum-track {
    height: 7px;
    border-radius: 4px;
    background-color: #1c273b;
    overflow: hidden;
    position: relative;
}

.spectrum-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 180ms ease;
}

.spectrum-meta {
    display: flex;
    justify-content: space-between;
    margin-top: 0.42rem;
    font-size: 0.72rem;
    color: var(--text-muted);
    font-family: var(--font-mono);
}

/* Stepper Grid on Page 3 */
.stepper-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.1rem;
}

@media (max-width: 960px) {
    .stepper-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

.step-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.85rem 0.95rem;
}

.step-code {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--cobalt-bright);
    margin-bottom: 0.25rem;
}

.step-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}

.step-desc {
    font-size: 0.77rem;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.48;
}

/* Semantic Status Badges */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.16rem 0.56rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    line-height: 1.3;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
}

.badge-potable {
    background-color: var(--potable-bg);
    color: var(--potable);
    border: 1px solid var(--potable-border);
}

.badge-moderate {
    background-color: var(--moderate-bg);
    color: var(--moderate);
    border: 1px solid var(--moderate-border);
}

.badge-poor {
    background-color: var(--poor-bg);
    color: var(--poor);
    border: 1px solid var(--poor-border);
}

.badge-cobalt {
    background-color: var(--cobalt-surface);
    color: #93c5fd;
    border: 1px solid #2563eb;
}

.badge-neutral {
    background-color: #1a2333;
    color: #cbd5e1;
    border: 1px solid #2b3952;
}

/* Clean Precision Data Tables */
.atlas-table-wrap {
    width: 100%;
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background-color: var(--bg-surface);
    margin: 0.65rem 0 1rem 0;
}

.atlas-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.835rem;
    font-variant-numeric: tabular-nums;
}

.atlas-table thead th {
    background-color: var(--bg-recessed);
    color: var(--text-secondary);
    font-weight: 700;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 0.72rem 0.9rem;
    border-bottom: 1px solid var(--border);
    text-align: left;
    white-space: nowrap;
}

.atlas-table thead th.num,
.atlas-table tbody td.num {
    text-align: right;
    font-family: var(--font-mono);
    white-space: nowrap;
}

.atlas-table tbody td {
    padding: 0.65rem 0.9rem;
    border-bottom: 1px solid var(--border-subtle);
    color: #e2e8f0;
    vertical-align: middle;
}

@media (max-width: 640px) {
    .atlas-table {
        font-size: 0.79rem;
        min-width: 520px;
    }
    .atlas-table thead th,
    .atlas-table tbody td {
        padding: 0.55rem 0.65rem;
    }
}

.atlas-table tbody tr:last-child td {
    border-bottom: none;
}

.atlas-table tbody tr:hover td {
    background-color: var(--bg-hover);
}

.atlas-table tbody tr.row-highlight td {
    background-color: #16223a;
    color: #f8fafc;
}

.atlas-table tbody tr.row-total td {
    background-color: var(--bg-recessed);
    font-weight: 700;
    color: #f8fafc;
    border-top: 1px solid var(--border);
}

.atlas-table thead th .math-sym {
    text-transform: none !important;
}

.atlas-table td code.nowrap-code {
    white-space: nowrap !important;
    display: inline-block;
    margin: 0.1rem 0.25rem 0.1rem 0;
}

/* Inline firing-strength bar inside white-box rule table */
.alpha-cell {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.55rem;
}

.alpha-bar-track {
    width: 64px;
    height: 6px;
    background-color: #0d1320;
    border-radius: 3px;
    overflow: hidden;
    flex-shrink: 0;
}

.alpha-bar-fill {
    height: 100%;
    border-radius: 3px;
}

/* Streamlit widget refinements */
div[data-testid="stTabs"] button[role="tab"] {
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--text-secondary);
    padding: 0.6rem 1rem;
}

div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #93c5fd;
    border-bottom-color: var(--cobalt);
}

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stDownloadButton"] button {
    border-radius: var(--radius-sm);
    font-weight: 600;
    border: 1px solid #2563eb;
    background-color: var(--cobalt-surface);
    color: #dbeafe;
    transition: background-color 150ms ease, border-color 150ms ease;
}

div[data-testid="stButton"] button[kind="primary"],
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"],
div[data-testid="stFormSubmitButton"] button[kind="primary"],
div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primaryFormSubmit"] {
    background-color: var(--cobalt);
    border-color: var(--cobalt-bright);
    color: #ffffff;
}

div[data-testid="stButton"] button:hover,
div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stDownloadButton"] button:hover {
    background-color: #1e3a8a;
    border-color: var(--cobalt-bright);
    color: #ffffff;
}

div[data-testid="stButton"] button[kind="primary"]:hover,
div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover,
div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background-color: #2563eb;
    border-color: #93c5fd;
    color: #ffffff;
}

div[data-testid="stButton"] button:focus-visible,
div[data-testid="stFormSubmitButton"] button:focus-visible,
div[data-testid="stDownloadButton"] button:focus-visible {
    outline: 2px solid var(--cobalt);
    outline-offset: 2px;
}

/* Presentation focus cue & active sample summary ribbon */
.focus-cue {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
    background-color: var(--bg-recessed);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.7rem 1rem;
    margin-bottom: 1.1rem;
    font-size: 0.86rem;
    color: #cbd5e1;
    line-height: 1.52;
}

.focus-cue-tag {
    font-family: var(--font-mono);
    font-size: 0.71rem;
    font-weight: 700;
    color: #93c5fd;
    background-color: var(--cobalt-surface);
    border: 1px solid #2563eb;
    padding: 0.14rem 0.5rem;
    border-radius: 5px;
    white-space: nowrap;
    flex-shrink: 0;
}

.focus-cue strong {
    color: var(--text-primary);
}

.sample-ribbon {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.8rem 1.05rem;
    margin-bottom: 1rem;
}

.sample-ribbon-items {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1.15rem;
    font-size: 0.84rem;
}

.sample-ribbon-kv {
    display: inline-flex;
    align-items: baseline;
    gap: 0.4rem;
}

.sample-ribbon-kv .k {
    color: var(--text-secondary);
    font-size: 0.78rem;
}

.sample-ribbon-kv .v {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    font-weight: 700;
    color: var(--text-primary);
}

.flow-caption {
    font-size: 0.84rem;
    color: var(--text-secondary);
    margin: 0.2rem 0 0 0;
}

/* Container borders */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--bg-surface);
    border-color: var(--border) !important;
    border-radius: var(--radius-md);
}

/* Plotly chart wrapper */
div[data-testid="stPlotlyChart"] {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.45rem 0.5rem 0.25rem 0.5rem;
}

/* Streamlit native metric override (if used anywhere) */
div[data-testid="stMetric"] {
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.05rem;
}
</style>
"""


def inject_theme() -> None:
    """Inject the Bathymetric Hydrographic Atlas stylesheet into Streamlit."""
    st.markdown(APP_CSS, unsafe_allow_html=True)
