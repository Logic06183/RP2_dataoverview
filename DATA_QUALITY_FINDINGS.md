# Data Quality Findings & Action Items

**Review Date**: 2025-11-24
**Reviewer**: [Your Name]
**Purpose**: Systematic review of RP2 clinical dataset quality reports to identify anomalies for correction in JupyterHub

---

## Review Status

| Study | Status | Priority Issues | Reviewed Date |
|-------|--------|-----------------|---------------|
| JHB_ACTG_015 | ⚠️ CRITICAL | CATASTROPHIC - Core variables 100% missing | 2025-11-24 |
| JHB_ACTG_016 | ⚠️ CRITICAL | SYSTEMATIC FAILURE - Same as 015 | 2025-11-24 |
| JHB_ACTG_017 | ⚠️ CRITICAL | FAILED EXTRACTION - Only admin data | 2025-11-24 |
| JHB_ACTG_018 | ⚠️ CRITICAL | ALL LAB VALUES 100% MISSING | 2025-11-24 |
| JHB_ACTG_019 | ⚠️ CRITICAL | SYSTEMATIC PROBLEMS - Missing codes | 2025-11-24 |
| JHB_ACTG_021 | ⚠️ CRITICAL | EXTRACTION FAILURE - No clinical data | 2025-11-24 |
| JHB_Aurum_009 | ✅ Reviewed | 2 high, 1 medium | 2025-11-24 |
| JHB_DPHRU_013 | ✅ Reviewed | 1 high (waist circ unit error) | 2025-11-24 |
| JHB_DPHRU_053 | ✅ Reviewed | 1 high, 1 medium, 1 low | 2025-11-24 |
| JHB_EZIN_002 | ✅ Reviewed | 3 high, 1 medium, 1 low | 2025-11-24 |
| JHB_EZIN_025 | ✅ Reviewed | 2 medium, 1 low | 2025-11-24 |
| JHB_JHSPH_005 | ⛔ EXCLUDE | Adverse events only - incompatible | 2025-11-24 |
| JHB_SCHARP_004 | ✅ Reviewed | 2 high, 2 medium, 1 low | 2025-11-24 |
| JHB_SCHARP_006 | ✅ Reviewed | 1 high, 1 medium, 2 low | 2025-11-24 |
| JHB_VIDA_007 | ✅ Reviewed | 1 high, 2 medium, 1 low | 2025-11-24 |
| JHB_VIDA_008 | ⚠️ CRITICAL | 1 critical, 2 high, 1 med, 1 low | 2025-11-24 |
| JHB_WRHI_001 | ✅ Reviewed | 3 high, 1 medium, 1 low | 2025-11-24 |
| JHB_WRHI_003 | ✅ Reviewed | 4 medium, 1 low | 2025-11-24 |

---

## Quality Check Categories

### 1. Missing Data Issues
**What to look for:**
- Unusual patterns of missing data (systematic missingness)
- Critical variables with >20% missing
- Variables that should never be missing but are

**Findings:**

---

### 2. Outliers & Anomalous Values
**What to look for:**
- Biologically implausible values (e.g., negative ages, BMI > 100)
- Statistical outliers that seem data entry errors
- Values outside expected ranges

**Findings:**

---

### 3. Distribution Issues
**What to look for:**
- Unexpected distribution shapes (e.g., bimodal when should be normal)
- Suspicious clustering of values (repeated entry errors)
- Zero-inflation or ceiling/floor effects

**Findings:**

---

### 4. Categorical Variable Issues
**What to look for:**
- Unexpected categories or misspellings
- Implausible category frequencies
- Missing category labels

**Findings:**

---

### 5. Consistency Issues
**What to look for:**
- Temporal inconsistencies (dates out of order)
- Logical inconsistencies (pregnant males, etc.)
- Duplicate records
- Conflicting values across related variables

**Findings:**

---

### 6. Study-Specific Concerns
**What to look for:**
- Sample size issues (too small for meaningful analysis)
- Recruitment period anomalies
- Protocol deviations

**Findings:**

---

## Detailed Findings by Study

### JHB_ACTG_015
**Report**: `JHB_ACTG_015_profile.html`
**Status**: ⚠️ CRITICAL - Reviewed on 2025-11-24

**SEVERE DATA EXTRACTION PROBLEMS**

**Issues Found:**

- [ ] Issue: Core HIV variables completely missing (100%)
  - **Priority**: CRITICAL
  - **Variable(s)**: age, cd4_count, hiv_viral_load, hiv_viral_load_suppression, creatinine
  - **Action**: Urgent re-extraction needed - these are fundamental variables for HIV cohort
  - **Status**: To Do
  - **Notes**: All 5 key variables have 100% missing (N=0)
    - Age is missing for ALL 87 participants (impossible for enrollment data)
    - CD4 count is completely absent (essential for HIV cohort)
    - HIV viral load completely missing (primary outcome measure)
    - These are NOT missingness issues - data was never extracted
    - **Dataset is essentially unusable without these variables**
    - Requires immediate data source investigation

- [ ] Issue: ALT and Platelet count using numeric missing codes (constant values)
  - **Priority**: CRITICAL
  - **Variable(s)**: alt, platelet_count
  - **Action**: Investigate why ALT = 1.0 and Platelet = 3.0 for ALL records
  - **Status**: To Do
  - **Notes**: ALT: All 87 records = 1.0 (mean = 1.0, SD = 0.0)
    - Platelet: All 87 records = 3.0 (mean = 3.0, SD = 0.0)
    - These are likely missing data codes or unit errors
    - ALT of 1.0 U/L is impossibly low (normal 7-56 U/L)
    - Platelet of 3.0 could be 3 ×10³/µL (severe thrombocytopenia) or missing code
    - Need to verify with source data

