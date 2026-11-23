---
name: Water Quality & Potability DSS
description: Bathymetric Hydrographic Atlas analytical workbench for white-box Fuzzy Mamdani and KNN water potability analysis.
colors:
  cobalt-primary: "#3b82f6"
  cobalt-bright: "#60a5fa"
  cobalt-surface: "#172554"
  cobalt-border: "#2563eb"
  potable-emerald: "#10b981"
  potable-mint: "#34d399"
  potable-surface: "#0b2922"
  moderate-ochre: "#eab308"
  moderate-amber: "#fbbf24"
  moderate-surface: "#2c200b"
  poor-rose: "#f43f5e"
  poor-coral: "#fb7185"
  poor-surface: "#2e121b"
  abyssal-canvas: "#0d111a"
  trench-rail: "#090c14"
  slate-surface: "#131a28"
  recessed-tray: "#0f1522"
  hover-slate: "#1a2438"
  hairline-border: "#233047"
  subtle-divider: "#1c2638"
  ink-primary: "#f1f5f9"
  ink-body: "#cbd5e1"
  ink-secondary: "#94a3b8"
  ink-muted: "#8192ac"
typography:
  display:
    fontFamily: "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "1.55rem"
    fontWeight: 800
    lineHeight: 1.22
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "1.18rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "0.98rem"
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "0.89rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0em"
  label:
    fontFamily: "Public Sans, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.04em"
  mono-kpi:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "1.6rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "0em"
    fontFeature: "tnum"
  mono-data:
    fontFamily: "JetBrains Mono, ui-monospace, SFMono-Regular, monospace"
    fontSize: "0.835rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0em"
    fontFeature: "tnum"
rounded:
  xs: "5px"
  sm: "8px"
  md: "12px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "12px"
  md: "16px"
  lg: "20px"
  xl: "36px"
components:
  button-primary:
    backgroundColor: "{colors.cobalt-surface}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  button-primary-hover:
    backgroundColor: "{colors.cobalt-border}"
    textColor: "{colors.ink-primary}"
  nav-item:
    backgroundColor: "transparent"
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
  nav-item-active:
    backgroundColor: "{colors.cobalt-surface}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
  kpi-card:
    backgroundColor: "{colors.slate-surface}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.md}"
    padding: "16px 18px"
  surface-card:
    backgroundColor: "{colors.slate-surface}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.md}"
    padding: "19px 22px"
  recessed-tray:
    backgroundColor: "{colors.recessed-tray}"
    textColor: "{colors.ink-body}"
    rounded: "{rounded.sm}"
    padding: "15px 17px"
  badge-potable:
    backgroundColor: "{colors.potable-surface}"
    textColor: "{colors.potable-mint}"
    rounded: "{rounded.pill}"
    padding: "3px 9px"
  badge-moderate:
    backgroundColor: "{colors.moderate-surface}"
    textColor: "{colors.moderate-amber}"
    rounded: "{rounded.pill}"
    padding: "3px 9px"
  badge-poor:
    backgroundColor: "{colors.poor-surface}"
    textColor: "{colors.poor-coral}"
    rounded: "{rounded.pill}"
    padding: "3px 9px"
  header-chip:
    backgroundColor: "{colors.cobalt-surface}"
    textColor: "{colors.ink-primary}"
    rounded: "{rounded.sm}"
    padding: "7px 14px"
---

# Design System: Water Quality & Potability DSS

## Overview

**Creative North Star: "Bathymetric Hydrographic Atlas"**

This design system treats the Water Quality & Potability Decision Support System as a precision hydrographic instrument rather than a generic web dashboard. Deep abyssal slate surfaces anchor the workspace so high-contrast tabular mathematics, membership polygons, and Model A vs Model B comparisons remain legible on both laptop screens and classroom projectors.

Every structural plane is separated through quiet dark tonal stepping and crisp 1px slate hairlines rather than drop shadows or frosted-glass clutter. Saturated color is disciplined and functional: mineral cobalt marks active navigation, primary focus, and Model B highlights, while emerald, amber, and rose are strictly reserved for water-quality classification verdicts (`Potable`/`Good`, `Moderate`, and `Not Potable`/`Poor`).

This visual world explicitly rejects flat white default templates and low-transparency pale-green highlight boxes. Its density is calibrated for white-box auditability so every fuzzy membership degree, rule firing strength, piecewise integral segment, and Euclidean KNN distance reads cleanly to four decimal places (`0.0000`).

