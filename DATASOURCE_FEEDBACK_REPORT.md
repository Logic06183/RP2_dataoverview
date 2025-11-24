# RP2 Clinical Dataset - Data Quality Feedback Report

**Date**: 2025-11-24
**Reviewer**: Data Quality Team
**Purpose**: Feedback to data sources for corrections in JupyterHub

---

## Executive Summary

We have completed a comprehensive quality review of all 17 studies in the RP2 Clinical Dataset collection. **Critical data extraction failures** were identified in **6 ACTG studies**, affecting 605 participants (23% of the cohort). These datasets are currently **unusable for clinical analysis** and require **immediate re-extraction**.

### Overall Findings

- **Total Studies Reviewed**: 17
- **Usable Studies**: 10 (59%)
- **Studies with Critical Failures**: 7 (41%)
  - 6 ACTG studies with extraction failures
  - 1 study (VIDA_008) with calculation errors
- **Study Recommended for Exclusion**: 1 (JHB_JHSPH_005 - adverse events data, not clinical outcomes)
- **Total Data Quality Issues**: 65+

### Urgency Levels

🔴 **CRITICAL (7 studies)**: Dataset unusable - requires immediate action
🟡 **High Priority (10 studies)**: Data quality issues that must be fixed before analysis
🟢 **Medium/Low Priority (10 studies)**: Issues to address before publication

---

## CRITICAL Priority Issues (Immediate Action Required)

### 🔴 ACTG Studies Cohort - SYSTEMATIC EXTRACTION FAILURE

**Affected Studies**: ALL 6 ACTG studies (JHB_ACTG_015, 016, 017, 018, 019, 021)
**Total Participants Affected**: 605 (23% of entire cohort)
**Severity**: CATASTROPHIC - Datasets completely unusable

#### Problem Description

All six ACTG studies have **systematic data extraction failures** with identical patterns:

1. **Core demographic variables 100% missing**:
   - Age: 100% missing in 5 of 6 ACTG studies
   - CD4 count: 100% missing in 4 of 6 ACTG studies
   - HIV viral load: Missing or constant values (all = 400)
   - Creatinine: 100% missing

2. **Laboratory values using numeric missing codes**:
   - ALT: All values = 1.0 (impossible - normal range 7-56 U/L)
   - Platelet count: All values = 3.0 across multiple studies
   - HIV viral load: All values = 400.0 (detection threshold used as missing code)

3. **Complete absence of clinical data**:
   - ACTG_017: Only administrative data (patient ID, dates, location)
   - ACTG_018: ALL 6 lab variables 100% missing for 240 participants
   - ACTG_021: No clinical/lab data - only follow-up tracking

4. **Impossible physiological values**:
   - Hematocrit: Minimum = 0.00% (impossible for living participants)

#### Required Action

**URGENT RE-EXTRACTION REQUIRED** for all 6 ACTG studies from source databases:

- Verify source data availability for core variables
- Identify and properly handle missing data (code as NA, not numeric codes)
- Extract complete laboratory panels
- Verify age/demographic data extraction
- Confirm treatment arm and study completion status

**Impact if not fixed**: Loss of 605 participants (23% of cohort) and inability to include ACTG trials in any analysis.

---

### 🔴 JHB_VIDA_008 - BMI Calculation Catastrophe

**Study**: JHB_VIDA_008
**Participants Affected**: 557
**Severity**: CRITICAL - Primary outcome measure unusable

#### Problem Description

BMI values are **completely invalid** with impossible extreme values:
- Mean BMI = 1,601.42 (normal 18.5-25)
- Maximum BMI = 850,000 (physiologically impossible)
- Standard deviation = 36,543 (indicates extreme outliers)

**Likely causes**:
1. Missing data code (850,000) not recoded to NA
2. Calculation error (wrong units for height/weight in formula)
3. Data entry errors (missing decimal points)
4. Source data corruption

**Contributing issues**:
- Height minimum = 0.01m (1 centimeter - impossible)
- Decimal/unit mixing causing calculation errors

#### Required Action

1. **Urgent investigation** of BMI calculation methodology
2. Identify and recode missing codes (values >200 to NA)
3. Verify height data (recode values <1.0m to NA)
4. Recalculate BMI from source height/weight OR
5. Re-extract BMI directly from source database

**Impact if not fixed**: Loss of anthropometric analysis capability for 557-participant COVID-19 healthcare worker study.

---

## High Priority Issues (Must Fix Before Analysis)

### 1. Missing Data Codes Disguised as Valid Values

**Affected Studies**: 8 studies
**Issue**: Numeric codes used for missing data, inflating means and invalidating statistical analysis