- [ ] Issue: Hematocrit contains zero values (impossible)
  - **Priority**: High
  - **Variable(s)**: hematocrit
  - **Action**: Recode hematocrit = 0 to NA/missing
  - **Status**: To Do
  - **Notes**: Min = 0.00% (impossible for living participants)
    - Mean = 27.82%, SD = 17.86 (huge variation suggests mixed data)
    - Zero hematocrit is physiologically impossible
    - High SD indicates possible mixing of percentage and decimal formats
    - Check how many records have hematocrit = 0

- [ ] Issue: Multiple constant administrative variables
  - **Priority**: Low
  - **Variable(s)**: treatment_arm (all "Unknown"), study_completion_status (all "Other"), study_week (all 0)
  - **Action**: Document incomplete data extraction or protocol issues
  - **Status**: To Do
  - **Notes**: Treatment arm completely unknown for all 87 participants
    - Study completion status uninformative (all "Other")
    - All records at study_week 0 (baseline only?)
    - Suggests incomplete or problematic data extraction

**OVERALL ASSESSMENT**: This dataset has **CATASTROPHIC data quality issues**. Core HIV variables (age, CD4, viral load) are completely absent. Several lab values appear to be missing codes (ALT=1, Platelet=3). Dataset requires urgent re-extraction from source and cannot be used for analysis in current state.

---

### JHB_ACTG_016
**Report**: `JHB_ACTG_016_profile.html`
**Status**: ⚠️ CRITICAL - Reviewed on 2025-11-24

**SAME SYSTEMATIC DATA EXTRACTION PROBLEMS AS ACTG_015**

**Issues Found:**

- [ ] Issue: Core HIV variables completely missing (100%) - SAME AS ACTG_015
  - **Priority**: CRITICAL
  - **Variable(s)**: age, cd4_count, hiv_viral_load_suppression, creatinine
  - **Action**: Systematic re-extraction needed across ALL ACTG studies
  - **Status**: To Do
  - **Notes**: Same pattern as ACTG_015 - fundamental variables absent
    - Age: 100% missing (N=0) for all 78 records
    - CD4 count: 100% missing (essential for HIV cohort)
    - Viral load suppression: 100% missing
    - **This is a SYSTEMATIC extraction issue affecting multiple ACTG studies**

- [ ] Issue: HIV viral load constant at detection threshold (likely missing code)
  - **Priority**: CRITICAL
  - **Variable(s)**: hiv_viral_load
  - **Action**: Investigate why ALL 78 records have viral_load = 400 copies/mL
  - **Status**: To Do
  - **Notes**: All records = 400.0 (mean = 400, SD = 0.0)
    - 400 copies/mL is a common assay detection threshold
    - This is likely either:
      1. Missing data code
      2. "Below detection limit" indicator
      3. Data extraction error where threshold was used for missing values
    - Cannot distinguish true viral loads from missing/undetectable

- [ ] Issue: ALT and Platelet count using numeric missing codes - SAME AS ACTG_015
  - **Priority**: CRITICAL
  - **Variable(s)**: alt (all = 1.0), platelet_count (all = 3.0)
  - **Action**: Same as ACTG_015 - verify these are missing codes
  - **Status**: To Do
  - **Notes**: Identical pattern to ACTG_015
    - Suggests systematic use of numeric codes for missing data
    - Needs source data verification and recoding to NA

- [ ] Issue: Hematocrit contains zeros - SAME AS ACTG_015
  - **Priority**: High
  - **Variable(s)**: hematocrit (min = 0.00)
  - **Action**: Recode zeros to NA
  - **Status**: To Do

**OVERALL ASSESSMENT**: **SYSTEMATIC DATA EXTRACTION FAILURE** across ACTG studies. Same critical variables missing as ACTG_015. Urgent source data review needed for entire ACTG cohort.

---

### JHB_ACTG_017
**Report**: `JHB_ACTG_017_profile.html`
**Status**: ⚠️ CRITICAL - Reviewed on 2025-11-24

**EXTREMELY MINIMAL DATA EXTRACTION**

**Issues Found:**

- [ ] Issue: Only 3 numeric variables extracted (geographic coordinates + Patient ID)
  - **Priority**: CRITICAL
  - **Variable(s)**: Only patient_id, latitude, longitude extracted
  - **Action**: Complete data re-extraction needed - no clinical data present
  - **Status**: To Do
  - **Notes**: This "extraction" captured ONLY:
    - Patient ID
    - Geographic coordinates (lat/long)
    - Administrative variables (country, province, site, visit_date)
    - **NO AGE, NO LAB VALUES, NO BIOMARKERS, NO CLINICAL DATA**
    - Dataset is completely unusable for any clinical analysis
    - Only 20 participants - smallest ACTG cohort

**OVERALL ASSESSMENT**: **FAILED EXTRACTION**. Only administrative/geographic data extracted. No clinical value.

---

### JHB_ACTG_018
**Report**: `JHB_ACTG_018_profile.html`
**Status**: ⚠️ CRITICAL - Reviewed on 2025-11-24

**ALL LAB VALUES 100% MISSING**

**Issues Found:**

- [ ] Issue: ALL laboratory values completely missing (100%)
  - **Priority**: CRITICAL
  - **Variable(s)**: ALT, AST, hematocrit, hemoglobin, platelet_count, wbc_count
  - **Action**: Complete data re-extraction needed for all lab values
  - **Status**: To Do
  - **Notes**: All 6 lab variables have 100% missing (N=0) for all 240 records
    - ALT: 100% missing
    - AST: 100% missing
    - Hematocrit: 100% missing
    - Hemoglobin: 100% missing
    - Platelet count: 100% missing
    - WBC count: 100% missing
    - Sex constant "Unknown" for all 240 participants
    - **Dataset has NO clinical/laboratory data - only administrative fields**