**Key Characteristics:**
- Layered dark slate architecture (`#090c14` rail, `#0d111a` canvas, `#131a28` cards, `#0f1522` recessed trays) with hairline borders (`#233047`).
- Disciplined Mineral Cobalt (`#3b82f6` / `#60a5fa`) interactive accent paired with strict 3-state water-quality semantics.
- Crisp pairing of `Public Sans` UI hierarchy with `JetBrains Mono` (`tabular-nums`) for all coordinates, KPI figures, and 4-decimal calculation tables.
- Zero drop shadows at rest; visual depth comes entirely from luminance stepping and structural hairlines.
- Inline data-reading craft such as physicochemical compliance spectrums and rule firing-strength bars embedded directly inside tables.

## Colors

The palette is built on cold deep-water slates with a single interactive Mineral Cobalt accent and a strictly bounded three-state semantic triad for potability verdicts.

### Primary
- **Mineral Cobalt** (`#3b82f6`): Primary interactive focus ring, active tab underline, and primary chart highlight series.
- **Cobalt Bright** (`#60a5fa`): High-contrast data highlights, active KPI deltas, step indices, and hover accents on dark slate surfaces.
- **Cobalt Surface** (`#172554`): Fill for active sidebar navigation items, primary action buttons, header status chips, and stage index badges.
- **Cobalt Border** (`#2563eb`): Crisp 1px outline pairing with Cobalt Surface for active pills, brand mark framing, and interactive controls.

### Secondary
- **Potable Emerald / Mint** (`#10b981` chart / `#34d399` text on `#0b2922` surface): Reserved exclusively for `Potable` and `Good` water-quality states and compliance bars inside WHO/Permenkes thresholds.
- **Moderate Ochre / Amber** (`#eab308` chart / `#fbbf24` text on `#2c200b` surface): Reserved for `Moderate`, transitional, or `Alkaline` membership curves and warning compliance ranges.
- **Poor Rose / Coral** (`#f43f5e` chart / `#fb7185` text on `#2e121b` surface): Reserved for `Not Potable`, `Poor`, `Acidic`, `Hard`, and `Turbid` states.

### Neutral
- **Trench Rail** (`#090c14`): Deepest background plane used exclusively for the left navigation rail.
- **Abyssal Canvas** (`#0d111a`): Primary application canvas behind all cards, tables, and Plotly figures.
- **Recessed Tray** (`#0f1522`): Sunken surface for nested pipeline steps, table headers, inline code pills, and physicochemical compliance cards.
- **Slate Surface** (`#131a28`): Elevated container plane for KPI cards, Plotly chart frames, sidebar telemetry trays, and analytical cards.
- **Hover Slate** (`#1a2438`): Subtle row hover elevation inside precision data tables.
- **Hairline Border** (`#233047`): Primary 1px structural divider around cards, tables, charts, and header rules.
- **Subtle Divider** (`#1c2638`): Secondary 1px internal separator for table rows, sidebar dividers, and recessed trays.
- **Ink Primary** (`#f1f5f9`): High-contrast primary headings, KPI figures, and emphasized labels.
- **Ink Body** (`#cbd5e1`): Default prose copy, stage descriptions, and table text.
- **Ink Secondary** (`#94a3b8`): Subtitles, inactive navigation items, KPI labels, and table column headers.
- **Ink Muted** (`#8192ac`): Secondary metadata, unit labels, and axis ticks.

### Named Rules
**The Semantic Quarantine Rule.** Emerald (`#10b981`/`#34d399`), amber (`#eab308`/`#fbbf24`), and rose (`#f43f5e`/`#fb7185`) are strictly quarantined to water-quality verdicts, membership curves, and compliance indicators. Never use green or red for generic navigation chrome, decorative borders, or neutral callout panels.

**The Single Interactive Voice Rule.** Mineral Cobalt (`#3b82f6` / `#172554`) is the sole accent for interactive state (active rail item, primary buttons, active tabs, and focus outlines).

## Typography

**Display Font:** `Public Sans` (fallback `-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif`)
**Body Font:** `Public Sans` (fallback `-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif`)
**Label/Mono Font:** `JetBrains Mono` (fallback `ui-monospace, SFMono-Regular, monospace`)

**Character:** Engineered and civic. `Public Sans` provides disciplined neutral geometry that stays sharp under classroom projection, while `JetBrains Mono` locks every 4-decimal calculation into strict vertical alignment.

### Hierarchy
- **Display / Page Title** (800 weight, `1.5rem`, `1.2` line-height, `-0.025em` tracking): Top-of-page analytical workspace headers across all 6 pages.
- **Headline / Section H2** (700 weight, `1.18rem`, `1.3` line-height, `-0.02em` tracking): Major analytical section headers inside each workspace page.
- **Title / Card Title** (700 weight, `0.98rem`, `1.35` line-height, `-0.015em` tracking): Card titles, recessed pipeline stage titles, and Plotly chart titles.
- **Body** (400 weight, `0.89rem`, `1.6` line-height, max `72ch` on subtitles): Explanatory prose, stage descriptions, and user guidance.
- **Label / Column Header** (700 weight, `0.75rem`, `1.3` line-height, `+0.04em` tracking, uppercase on table headers and sidebar section labels): Table headers, KPI labels, and compact telemetry keys.
- **Monospace KPI** (700 weight, `1.6rem`, `1.15` line-height, `tabular-nums`): Primary numeric readouts inside the 4-column KPI strip.
- **Monospace Data** (600 weight, `0.835rem`, `1.4` line-height, `tabular-nums`): Right-aligned table cells, sidebar telemetry values, physicochemical readouts, and 4-decimal white-box proof outputs (`0.0000`).