| Study | Variable | Code | Action Required |
|-------|----------|------|-----------------|
| JHB_Aurum_009 | CD4 count | 9999 | Recode to NA |
| JHB_Aurum_009 | HIV viral load | 99999999 | Recode to NA |
| JHB_WRHI_001 | HIV viral load | 10000001 | Recode to NA |
| JHB_EZIN_002 | HIV viral load | 9475772 | Investigate threshold, recode >10M to NA |
| JHB_ACTG_015/016/019 | ALT | 1.0 | Verify if missing code, recode |
| JHB_ACTG_015/016/019 | Platelet count | 3.0 | Verify if missing code, recode |
| JHB_ACTG_016 | HIV viral load | 400.0 | Detection threshold - clarify meaning |

**Impact**: Inflated means, huge SDs, invalid statistical analyses. Example: CD4 mean = 687 vs median = 425 due to 9999 codes.

**Action**: Systematically identify and recode all numeric missing codes to NA across all studies.

---

### 2. Unit Conversion Errors

#### JHB_DPHRU_013 - Waist Circumference

**Issue**: Values in millimeters instead of centimeters
**Current**: Mean = 893.62 cm (8.9 meters!), Max = 9,150 cm (91.5 meters!)
**Correct**: Mean should be 89.3 cm, Max = 91.5 cm
**Action**: Divide all 563 waist circumference values by 10
**Impact**: Affects ALL anthropometric analyses for this 784-participant study

#### JHB_WRHI_001 - Hematocrit Format Mixing

**Issue**: Mixing decimal (0.46) and percentage (46) formats
**Current**: Mean = 16.86, Median = 0.46, Max = 60.30
**Action**: Convert all values >1 to decimal format (divide by 100)
**Impact**: Critical for anemia/blood disorder analyses

---

### 3. Impossible/Zero Values (Physiologically Invalid)

**Issue**: Zero values in variables that cannot be zero for living participants

| Study | Variable | Min Value | Action |
|-------|----------|-----------|--------|
| JHB_DPHRU_053 | Hip/Waist circumference | 0.00 | Recode to NA |
| JHB_EZIN_002 | Heart rate | 0.00 bpm | Recode to NA |
| JHB_ACTG_015/016/019 | Hematocrit | 0.00% | Recode to NA |
| JHB_VIDA_008 | Height | 0.01m | Recode <1.0m to NA |

**Action**: Systematically identify and recode zero/impossible values to NA.

---

### 4. Variable Naming Errors

#### JHB_EZIN_002 & JHB_SCHARP_004 - Cell Count Mislabeling

**Issue**: Variables labeled "percentage" but contain absolute counts

**Examples**:
- "Lymphocyte percentage": Mean = 1.83 (matches absolute count 1-4 ×10⁹/L, NOT percentage)
- "Neutrophil percentage": Mean = 2.76 (matches absolute count, would be 276% if percentage)
- "Basophil percentage": Mean = 58.48 (impossible as percentage)

**Action**: **RENAME variables** to reflect absolute counts (×10⁹/L), do NOT multiply/divide values
**Impact**: Prevents misinterpretation of immune function data

---

## Medium Priority Issues (Fix Before Publication)

### 1. Near-Empty Variables (>95% Missing)

Remove or document rationale for keeping variables with minimal data:

| Study | Variable | Missing % | Records with Data | Action |
|-------|----------|-----------|-------------------|--------|
| JHB_WRHI_003 | Fasting glucose, alkaline phosphatase, LDH, transferrin, total protein | 100% | 0/300 | Remove |
| JHB_WRHI_003 | Albumin, calcium | 99.7% | 1/300 | Remove |
| JHB_SCHARP_006 | Syphilis test result | 96.5% | 16/451 | Remove or document |
| JHB_VIDA_008 | Hyperlipidemia | 99% | 5/557 | Remove |
| JHB_Aurum_009 | HIV viral load latest | 96.5% | N/A | Document if expected |

**Action**: Remove variables with <5% data unless there's documented research justification.

---

### 2. Unclear Variable Definitions

#### "Other Measures of Obesity"

**Affected Studies**: JHB_EZIN_025, JHB_WRHI_003

**Issue**: Vague variable name - values match BMI range but labeled ambiguously
- Mean ≈ 27, Range 17-45 (typical BMI distribution)
**Action**: Rename to "bmi" if appropriate, or clarify what "other measures" means

---

### 3. High Systematic Missingness

Document if missingness is protocol-driven or data quality issue:

| Study | Variable | Missing % | Action |
|-------|----------|-----------|--------|
| JHB_EZIN_025 | Anthropometric/vitals | 74.0% | Document if COVID-19 protocol issue |
| JHB_SCHARP_006 | Creatinine | 67.2% | Document if selective testing |
| JHB_VIDA_008 | HIV status | 48.1% | Document if optional collection |

---

### 4. Lipid Panel Extreme Outliers

**Study**: JHB_WRHI_001

**Issue**: Means vastly exceed medians, suggesting missing codes or unit errors

- HDL: Mean = 16.88, Median = 1.40 (12x difference)
- LDL: Mean = 40.02, Median = 3.10 (13x difference)
- Total cholesterol: Mean = 65.87, Median = 4.80 (14x difference)

**Action**: Identify and recode extreme outliers or missing codes pulling averages up.

---