**OVERALL ASSESSMENT**: **CATASTROPHIC EXTRACTION FAILURE**. Largest ACTG cohort (240 participants) but ZERO lab data extracted.

---

### JHB_ACTG_019
**Report**: `JHB_ACTG_019_profile.html`
**Status**: ⚠️ CRITICAL - Reviewed on 2025-11-24

**SAME SYSTEMATIC ISSUES AS ACTG_015/016**

**Issues Found:**

- [ ] Issue: ALT and Platelet using numeric missing codes - SAME PATTERN
  - **Priority**: CRITICAL
  - **Variable(s)**: ALT (mean=1.12, range 1-2), platelet_count (all = 3.0)
  - **Action**: Same as other ACTG studies - verify and recode missing codes
  - **Status**: To Do
  - **Notes**: Nearly identical pattern to ACTG_015 and ACTG_016
    - ALT values suspiciously low (1.0-2.0) - likely missing codes
    - Platelet constant at 3.0 for ALL 102 records
    - **Systematic missing code problem across ACTG cohort**

- [ ] Issue: Hematocrit contains zeros - SAME AS ALL OTHER ACTG STUDIES
  - **Priority**: High
  - **Variable(s)**: hematocrit (min = 0.00)
  - **Action**: Recode zeros to NA
  - **Status**: To Do

- [ ] Issue: Sex constant "Unknown" for all 102 participants
  - **Priority**: Medium
  - **Variable(s)**: sex
  - **Action**: Extract actual sex data from source
  - **Status**: To Do

**OVERALL ASSESSMENT**: **SYSTEMATIC EXTRACTION PROBLEMS** consistent with entire ACTG cohort.

---

### JHB_ACTG_021
**Report**: `JHB_ACTG_021_profile.html`
**Status**: ⚠️ CRITICAL - Reviewed on 2025-11-24

**NO CLINICAL/LABORATORY DATA EXTRACTED**

**Issues Found:**

- [ ] Issue: Only administrative/follow-up data extracted - no clinical variables
  - **Priority**: CRITICAL
  - **Variable(s)**: Missing ALL: age, lab values, biomarkers, clinical measures
  - **Action**: Complete data re-extraction needed
  - **Status**: To Do
  - **Notes**: Only 6 numeric variables extracted:
    - Patient ID
    - Geographic coordinates (lat/long)
    - Neurological assessment flag (constant = 1)
    - Study week (constant = 0)
    - Total follow-up weeks (only meaningful variable: mean=173 weeks)
    - **NO clinical/lab data extracted at all**
    - **Dataset unusable for clinical analysis**
    - 78 participants with only administrative metadata

**OVERALL ASSESSMENT**: **EXTRACTION FAILURE**. Only administrative tracking data present. No clinical utility.

---

### JHB_Aurum_009
**Report**: `JHB_Aurum_009_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: CD4 counts using 9999 as missing data code instead of NA
  - **Priority**: High
  - **Variable(s)**: cd4_count, cd4_art_start, cd4_enrollment, cd4_latest
  - **Action**: Recode all values = 9999 to NA/missing. This affects ALL CD4 variables.
  - **Status**: To Do
  - **Notes**: Max values show 9999 across all CD4 variables. This is causing:
    - Inflated means (CD4 mean = 687.85 vs median = 425)
    - Huge SD (1490.34 - completely unrealistic)
    - Will invalidate any statistical analysis using these variables
    - Check if other numeric missing codes exist (e.g., -999, 999)

- [ ] Issue: HIV viral load using 99999999 as missing data code
  - **Priority**: High
  - **Variable(s)**: hiv_viral_load, hiv_viral_load_latest
  - **Action**: Recode all values = 99999999 to NA/missing
  - **Status**: To Do
  - **Notes**: Max = 99,999,999 causing absurd means (12.5 million!). Median = 1.00 suggests most values are either undetectable or missing codes.

- [ ] Issue: High missingness on key HIV variables
  - **Priority**: Medium
  - **Variable(s)**: hiv_viral_load_latest (96.5% missing), cd4_lowest (87.6%), cd4_latest (87.6%), hiv_viral_load (84.0%)
  - **Action**: Document why these variables have such high missingness. Are these truly missing or data extraction issues?
  - **Status**: To Do
  - **Notes**: Some missingness expected for ART-specific variables in mixed cohort, but >80% is concerning for analysis validity.

---

### JHB_DPHRU_013
**Report**: `JHB_DPHRU_013_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Waist circumference in millimeters instead of centimeters (SYSTEMATIC UNIT ERROR)
  - **Priority**: High
  - **Variable(s)**: waist_circumference
  - **Action**: Divide all values by 10 to convert mm to cm
  - **Status**: To Do
  - **Notes**: Current values: Mean = 893.62cm (8.9m!), Max = 9150cm (91.5m!)
    - After conversion: Mean = 89.3cm, Max = 91.5cm (reasonable)
    - This affects ALL 563 non-missing waist circumference values systematically
    - Standard deviation also absurdly high (382.57) due to unit error
    - **This is the main critical issue in this dataset**

