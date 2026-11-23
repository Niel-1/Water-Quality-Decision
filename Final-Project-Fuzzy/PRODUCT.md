# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary users are Universitas Udayana Computer Science lecturers evaluating the Final Project during live class presentations, and Kelompok 1 students demonstrating and exploring the hybrid Fuzzy Mamdani + K-Nearest Neighbor (KNN) water potability system interactively.

## Product Purpose

The application is an interactive, white-box Water Quality & Potability Decision Support System built in Streamlit. It makes every step of the hybrid pipeline transparent and verifiable: physicochemical input entry (`ph`, `Hardness`, `Turbidity`), 27-rule Ruspini triangular Fuzzy Mamdani inference with exact piecewise-linear analytic centroid defuzzification (`fuzzy_quality_score` in `[0, 100]`), leakage-free Min-Max/Z-Score scaling, Euclidean KNN classification (`Potable` vs `Not Potable`), full-dataset batch scoring, and head-to-head Model A (3-feature Baseline KNN) vs Model B (4-feature Fuzzy-Enhanced KNN) evaluation.

Success means a lecturer or student can live-demo presets (`S1`–`S5`, `Q*`) or custom values during presentation, audit every intermediate number to 4 decimal places (`0.0000`) against manual calculus calculations without visual clutter, upload a custom CSV, and inspect Model A vs Model B accuracy gains across `K = 3, 5, 7, 9, 11`.

## Positioning

A fully transparent, from-scratch white-box computational workbench where exact piecewise-linear analytic centroid integration produces zero discrepancy (`0.0000`) against hand-calculated report derivations, paired directly with leakage-free KNN verification against `scikit-learn`.

## Operating Context

- Presented live on classroom projectors and laptop screens during course evaluation for Teknologi Logika Fuzzy (Program Studi Informatika, FMIPA Universitas Udayana).
- Used alongside the Kelompok 1 written report and manual calculation reference samples (`S1`–`S5` and query sample `Q*`).
- Runs locally via `streamlit run app.py` using Python 3, Streamlit, Plotly, NumPy, Pandas, and scikit-learn.

## Capabilities and Constraints

- Preserve all 6 pages in Bahasa Indonesia:
  1. Halaman Utama (Dashboard)
  2. Input Data & Eksplorasi Dataset (single-sample simulator with `S1`–`S5`/`Q*` presets + Kaggle dataset exploration & CSV upload)
  3. Proses Pengolahan (White-Box Step-by-Step: 4 membership function charts, fuzzification table, 27-rule evaluation with active filter, aggregated centroid curve, analytic piecewise integral table, Min-Max scaling & Euclidean KNN neighbor table)
  4. Hasil Pengolahan & Klasifikasi Kelayakan (filterable full-dataset ranking, Potable/Not Potable counts, CSV download, score histogram & physicochemical scatter)
  5. Evaluasi Sistem (Model A vs Model B head-to-head across `K = 3, 5, 7, 9, 11`, split strategy & scaler selectors, sensitivity charts, side-by-side Confusion Matrices, per-class metrics)
  6. Informasi Sistem & Petunjuk Penggunaan (LaTeX mathematical formulations, complete 27-rule base table, user manual)
- Preserve all backend APIs in `src/fuzzy_mamdani.py` and `src/knn_model.py` untouched so all existing automated tests (`pytest`) pass.
- Preserve 4-decimal numerical precision (`0.0000`) across all calculation tables and metrics.
- Avoid flat white generic dashboard styling and low-transparency pale green boxes (explicit user rejection of the prior visual design).
- Avoid em-dashes (`—`) in user-facing UI copy.
- Rewrite the monolithic GUI codebase cleanly into modular, maintainable Python modules under `src/ui/` with `app.py` as a clean entrypoint.

## Brand Commitments

- Project Identity: Water Quality & Potability Decision Support System, Kelompok 1, Teknologi Logika Fuzzy, Program Studi Informatika, FMIPA Universitas Udayana.
- Team members: Nathanael Adrian Wattimena (`2408561013`), I Wayan Arya Adi Guna (`2408561019`), Komang Dhika Artika Nurdi (`2408561055`), Kadek Phatra Adisuta Timonuli (`2408561076`), I Putu Maichail Ganio Wijaya (`2408561123`).
- Course Lecturer: Dr. Made Agung Raharja, S.Si., M.Cs.

## Evidence on Hand

- Clean balanced dataset: `data/processed/water_potability_clean.csv` (600 observations: 300 Potable, 300 Not Potable; derived from Kaggle `adityakadiwal/water-potability`, 3,276 raw rows).
- Manual calculation reference dataset: `data/processed/manual_calc_sample.csv` (`S1`–`S5`).
- Verified white-box engines: `src/fuzzy_mamdani.py`, `src/knn_model.py`, and test suite `tests/test_system.py` (5/5 passing).
- Do not fabricate external clinical certifications, real-time IoT sensor feeds, or third-party endorsements.

## Product Principles

1. **White-box clarity first:** Every intermediate fuzzy membership, rule firing strength, integral segment, and KNN distance must remain effortless to scan and verify at 4-decimal precision.
2. **Presentation-ready hierarchy:** Key verdicts, active simulation parameters, and Model B gains must read clearly at a glance on both laptop screens and classroom projectors.
3. **Standard, trustworthy controls:** Filters, sliders, tables, tabs, and navigation must behave like dependable analytical software without novelty chrome or visual noise.
4. **Clean modular engineering:** Keep UI presentation, Plotly chart theming, cached data pipelines, and page views cleanly separated from mathematical core modules.

## Accessibility & Inclusion

- High contrast text and data readability (WCAG AA minimum, crisp contrast for projector viewing and dark/tonal surfaces).
- Strict tabular numerals (`tabular-nums`) for all numbers, coordinates, metrics, and calculation tables.
- Color is never the sole indicator of `Potable` vs `Not Potable` or `Good` / `Moderate` / `Poor` status; explicit text labels always accompany semantic color cues.