### Named Rules
**The Tabular Lock Rule.** Every numeric column, KPI figure, sidebar telemetry reading, and fuzzy rule firing strength must use `JetBrains Mono` with `font-variant-numeric: tabular-nums` and right alignment in tables so decimal points stack vertically.

## Layout

The application uses an asymmetric persistent-rail workbench layout optimized for desktop projection (`1440px`) while collapsing cleanly down to narrow mobile screens (`390px`).

- **Navigation Rail:** Fixed left sidebar on Trench Rail (`#090c14`) separated by a 1px right divider (`#1c2638`), housing the brand mark, 6 numbered workspace routes, and a recessed Active Sample Telemetry tray. Streamlit collapses the rail automatically behind its native top-left toggle on narrow viewports (`initial_sidebar_state="auto"`).
- **Primary Workspace Container:** Centered up to `1280px` max-width with `3.6rem` top padding, `3.25rem` bottom padding, and `2.25rem` horizontal padding.
- **Page Header Band:** Flex row pairing left-aligned title/subtitle (`max-width: 72ch`) with a right-aligned monospace status chip over a full-width 1px bottom border (`#233047`). Stacks vertically below `860px`.
- **KPI Metric Grid:** 4 equal columns (`repeat(4, minmax(0, 1fr))`) with `0.95rem` gap; collapses to 2 columns below `960px` and 1 column below `560px`.
- **Physicochemical Compliance Strip:** 3 equal columns (`pH`, `Hardness`, `Turbidity`) with `0.85rem` gap; collapses to 1 column below `768px`.
- **White-Box Stepper Grid:** 4 equal columns on Page 3 with `0.75rem` gap; collapses to 2 columns below `960px`.
- **Chart & Analysis Grids:** 2-column Streamlit splits for side-by-side membership curves, confusion matrices, and dashboard pipeline/chart pairings.

## Elevation & Depth

This system uses **tonal layering and hairline borders only**. Surfaces are completely flat with zero drop shadows at rest. Depth is communicated strictly through four controlled luminance planes from deepest to highest:

1. **Plane 0 (Trench Rail):** `#090c14` for the persistent navigation sidebar.
2. **Plane 1 (Abyssal Canvas):** `#0d111a` for the main workspace floor.
3. **Plane 2 (Recessed Tray):** `#0f1522` for sunken nested trays, table headers, and compliance gauges inside cards.
4. **Plane 3 (Elevated Surface):** `#131a28` bordered by `1px solid #233047` for KPI cards, analytical panels, Plotly frames, and telemetry cards.

Interactive hover states step up cleanly to `#1a2438` (table rows) or `#121a2a` (sidebar items) over `150ms ease`.

### Named Rules
**The Zero-Shadow Tonal Rule.** Never apply blurred drop shadows or glowing box-shadows to cards, badges, or charts. Separate planes exclusively by stepping between `#090c14`, `#0d111a`, `#0f1522`, and `#131a28` framed by 1px slate hairlines (`#233047` / `#1c2638`).

## Shapes

The form language is architectural and restrained, favoring precision-machined corners over pill-heavy consumer styling.

- **Primary Containers (`12px` radius):** Applied uniformly to KPI cards, surface cards, table wrappers, Plotly frames, notice banners, and the sidebar telemetry tray.
- **Controls & Recessed Trays (`8px` radius):** Applied to sidebar navigation pills, buttons, header status chips, physicochemical spectrum cards, and stage trays.
- **Micro Badges & Inline Code (`5px` radius):** Applied to stage number tags (`01`..`04`) and inline monospace code snippets.
- **Semantic Status Pills (`999px` radius):** Reserved solely for compact classification badges (`Potable`, `Not Potable`, `Good`, `Moderate`, `Poor`, `Aktif`) so status verdicts stand out immediately from structural cards.
- **Progress & Firing-Strength Tracks (`3px`–`4px` radius):** Crisp horizontal micro-bars inside physicochemical compliance cards and the 27-rule white-box table.

## Components

Every component is built to feel tactile, high-contrast, and instrument-grade without decorative noise.