- [ ] Issue: Moderate missingness on anthropometric measures
  - **Priority**: Low
  - **Variable(s)**: height, weight, waist_circumference, blood_pressure (all 28.2% missing)
  - **Action**: Document if missingness pattern is systematic (e.g., specific visits)
  - **Status**: To Do
  - **Notes**: All anthropometric variables have identical 28.2% missing
    - Suggests these were not collected at certain timepoints
    - Verify this is expected given longitudinal study design

---

### JHB_DPHRU_053
**Report**: `JHB_DPHRU_053_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Zero values in anthropometric measurements (impossible values)
  - **Priority**: High
  - **Variable(s)**: hip_circumference, waist_circumference
  - **Action**: Recode values = 0 to NA/missing for both variables
  - **Status**: To Do
  - **Notes**: Hip circ min = 0.00, Waist circ min = 0.00
    - Zero is impossible for living humans - these are missing data codes or entry errors
    - Means/medians are reasonable (106cm, 95cm) so zeros are outliers
    - Check how many records affected before recoding

- [ ] Issue: Total protein with extreme high values
  - **Priority**: Medium
  - **Variable(s)**: total_protein
  - **Action**: Investigate max value (261.25) and verify units/plausibility
  - **Status**: To Do
  - **Notes**: Normal range 60-80 g/L, max = 261.25 is extreme
    - Median = 48.98 is actually LOW (should be 60-80)
    - Large SD (26.78) suggests heterogeneity or unit issues
    - May need unit conversion or outlier removal

- [ ] Issue: Harmonization metadata variables in analysis dataset
  - **Priority**: Low
  - **Variable(s)**: heat_completeness, harmonization_version, harmonization_date
  - **Action**: Decide if these metadata variables should remain in analysis datasets
  - **Status**: To Do
  - **Notes**: These are not original study variables but harmonization tracking metadata
    - heat_completeness varies across studies (0.87-1.00)
    - May be useful for QC but redundant for analysis
    - Consider moving to separate metadata table

---

### JHB_EZIN_002
**Report**: `JHB_Ezin_002_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: HIV viral load extreme high values (likely missing code)
  - **Priority**: High
  - **Variable(s)**: hiv_viral_load
  - **Action**: Investigate max value (9,475,772) - likely missing data code variant
  - **Status**: To Do
  - **Notes**: Max = 9.5 million (close to 10 million threshold)
    - Mean = 97,626 vs Median = 24,814 (huge discrepancy)
    - SD = 370,636 (extremely high - indicates extreme values)
    - Check if values >10 million or other thresholds should be recoded to NA
    - Similar pattern to other studies with viral load missing codes

- [ ] Issue: Heart rate contains zero values (impossible)
  - **Priority**: High
  - **Variable(s)**: heart_rate
  - **Action**: Recode values = 0 to NA/missing
  - **Status**: To Do
  - **Notes**: Min = 0.00 bpm (impossible for living participants)
    - Mean/median are reasonable (78 bpm) so zeros are outliers
    - Check how many records have heart_rate = 0

- [ ] Issue: Cell count variables mislabeled as percentages
  - **Priority**: High
  - **Variable(s)**: lymphocyte_percentage, neutrophil_percentage, monocyte_percentage, basophil_percentage, eosinophil_percentage
  - **Action**: Rename variables to reflect absolute counts (×10⁹/L), not percentages
  - **Status**: To Do
  - **Notes**: Variables labeled "percentage" but contain absolute counts:
    - Lymphocyte "percentage": Mean = 1.83 (matches absolute count 1-4 ×10⁹/L)
    - Neutrophil "percentage": Mean = 2.76 (matches absolute count 2-7.5 ×10⁹/L)
    - Values too low for percentages (should be 20-70%), perfect for absolute counts
    - This is a VARIABLE NAMING error, not unit conversion issue
    - Do NOT multiply by 100! Just rename variables correctly

- [ ] Issue: HIV viral load status constant "Unknown" despite having viral load data
  - **Priority**: Medium
  - **Variable(s)**: hiv_viral_load_status
  - **Action**: Derive viral load status from numeric viral_load values or remove redundant variable
  - **Status**: To Do
  - **Notes**: All 1,053 records = "Unknown" yet viral load values exist
    - Variable is not informative in current state
    - Either needs to be properly derived (detectable/undetectable) or removed

- [ ] Issue: UREA NITROGEN extremely high missingness
  - **Priority**: Low
  - **Variable(s)**: urea_nitrogen
  - **Action**: Document if this variable should be collected or removed from dataset
  - **Status**: To Do
  - **Notes**: 91.5% missing - only 90 out of 1,053 records
    - Likely not part of standard protocol
    - Consider removing if not essential to analysis

---

