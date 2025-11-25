# RP2 Clinical Dataset - Quality Check Report

**Generated:** November 25, 2025
**Dataset:** CLINICAL_DATASET_QUALITY_HARMONIZED.csv
**Total Records:** 11,026 across 17 studies

---

## Executive Summary

Quality check identified **8 potential issues** affecting 984 records (8.92% of dataset). The most significant issue is abnormally high albumin values (943 records, 8.55%), which may indicate a unit conversion error. Other issues are minor and affect <1% of records.

**Good News:**
- **No CD4 counts = 0 found** (previous concern has been resolved)
- No zero values in hematology parameters
- Most biomarkers are within physiologically plausible ranges

---

## Priority Issues for Data Source Review

### 🔴 HIGH PRIORITY

#### 1. Albumin Values > 6 g/dL
- **Records affected:** 943 (8.55% of dataset)
- **Normal range:** 3.5-5.5 g/dL
- **Issue:** Values consistently >6 suggest possible unit error (mg/dL vs g/dL) or data extraction problem
- **Studies affected:** JHB_DPHRU_053, JHB_WRHI_003, others
- **Recommendation:** Review source data for unit specification or extraction logic

---

### 🟡 MEDIUM PRIORITY

#### 2. HIV Viral Load Patterns

**a. Viral Load = 0 (423 records, 3.84%)**
- **Interpretation:** Could indicate:
  - Undetectable viral load (clinically valid for patients on ART)
  - Missing data coded as zero
  - Data entry/extraction error
- **Recommendation:** Verify if zero represents "undetectable" or missing data

**b. Viral Load > 1,000,000 copies/mL (13 records, 0.12%)**
- **Interpretation:** Unusually high but physiologically possible in treatment-naïve patients
- **Studies affected:** JHB_Ezin_002, others
- **Recommendation:** Verify these values against source records

#### 3. CD4 Count > 2,000 cells/µL
- **Records affected:** 3 (0.03%)
- **Normal range:** 500-1,500 cells/µL
- **Study affected:** JHB_Aurum_009
- **Recommendation:** Verify against source - possible but rare

---

### 🟢 LOW PRIORITY (Minor Issues)

#### 4. Waist Circumference Extremes
- **< 40 cm:** 3 records (0.03%) - Study: JHB_DPHRU_013
- **> 200 cm:** 1 record (0.01%) - Study: JHB_DPHRU_013
- **Recommendation:** Review individual records - likely data entry errors

#### 5. Blood Pressure Extremes
- **Systolic BP > 250 mmHg:** 1 record (0.01%) - Study: JHB_DPHRU_053
- **Diastolic BP < 40 mmHg:** 1 record (0.01%) - Study: JHB_Ezin_002
- **Recommendation:** Review individual records

---

## Informational Findings (Not Issues)

### CD4 Count < 50 cells/µL
- **Records:** 1,078 (9.77%)
- **Interpretation:** Severe immunosuppression - **clinically valid** for HIV cohorts
- **No action needed**

### Viral Load = 0
- **Records:** 423 (3.84%)
- **Interpretation:** Likely represents undetectable viral load in patients on effective ART
- **Action needed:** Clarify coding convention (zero vs. missing vs. "undetectable")

---

## Variables with No Issues Detected

✅ **Hematology:** No zero values in hematocrit, hemoglobin, WBC, RBC, platelets
✅ **CD4 Counts:** No zero values, no obvious missing codes
✅ **Liver Enzymes (ALT, AST):** Values within expected ranges
✅ **Creatinine:** No suspicious values
✅ **Anthropometrics (BMI, Weight, Height):** Within physiological ranges
✅ **Heart Rate:** No zero values, reasonable ranges
✅ **Temperature:** Reasonable ranges

---

## Recommended Actions

### For Data Manager

1. **Albumin Unit Error (HIGH)**
   - Investigate DPHRU_053 and WRHI_003 albumin extraction
   - Check if source data specifies units (g/dL vs mg/dL vs g/L)
   - If units are wrong, divide by 10 (if g/L) or multiply by correct conversion

2. **Viral Load Coding (MEDIUM)**
   - Document whether VL=0 means "undetectable" or "missing"
   - Consider coding undetectable as a separate category or using detection limit (e.g., <20 copies/mL)

3. **Individual Value Verification (LOW)**
   - Review 3 CD4 > 2000 records against source
   - Review 4 waist circumference extremes
   - Review 2 BP extremes

### For Analysts Using This Dataset

1. **Exclude/Handle Albumin Carefully**
   - Do NOT use albumin values until unit issue is resolved
   - Flag these records in analysis

2. **Viral Load = 0**
   - Treat as "undetectable" rather than numeric zero in analyses
   - Consider censoring at detection limit

3. **CD4 < 50**
   - These are valid data - severe immunosuppression is expected in HIV cohorts
   - No exclusion needed

---

## Quality Report Files

- **Summary CSV:** `QUALITY_CHECK_REPORT.csv`
- **Quality Check Script:** `quality_check.py`
- **This Report:** `CURRENT_QUALITY_REPORT.md`

---

## Comparison to Previous Quality Issues

### ✅ **RESOLVED ISSUES** (from previous corrections):
- CD4 counts = 9999, 99999 → Removed
- Viral load = 99999999, 10000001 → Removed
- ALT = 1.0 (missing code) → Removed
- Platelet = 3.0 (missing code) → Removed
- Waist circumference mm→cm conversion → **Fixed**
- BMI extreme values (>200) → Removed
- Hematocrit = 0 → Removed
- Heart rate = 0 → Removed

### 🆕 **NEW ISSUES IDENTIFIED**:
- Albumin > 6 g/dL (possible unit error)
- A few extreme values in waist, BP (likely data entry errors)

---

## Contact

For questions about this quality report or to provide feedback on identified issues:
- **Data Owner:** [Your contact information]
- **Quality Check Date:** November 25, 2025
- **Dataset Version:** Production v2.0