## Low Priority Issues (Address When Convenient)

### 1. Patient ID Stored as Numeric

**Affected**: Multiple studies
**Issue**: Patient IDs treated as numeric variables (showing means, SDs)
**Action**: Convert to categorical/text type to prevent accidental calculations

### 2. Constant/Uninformative Variables

Variables with no variation provide no analytical value - consider removal:
- Treatment arm = "Unknown" for all records (ACTG studies)
- Study completion status = "Other" for all records
- Sex = all Female or all Unknown (single-sex studies)

### 3. Duplicate/Inconsistent Country Variables

**Study**: JHB_WRHI_003
**Issue**: "Country" (11 unique values) vs "country" (1 value)
**Action**: Investigate discrepancy and standardize

---

## Study Recommended for Exclusion

### JHB_JHSPH_005 - Adverse Events Registry

**Recommendation**: ⛔ **EXCLUDE from RP2 clinical dataset collection**

**Rationale**:
- Fundamentally different data type (adverse events, not clinical outcomes)
- Missing ALL core clinical variables (age, sex, biomarkers, vital signs, anthropometrics)
- Cannot be integrated with climate/health outcome analyses
- Should be maintained in separate adverse events database

**Action**: Remove from RP2 collection, update documentation, maintain separately if needed for safety surveillance.

---

## Recommended Actions Summary

### Immediate Actions (This Week)

1. ✅ **Re-extract all 6 ACTG studies** - Contact ACTG data source
2. ✅ **Investigate VIDA_008 BMI** - Urgent calculation review
3. ✅ **Fix waist circumference unit error** (DPHRU_013) - Simple division by 10

### Short-term Actions (This Month)

4. Systematically identify and recode all numeric missing codes to NA
5. Fix hematocrit format mixing (WRHI_001)
6. Recode all zero/impossible values to NA
7. Rename mislabeled cell count variables
8. Remove empty variables (<5% data)

### Medium-term Actions (Before Analysis)

9. Document high missingness patterns
10. Clarify vague variable definitions
11. Investigate and fix lipid panel outliers
12. Convert Patient IDs to categorical
13. Remove/document constant variables

### Before Publication

14. Final validation of all corrections
15. Update data dictionary with changes
16. Document exclusion of JHB_JHSPH_005

---

## Technical Contact Information

For questions about specific studies or data extraction issues, please contact:

**ACTG Studies**: [ACTG Data Coordinator Contact]
**VIDA Studies**: [VIDA Data Coordinator Contact]
**WRHI Studies**: [WRHI Data Coordinator Contact]
**DPHRU Studies**: [DPHRU Data Coordinator Contact]

**General Data Quality Questions**: [Primary Data Manager Contact]

---

## Appendix: Study-by-Study Issue Count

| Study | Critical | High | Medium | Low | Total | Status |
|-------|----------|------|--------|-----|-------|--------|
| JHB_ACTG_015 | 3 | 1 | 1 | 0 | 5 | ⚠️ CRITICAL |
| JHB_ACTG_016 | 3 | 1 | 0 | 0 | 4 | ⚠️ CRITICAL |
| JHB_ACTG_017 | 1 | 0 | 0 | 0 | 1 | ⚠️ CRITICAL |
| JHB_ACTG_018 | 1 | 0 | 0 | 0 | 1 | ⚠️ CRITICAL |
| JHB_ACTG_019 | 1 | 1 | 1 | 0 | 3 | ⚠️ CRITICAL |
| JHB_ACTG_021 | 1 | 0 | 0 | 0 | 1 | ⚠️ CRITICAL |
| JHB_Aurum_009 | 0 | 2 | 1 | 0 | 3 | ✅ Fixable |
| JHB_DPHRU_013 | 0 | 1 | 0 | 1 | 2 | ✅ Fixable |
| JHB_DPHRU_053 | 0 | 1 | 1 | 1 | 3 | ✅ Fixable |
| JHB_EZIN_002 | 0 | 3 | 1 | 1 | 5 | ✅ Fixable |
| JHB_EZIN_025 | 0 | 0 | 2 | 1 | 3 | ✅ Fixable |
| JHB_JHSPH_005 | 0 | 0 | 0 | 0 | N/A | ⛔ Exclude |
| JHB_SCHARP_004 | 0 | 2 | 2 | 1 | 5 | ✅ Fixable |
| JHB_SCHARP_006 | 0 | 1 | 1 | 2 | 4 | ✅ Fixable |
| JHB_VIDA_007 | 0 | 1 | 2 | 1 | 4 | ✅ Fixable |
| JHB_VIDA_008 | 1 | 2 | 1 | 1 | 5 | ⚠️ CRITICAL |
| JHB_WRHI_001 | 0 | 3 | 1 | 1 | 5 | ✅ Fixable |
| JHB_WRHI_003 | 0 | 0 | 4 | 1 | 5 | ✅ Fixable |

---

**Report Generated**: 2025-11-24
**Next Review**: After corrections implemented
**Contact**: [Your contact information]