### JHB_EZIN_025
**Report**: `JHB_EZIN_025_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Very high systematic missingness on anthropometric/vital signs (74%)
  - **Priority**: Medium
  - **Variable(s)**: height, weight, oral_temperature, heart_rate, respiration_rate, other_measures_obesity
  - **Action**: Document if this missingness is expected given COVID-19 trial design
  - **Status**: To Do
  - **Notes**: All 6 variables have exactly 74.0% missing (only 50/192 records)
    - This is clearly systematic, not random missingness
    - Pattern suggests these weren't collected for certain participants/phases
    - May limit utility of these variables for analysis
    - Verify if this is protocol-driven or data collection issue

- [ ] Issue: Unclear variable naming - "Other measures of obesity"
  - **Priority**: Medium
  - **Variable(s)**: other_measures_obesity
  - **Action**: Clarify what this variable represents and rename appropriately
  - **Status**: To Do
  - **Notes**: Mean = 26.53, Range = 17.51-44.89 (looks like BMI!)
    - Values match typical BMI range (18.5-25 normal, >30 obese)
    - Variable name is vague and uninformative
    - Recommend renaming to "bmi" if that's what it is
    - Or document what "other measures" actually means

- [ ] Issue: Patient ID stored as numeric instead of categorical
  - **Priority**: Low
  - **Variable(s)**: patient_id
  - **Action**: Convert Patient ID to text/categorical type
  - **Status**: To Do
  - **Notes**: Currently treated as numeric (mean = 2148.09, SD = 887.89)
    - IDs should be categorical to prevent accidental mathematical operations
    - No analytical benefit to treating as numeric

**General Note**: Distributions look good - no extreme outliers, unit errors, or impossible values detected. Main concerns are structural (missingness, variable naming) rather than value-level issues.

---

### JHB_JHSPH_005
**Report**: `JHB_JHSPH_005_profile.html`
**Status**: ✅ Reviewed on 2025-11-24
**RECOMMENDATION**: ⛔ **EXCLUDE FROM DATASET**

**Rationale for Exclusion:**

This dataset should be **removed from the RP2 clinical dataset collection** for the following reasons:

1. **Fundamentally Different Data Type**
   - This is an **adverse events registry**, not clinical outcomes data
   - Study type: "adverse_events_clinical_trial"
   - Contains only safety/toxicity reporting, not health measurements
   - Does not align with the purpose of other 16 studies (clinical/health outcomes)

2. **Missing All Core Clinical Variables**
   - ❌ No demographics (age, sex) - cannot analyze by participant characteristics
   - ❌ No biomarkers (CD4, viral load, lab values) - no clinical outcomes
   - ❌ No anthropometrics (height, weight, BMI) - no body composition data
   - ❌ No vital signs (BP, heart rate, temperature) - no physiological measures
   - ❌ No climate/heat exposure variables - cannot link to climate-health outcomes

3. **Incompatible with Climate-Health Analysis**
   - Other studies measure health outcomes that could be affected by climate/heat
   - This study only tracks adverse events (medication side effects, not health outcomes)
   - Cannot be integrated with climate exposure data meaningfully
   - Would dilute/confuse analyses if included with clinical datasets

4. **Data Quality Issues if Retained**
   - Categorical variables incorrectly stored as numeric (adverse_event_type, study_drug_related, treatment_arm)
   - Suspicious missing code "ZZZ" in adverse_event_grade
   - These issues suggest data was not prepared for clinical analysis

**Conclusion:**
JHB_JHSPH_005 serves a **different research purpose** (medication safety surveillance for TB prevention trial) and should be maintained in a **separate adverse events database**, not combined with the RP2 clinical outcomes datasets.

**Action Items:**
- [ ] Remove JHB_JHSPH_005 from RP2 clinical dataset collection
- [ ] Document exclusion in data dictionary/methods
- [ ] Archive separately if needed for adverse event reporting
- [ ] Update study count from 17 to 16 in documentation

**Issues Found (if dataset were to be retained - for reference only):**

---

### JHB_SCHARP_004
**Report**: `JHB_SCHARP_004_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Cell count variables mislabeled as percentages (SAME AS EZIN_002)
  - **Priority**: High
  - **Variable(s)**: basophil_percentage, eosinophil_percentage, lymphocyte_percentage, monocyte_percentage, neutrophil_percentage
  - **Action**: Rename variables to reflect absolute counts (×10⁹/L), NOT percentages
  - **Status**: To Do
  - **Notes**: Variables labeled "percentage" but contain absolute counts:
    - Basophil "percentage": Mean = 58.48 (impossible for %, normal for absolute count)
    - Eosinophil "percentage": Mean = 212.67 (absurd for %, matches absolute count)
    - Lymphocyte "percentage": Mean = 2067.56 (impossible - would be 2067%!)
    - Monocyte "percentage": Mean = 362.63 (absurd for %)
    - Neutrophil "percentage": Mean = 2891.66 (impossible for %)
    - **This is a VARIABLE NAMING error, not unit conversion issue**
    - Same issue as JHB_EZIN_002 - suggests systematic data extraction problem
    - Do NOT multiply or divide - just rename variables correctly

- [ ] Issue: Visit date extremely high missingness (99%)
  - **Priority**: High
  - **Variable(s)**: visit_date
  - **Action**: Investigate why 99% of visit dates are missing (only 4/401 records have dates)
  - **Status**: To Do
  - **Notes**: This is extreme and suspicious missingness
    - Only 4 out of 401 participants have visit dates
    - May indicate data extraction issue or incomplete data transfer
    - Limits temporal analysis capabilities
    - Verify if this is expected or needs re-extraction

- [ ] Issue: Unclear categorical coding for test results
  - **Priority**: Medium
  - **Variable(s)**: syphilis_result, hiv2_test_result
  - **Action**: Clarify what "X" and "." represent in test results
  - **Status**: To Do
  - **Notes**: Syphilis result: All = "X" (Positive? Not tested? Unknown?)
    - HIV-2 result: All = "." (Not tested? Missing?)
    - Need proper categorical labels (Positive/Negative/Not Tested/Unknown)
    - Current coding is ambiguous

- [ ] Issue: Single timepoint extraction - all visit_number = 201
  - **Priority**: Medium
  - **Variable(s)**: visit_number
  - **Action**: Verify if only visit 201 should be included or if data extraction is incomplete
  - **Status**: To Do
  - **Notes**: All 401 records have visit_number = 201 (constant variable)
    - Suggests only one visit/timepoint was extracted
    - Is this intentional (baseline only) or data extraction issue?
    - May limit longitudinal analysis if multiple timepoints exist