### Buttons
- **Shape:** Precision rounded rectangle (`8px` radius).
- **Primary:** Cobalt Surface (`#172554`) background, `#dbeafe` / `#f1f5f9` text, `1px solid #2563eb` border, 600 weight, `150ms ease` color transition.
- **Hover / Focus:** Shifts to deep cobalt fill (`#1e3a8a`), Cobalt Bright (`#60a5fa`) border, and `#ffffff` text; `:focus-visible` shows a crisp `2px solid #3b82f6` outline with `2px` offset.

### Chips & Semantic Badges
- **Header Status Chip:** Monospace `0.78rem` tag on Cobalt Surface (`#172554`) with `1px solid #2563eb` border and `8px` radius, anchored top-right of every page header.
- **Classification Badges:** Full-pill (`999px`) `0.74rem` bold tags pairing dark tinted fills with high-contrast text and borders (`Potable`/`Good`: `#0b2922` / `#34d399` / `#165242`; `Moderate`: `#2c200b` / `#fbbf24` / `#593f14`; `Not Potable`/`Poor`: `#2e121b` / `#fb7185` / `#632236`). Always include explicit text labels alongside color.

### Cards & Containers
- **Corner Style:** `12px` radius for primary surfaces (`atlas-card`, `kpi-card`, `atlas-notice`, `stPlotlyChart`), `8px` radius for nested `stage-tray` blocks.
- **Background:** Slate Surface (`#131a28`) for outer cards; Recessed Tray (`#0f1522`) for nested stages.
- **Border:** `1px solid #233047` on outer surfaces; `1px solid #1c2638` on nested trays.
- **Internal Padding:** `16px 18px` on KPI cards (`min-height: 112px`), `19px 22px` on surface cards, `15px 17px` on recessed trays.

### Inputs & Fields
- **Style:** Native dark-theme Streamlit inputs, sliders, selectboxes, and file uploaders inheriting `#0d111a` / `#131a28` surfaces, `#233047` borders, and `#3b82f6` active accent from `.streamlit/config.toml`.
- **Focus:** Cobalt border and focus ring without shifting layout geometry.

### Navigation
- **Sidebar Rail:** Full-width stacked radio items inside the `#090c14` rail with `8px` radius, `0.52rem 0.72rem` padding, and `0.84rem` 600-weight labels.
- **States:** Transparent default (`#94a3b8`), `#121a2a` hover (`#f1f5f9`), and Cobalt Surface (`#172554`) + `1px solid #2563eb` border (`#dbeafe`) when active.
- **Telemetry Footer Tray:** Recessed `#131a28` card below navigation displaying live `pH`, `Hardness`, `Turbidity`, `Skor z*`, `Tetangga K`, and dataset size in right-aligned `JetBrains Mono`.

### Physicochemical Compliance Strip
A 3-card recessed horizontal strip (`pH`, `Hardness`, `Turbidity`) displaying each parameter's live monospace value, a `7px` color-coded compliance track against WHO/Permenkes limits, and a range footer (`Ideal 6.5-8.5`, `Ideal <= 150 mg/L`, `Ideal <= 3.0 NTU`).

### Precision White-Box Rule Table
A full-width dark table (`#131a28` body, `#0f1522` uppercase header, `#1a2438` row hover, `#16223a` highlighted active rows) featuring right-aligned `JetBrains Mono` 4-decimal numbers and an inline `64px × 6px` firing-strength (`alpha`) progress bar beside every rule's numeric firing weight.

## Do's and Don'ts

### Do:
- **Do** format every numerical metric, membership value, integral area, and KNN distance in `JetBrains Mono` with `tabular-nums` and exact 4-decimal precision (`0.0000`) where calculations are audited.
- **Do** pair every semantic color cue (`Potable`, `Not Potable`, `Good`, `Moderate`, `Poor`) with an explicit text label or badge.
- **Do** separate surface levels using the four dark slate planes (`#090c14`, `#0d111a`, `#0f1522`, `#131a28`) and 1px hairline borders (`#233047`).
- **Do** render custom HTML blocks through `render_html()` so line indentation never triggers Streamlit Markdown code-block escaping.
- **Do** keep Plotly chart canvases dark (`#131a28` paper, `#0f1522` plot area, `#1e2a3f` gridlines) so visualizations integrate seamlessly into surrounding cards.

### Don't:
- **Don't** use flat white backgrounds or low-transparency pale-green highlight boxes anywhere in the interface.
- **Don't** apply drop shadows, neon glows, or decorative gradients to cards, buttons, or charts.
- **Don't** use emerald, amber, or rose for neutral UI chrome or interactive focus states; reserve them strictly for water-quality semantics.
- **Don't** use em-dashes (`U+2014`) in UI labels, headers, tooltips, or analytical copy.
- **Don't** hide native Streamlit radio label containers with aggressive `:first-of-type` CSS overrides that break accessible labels.
