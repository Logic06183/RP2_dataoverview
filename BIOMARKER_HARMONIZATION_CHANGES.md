# Biomarker Harmonization Change Log

**Date**: 2025-11-25 08:06:43
**Input**: CLINICAL_DATASET_QUALITY_HARMONIZED.csv
**Output**: CLINICAL_DATASET_BIOMARKERS_HARMONIZED.csv

---

## Changes Applied

**Total Changes**: 49

### 1. Lipid Panel Unit Corrections

- Renamed: hdl_cholesterol_mg_dL → hdl_cholesterol_mmol_L
- Renamed: ldl_cholesterol_mg_dL → ldl_cholesterol_mmol_L
- Renamed: total_cholesterol_mg_dL → total_cholesterol_mmol_L
- Renamed: Triglycerides (mg/dL) → triglycerides_mmol_L

### 2. Column Consolidations

- Consolidated 3 columns into neutrophil_count_10e9_L: 1365 records
- Consolidated 3 columns into lymphocyte_count_10e9_L: 1370 records
- Consolidated 2 columns into monocyte_count_10e9_L: 1269 records
- Consolidated 2 columns into eosinophil_count_10e9_L: 1269 records
- Consolidated 2 columns into basophil_count_10e9_L: 1269 records
- Consolidated 2 columns into mcv_fL: 1269 records
- Consolidated 2 columns into hdl_cholesterol_mmol_L_consolidated: 2918 records
- Consolidated 2 columns into ldl_cholesterol_mmol_L_consolidated: 2917 records
- Consolidated 2 columns into triglycerides_mmol_L_consolidated: 972 records

### 3. Standardized Column Names

- Standardized: RDW → rdw_percent
- Standardized: creatinine clearance → creatinine_clearance_mL_min
- Standardized: Potassium (mEq/L) → potassium_mEq_L
- Standardized: Sodium (mEq/L) → sodium_mEq_L
- Standardized: CD4 cell count (cells/µL) → cd4_count_cells_uL
- Standardized: HIV viral load (copies/mL) → hiv_vl_copies_mL
- Standardized: Antiretroviral Therapy Status → art_status
- Standardized: White blood cell count (×10³/µL) → wbc_count_10e9_L
- Standardized: Hematocrit (%) → hematocrit_percent
- Standardized: Platelet count (×10³/µL) → platelet_count_10e9_L
- Standardized: ALT (U/L) → alt_U_L
- Standardized: AST (U/L) → ast_U_L
- Standardized: Albumin (g/dL) → albumin_g_dL
- Standardized: Total protein (g/dL) → total_protein_g_dL
- Standardized: Alkaline phosphatase (U/L) → alkaline_phosphatase_U_L
- Standardized: Total bilirubin (mg/dL) → total_bilirubin_mg_dL

### 4. Removed Duplicate Columns

- Removed duplicate: Neutrophil count (×10⁹/L)
- Removed duplicate: Neutrophil count (×10³/µL)
- Removed duplicate: Lymphocyte count (×10³/µL)
- Removed duplicate: FASTING LDL
- Removed duplicate: FASTING HDL
- Removed duplicate: Lymphocyte count (×10⁹/L)
- Removed duplicate: Monocyte count (×10⁹/L)
- Removed duplicate: Neutrophil count (×10⁹/L).1
- Removed duplicate: Eosinophil count (×10⁹/L).1
- Removed duplicate: FASTING TRIGLYCERIDES
- Removed duplicate: Basophil count (×10⁹/L)
- Removed duplicate: Monocyte count (×10⁹/L).1
- Removed duplicate: triglycerides_mmol_L
- Removed duplicate: Basophil count (×10⁹/L).1
- Removed duplicate: Eosinophil count (×10⁹/L)
- Removed duplicate: Lymphocyte count (×10⁹/L).1
- Removed duplicate: hdl_cholesterol_mmol_L
- Removed duplicate: MCV (MEAN CELL VOLUME)
- Removed duplicate: ldl_cholesterol_mmol_L
- Removed duplicate: Mean corpuscular volume (fL)

---

## Final Biomarker Summary

| Category | Available | Total | Coverage |
|----------|-----------|-------|----------|
| HIV Markers | 3 | 3 | 100.0% |
| Hematology | 13 | 13 | 100.0% |
| Liver Function | 4 | 6 | 66.7% |
| Renal Function | 2 | 2 | 100.0% |
| Electrolytes | 1 | 2 | 50.0% |
| Lipids | 4 | 4 | 100.0% |
| Metabolic | 1 | 1 | 100.0% |

**TOTAL**: 28/31 biomarkers available (90.3%)