- [ ] Issue: Patient ID stored as numeric instead of categorical
  - **Priority**: Low
  - **Variable(s)**: patient_id
  - **Action**: Convert Patient ID to text/categorical type
  - **Status**: To Do
  - **Notes**: Currently treated as numeric (mean = 997.72)
    - Same issue across multiple studies

---

### JHB_SCHARP_006
**Report**: `JHB_SCHARP_006_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Syphilis test result nearly empty (96.5% missing)
  - **Priority**: High
  - **Variable(s)**: syphilis_result
  - **Action**: Remove variable or document why only 16/451 records have data
  - **Status**: To Do
  - **Notes**: Only 16 out of 451 participants have syphilis test results (3.5% data)
    - This is essentially an empty variable
    - Cannot be used for meaningful analysis
    - Likely optional testing or data extraction issue
    - Recommend removing from dataset unless there's specific reason

- [ ] Issue: Creatinine high missingness (67.2%)
  - **Priority**: Medium
  - **Variable(s)**: creatinine
  - **Action**: Document why 67% of creatinine values are missing
  - **Status**: To Do
  - **Notes**: Only 148 out of 451 records have creatinine data
    - May be protocol-driven (not collected for all participants)
    - Limits utility for kidney function analyses
    - Check if this was optional or selective testing

- [ ] Issue: Constant variables with no variation
  - **Priority**: Low
  - **Variable(s)**: sex, hiv_test_result, visit_date
  - **Action**: Document that study enrolled only HIV-negative females at baseline (2017-01-01)
  - **Status**: To Do
  - **Notes**: All 451 participants are Female, HIV-negative, with visit_date = 2017-01-01
    - These constant variables provide no analytical value
    - Important for documentation but could be removed from analysis dataset
    - Suggests this is a baseline/enrollment extraction only
    - Single timepoint extraction (no longitudinal data)

- [ ] Issue: Patient ID stored as numeric instead of categorical
  - **Priority**: Low
  - **Variable(s)**: patient_id
  - **Action**: Convert Patient ID to text/categorical type
  - **Status**: To Do
  - **Notes**: Same issue across multiple studies (Mean = 1026.86)

**OVERALL ASSESSMENT**: Small study (451 HIV-negative females at baseline). Main issues are near-empty variables and single timepoint extraction. No severe data quality problems like unit errors or impossible values.

---

### JHB_VIDA_007
**Report**: `JHB_VIDA_007_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Core vaccination variables 100% missing in vaccine trial
  - **Priority**: High
  - **Variable(s)**: vaccination_date, vaccination_site, vaccination_route
  - **Action**: Investigate why core vaccine study variables are completely absent (N=0)
  - **Status**: To Do
  - **Notes**: This is a COVID vaccine clinical trial (ChAdOx1/AstraZeneca)
    - All vaccination-related variables are 100% missing (0 records)
    - These should be core outcome/protocol variables
    - Suggests data extraction issue or variables were never populated in source
    - May indicate incomplete data transfer from original study database
    - Verify if vaccination data exists in source system

- [ ] Issue: Age missing for 18.2% of participants
  - **Priority**: Medium
  - **Variable(s)**: age
  - **Action**: Investigate why 388/2,129 participants are missing age data
  - **Status**: To Do
  - **Notes**: Age is a core demographic variable
    - 18.2% missingness is high for such a fundamental variable
    - Limits demographic subgroup analyses
    - Check if age can be derived from date of birth or other sources
    - May need to exclude records without age from certain analyses

- [ ] Issue: Height units inconsistent with other studies
  - **Priority**: Medium
  - **Variable(s)**: height
  - **Action**: Document that height is in centimeters (not meters) for this study
  - **Status**: To Do
  - **Notes**: Mean = 167 cm (most other studies use meters)
    - Values are reasonable (130-197 cm range)
    - Not an error, but INCONSISTENT with other studies
    - Could cause analysis errors if not properly documented
    - Recommend standardizing to meters across all studies for consistency
    - Conversion: divide by 100 to get meters

- [ ] Issue: Potential outliers in physiological measures
  - **Priority**: Low
  - **Variable(s)**: respiratory_rate, bmi
  - **Action**: Verify extreme values are real and not data entry errors
  - **Status**: To Do
  - **Notes**: Respiratory rate max = 52 (normal 12-20, but high resp rate possible in COVID patients)
    - BMI min = 14.0 (severe underweight, should verify)
    - Given COVID vaccine trial context, some extreme values may be legitimate
    - Review individual records with extreme values

---

### JHB_VIDA_008
**Report**: `JHB_VIDA_008_profile.html`
**Status**: ✅ Reviewed on 2025-11-24
**⚠️ CRITICAL DATA QUALITY ISSUES**

**Issues Found:**

- [ ] Issue: BMI values completely invalid - CATASTROPHIC DATA QUALITY ISSUE
  - **Priority**: CRITICAL
  - **Variable(s)**: bmi
  - **Action**: Urgent investigation required - BMI data is completely unusable
  - **Status**: To Do
  - **Notes**: Mean = 1,601.42 (normal 18.5-25), Max = 850,000 (IMPOSSIBLE!)
    - SD = 36,543 indicating extreme outliers or systematic error
    - **Possible causes:**
      1. Missing data code (850000 or similar used for missing)
      2. Calculation error (wrong units for height/weight in BMI formula)
      3. Data entry errors (missing decimal points, extra digits)
      4. Source data corruption
    - **BMI cannot be used for any analysis in current state**
    - Need to recalculate from height/weight or re-extract from source
    - Check if height (min=0.01m) and weight errors are causing BMI calculation errors

- [ ] Issue: Height contains impossible minimum value
  - **Priority**: High
  - **Variable(s)**: height
  - **Action**: Investigate and recode height = 0.01m (1cm - impossible for adults)
  - **Status**: To Do
  - **Notes**: Min = 0.01m (1 centimeter!)
    - Median = 1.63m is reasonable, so this is an outlier
    - Likely missing data coded as 0 or data entry error
    - May be causing BMI calculation issues
    - Recode extreme values (<1.0m) to NA

- [ ] Issue: Sex variable has 3 categories instead of 2
  - **Priority**: High
  - **Variable(s)**: sex
  - **Action**: Investigate what the 3rd sex category represents
  - **Status**: To Do
  - **Notes**: Should only have Male/Female (2 values)
    - 3rd category could be: Other, Unknown, Missing, data entry error, or non-binary
    - Need to clarify and properly code
    - 1.4% of records missing sex (8 participants)

- [ ] Issue: HIV status high missingness (48%)
  - **Priority**: Medium
  - **Variable(s)**: hiv_status
  - **Action**: Investigate why nearly half of participants missing HIV status
  - **Status**: To Do
  - **Notes**: 289/557 records have HIV status, 268 missing (48.1%)
    - This is a COVID healthcare worker study - HIV status may not have been collected for all
    - May be protocol-driven (optional variable) rather than data quality issue
    - Limits HIV-stratified analyses

- [ ] Issue: Hyperlipidaemia 99% missing (essentially empty variable)
  - **Priority**: Low
  - **Variable(s)**: hyperlipidaemia
  - **Action**: Remove variable from dataset or document why only 5/557 records
  - **Status**: To Do
  - **Notes**: Only 5 out of 557 records (0.9%) have data
    - Variable is essentially useless for analysis
    - May have been optional or added late in study
    - Recommend removing from dataset

**OVERALL ASSESSMENT**: This dataset has SEVERE data quality issues, particularly the BMI catastrophe. Requires urgent attention before any analysis.

---

### JHB_WRHI_001
**Report**: `JHB_WRHI_001_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: HIV viral load with missing data code (10,000,001)
  - **Priority**: High
  - **Variable(s)**: hiv_viral_load
  - **Action**: Recode values = 10,000,001 to NA/missing
  - **Status**: To Do
  - **Notes**: Max = 10,000,001 (10 million + 1) - clear missing code variant
    - Mean = 248,208 vs Median = 84,559 (huge discrepancy due to extreme value)
    - SD = 576,289 (massive - indicates outliers)
    - Same pattern as other studies (9,475,772 in EZIN_002, 99999999 in Aurum_009)
    - Systematic missing code issue across multiple studies

- [ ] Issue: Lipid panel (HDL, LDL, Cholesterol) with extreme outliers
  - **Priority**: High
  - **Variable(s)**: fasting_hdl, fasting_ldl, fasting_total_cholesterol
  - **Action**: Investigate extreme values and recode outliers or missing codes
  - **Status**: To Do
  - **Notes**: Means vastly exceed medians:
    - HDL: Mean = 16.88, Median = 1.40 (12x difference!)
    - LDL: Mean = 40.02, Median = 3.10 (13x difference!)
    - Cholesterol: Mean = 65.87, Median = 4.80 (14x difference!)
    - Medians look reasonable if mmol/L (HDL ~1.4, LDL ~3.1, Chol ~4.8)
    - Extreme means suggest missing data codes or unit errors pulling averages up
    - Need to identify and recode outliers

- [ ] Issue: Hematocrit mixing decimal and percentage formats
  - **Priority**: High
  - **Variable(s)**: hematocrit
  - **Action**: Standardize all hematocrit values to decimal format (0.36-0.50)
  - **Status**: To Do
  - **Notes**: Mean = 16.86, Median = 0.46, Max = 60.30
    - Median 0.46 = 46% (correct decimal format: 0.36-0.50)
    - Mean 16.86 suggests some values in percentage format (40-50 instead of 0.40-0.50)
    - Max 60.30 could be 60% as percentage or 0.603 as decimal
    - Need to convert all percentage values (>1) to decimal by dividing by 100
    - Verify values in 1-100 range should be percentages

- [ ] Issue: Fasting glucose with extreme outliers
  - **Priority**: Medium
  - **Variable(s)**: fasting_glucose
  - **Action**: Investigate and recode extreme glucose values (max = 295)
  - **Status**: To Do
  - **Notes**: Mean = 36.35, Median = 5.00, Max = 295
    - Median 5.00 mmol/L is normal
    - Max 295 is extremely high - diabetic emergency if mmol/L
    - Mean >> median suggests multiple extreme outliers
    - Check if mixing mmol/L and mg/dL units (295 mg/dL = 16.4 mmol/L, reasonable)
    - Or if high values are missing codes

- [ ] Issue: Patient ID stored as numeric instead of categorical
  - **Priority**: Low
  - **Variable(s)**: patient_id
  - **Action**: Convert Patient ID to text/categorical type
  - **Status**: To Do
  - **Notes**: Currently treated as numeric (mean = 15,505.70)
    - Same issue across multiple studies

---

### JHB_WRHI_003
**Report**: `JHB_WRHI_003_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**

- [ ] Issue: Multiple variables completely empty (100% missing) - should be removed
  - **Priority**: Medium
  - **Variable(s)**: fasting_glucose, alkaline_phosphatase, ldh, transferrin, total_protein
  - **Action**: Remove these 5 variables from dataset (N=0 for all)
  - **Status**: To Do
  - **Notes**: All 5 variables have 100% missing data (0 records)
    - These variables add no value and clutter the dataset
    - Likely were not collected as part of this study protocol
    - Clean removal will improve data clarity

- [ ] Issue: Near-empty variables (99.7% missing) - essentially useless
  - **Priority**: Medium
  - **Variable(s)**: albumin, calcium
  - **Action**: Remove these variables or document why only 1/300 records
  - **Status**: To Do
  - **Notes**: Only 1 out of 300 records has data for each variable
    - With 99.7% missingness, these are essentially empty
    - Cannot be used for any meaningful analysis
    - Recommend removing unless there's specific reason to keep

- [ ] Issue: Unclear variable naming - "Other measures of obesity"
  - **Priority**: Medium
  - **Variable(s)**: other_measures_obesity
  - **Action**: Clarify what this variable represents and rename appropriately
  - **Status**: To Do
  - **Notes**: Mean = 27.95, Range = 17.63-47.39 (looks like BMI)
    - Same vague naming issue as EZIN_025
    - Values match typical BMI range
    - Should rename to "bmi" if that's what it represents
    - Or document what "other measures" actually means

- [ ] Issue: HIV viral load in different format/units than other studies
  - **Priority**: Medium
  - **Variable(s)**: pcr_hiv_viral_load_roche
  - **Action**: Document units and verify comparability with other studies
  - **Status**: To Do
  - **Notes**: Median = 0.00, Mean = 7.15, Max = 63.00
    - Values are VERY different from other studies (which have medians ~25,000-85,000)
    - Might be log-transformed values (log10)
    - Or different assay/units (Roche vs other methods)
    - Median of 0 could represent undetectable viral loads
    - Need to clarify units for cross-study comparisons

- [ ] Issue: Duplicate "Country" variables with different values
  - **Priority**: Low
  - **Variable(s)**: Country (capital C), country (lowercase)
  - **Action**: Investigate why "Country" has 11 values vs "country" with 1 value
  - **Status**: To Do
  - **Notes**: "Country" (capital): 11 unique values
    - "country" (lowercase): 1 value (South Africa)
    - Suggests duplicate variable or data entry inconsistency
    - Need to check what the 11 Country values represent
    - May need to merge/standardize

**OVERALL ASSESSMENT**: This dataset is relatively clean compared to others. Main issues are empty variables that should be removed and clarification needed on variable definitions. No critical data quality disasters like other studies.

---

## Summary Statistics

**Total Studies**: 17 (original)
**Studies Reviewed**: 17 / 17 (100%)
**Recommended for Exclusion**: 1 (JHB_JHSPH_005 - adverse events only)

**Study Status Breakdown:**
- ✅ **Reviewed and Usable**: 10 studies
- ⚠️ **CRITICAL Data Quality Issues**: 7 studies (6 ACTG + 1 VIDA_008)
  - **ALL 6 ACTG studies have CATASTROPHIC extraction failures**
  - JHB_VIDA_008 has critical BMI calculation errors
- ⛔ **Excluded**: 1 study (JHB_JHSPH_005 - wrong data type)

**Usable Clinical Studies**: 10 out of 16 (62.5%)
**Unusable Due to Extraction Failures**: 6 ACTG studies (605 participants - 23% of total cohort lost)
**Critical Issues Requiring Immediate Attention**: 1 study (VIDA_008 - BMI catastrophe)

**Total Issues Found**: 65+ across all studies
- **CRITICAL Priority Issues**: 20+ (dataset unusable without fixes)
- **High Priority Issues**: 15+ (must fix before analysis)
- **Medium Priority Issues**: 20+ (should fix before publication)
- **Low Priority Issues**: 10+ (fix when convenient)

**Issues Fixed in JupyterHub**: 0 / 65+

**Key Issue Types:**
- **SYSTEMATIC EXTRACTION FAILURES (ACTG cohort)**: 6 studies
  - Core HIV variables 100% missing (age, CD4, viral load)
  - Numeric missing codes (ALT=1, Platelet=3, Viral load=400)
  - ALL laboratory values absent in some studies
- **Missing data codes** (9999, 99999999, 0, 400): 8 studies
- **Unit errors** (mm vs cm, kg vs g): 2 studies
- **Calculation errors** (BMI catastrophe): 1 study (VIDA_008)
- **Variable naming errors**: 2 studies
- **Near-empty variables** (>95% missing): 5 studies
- **Impossible/zero values**: 6 studies

**URGENT ACTION REQUIRED:**
1. **Re-extract ALL 6 ACTG studies** - current data unusable
2. **Investigate VIDA_008 BMI** - values impossibly high (max 850,000)
3. **Systematically recode missing data codes** across all studies

---

## Quick Reference Commands

### Open Reports in Browser
```bash
# Open specific study report
open JHB_ACTG_015_profile.html

# Open quality reports
open DATASET_STATUS_RESEARCH_REPORT.html
open ENHANCED_DATASET_STATUS_REPORT.html

# Open comprehensive report
open ULTRA_COMPREHENSIVE_REPORT.html
```

### Navigate Study Visualizations
```bash
# View missing data visualization
open JHB_ACTG_015/JHB_ACTG_015_missing_data.svg

# View distributions
open JHB_ACTG_015/JHB_ACTG_015_ALL_distributions.svg
```

---

## Review Workflow

1. **Open study profile HTML** in browser
2. **Check summary statistics** for implausible values
3. **Review missing data heatmaps** for patterns
4. **Examine distribution plots** for outliers/anomalies
5. **Check categorical variable frequencies** for issues
6. **Document findings** in this file with clear action items
7. **Mark study as reviewed** in status table
8. **Fix issues in JupyterHub** when batch is ready
9. **Update status** when fixed

---

## Notes & Observations

[Add any general observations or cross-study patterns here]
