# Anomaly Detection Checklist for RP2 Clinical Data Quality Review

This checklist provides a systematic approach to identifying data quality issues when reviewing study profile reports.

---

## Pre-Review Setup

- [ ] Open `DATA_QUALITY_FINDINGS.md` in a text editor to document issues
- [ ] Have the study profile HTML open in browser
- [ ] Have JupyterHub accessible for quick verification if needed
- [ ] Note the study name and start time

---

## Section 1: Study Overview & Demographics

### Sample Size & Recruitment
- [ ] **Check total sample size** - Is it reasonable for the study type?
  - Flag if: n < 20 (may be underpowered), or suspiciously round numbers

- [ ] **Check recruitment dates** - Are they logical and complete?
  - Flag if: Future dates, dates before 1990, missing dates, impossible date ranges

### Demographics
- [ ] **Age distribution**
  - Flag if: Negative ages, ages > 120, ages < 18 (for adult studies), unusual modes
  - Check: Does the age range match study inclusion criteria?

- [ ] **Sex/Gender distribution**
  - Flag if: Unexpected ratios (all male/female when should be mixed)
  - Check: Are categories properly coded (not numeric codes like 1/2)?

- [ ] **BMI distribution** (if available)
  - Flag if: BMI < 10 or > 70 (biologically implausible)
  - Check: Unusual bimodal distributions suggesting unit errors (lbs vs kg?)

---

## Section 2: Missing Data Patterns

### Missing Data Heatmap Review
- [ ] **Check for systematic missingness**
  - Flag if: Entire variables are 100% missing (shouldn't exist or collection failed?)
  - Flag if: Variables that should never be missing have >5% missing (e.g., participant ID, visit dates)
  - Flag if: Diagonal or block patterns suggesting batch data entry issues

- [ ] **Check critical variables**
  - Flag if: Primary outcomes have >20% missing
  - Flag if: Key covariates (age, sex) have any missing values

- [ ] **Look for MAR vs MNAR patterns**
  - Flag if: Missingness correlates with outcome (e.g., sicker patients have more missing data)

---

## Section 3: Continuous Variable Distributions

### For Each Biomarker/Continuous Variable:

- [ ] **Check distribution shape**
  - Flag if: Extremely skewed when should be normal
  - Flag if: Suspicious spikes at rounded values (10, 20, 50) suggesting estimation/rounding
  - Flag if: Bimodal without biological reason

- [ ] **Check for impossible values**
  - Blood pressure: < 50 or > 250 (systolic), < 30 or > 150 (diastolic)
  - Heart rate: < 30 or > 220 bpm
  - Temperature: < 35°C or > 42°C (94°F - 107.6°F)
  - Lab values: Negative values where impossible, or extremely high

- [ ] **Check for unit errors**
  - Flag if: Values suggest wrong units (e.g., glucose in mmol/L vs mg/dL)
  - Flag if: Some values are 10x or 100x others (decimal place errors)

- [ ] **Check for outliers**
  - Flag if: Values beyond 4-5 standard deviations from mean
  - Flag if: Single extreme values that dramatically affect distribution

- [ ] **Check for digit preference**
  - Flag if: All values end in 0 or 5 (over-rounding)
  - Flag if: Suspiciously few decimal places when precision is expected

---

## Section 4: Categorical Variables

### For Each Categorical Variable:

- [ ] **Check category labels**
  - Flag if: Numeric codes instead of labels (1, 2, 3 instead of "Yes", "No", "Unknown")
  - Flag if: Misspellings or inconsistent naming ("Yes" vs "yes" vs "YES")
  - Flag if: Unexpected categories appear

- [ ] **Check category frequencies**
  - Flag if: One category dominates (>95%) when should be more balanced
  - Flag if: Very small cells (<5) that might indicate rare miscoding

- [ ] **Check for "Unknown" / "Other" categories**
  - Flag if: >20% in Unknown/Other/Prefer not to say
  - Check: Should these be re-coded to missing?

- [ ] **Check logical categories**
  - Flag if: "N/A" appears as data value instead of missing
  - Flag if: Categories like "9999" or "-1" used for missing

---

## Section 5: Temporal & Longitudinal Checks

- [ ] **Check visit dates/times**
  - Flag if: Visits out of chronological order
  - Flag if: Duplicate visit dates for same participant
  - Flag if: Impossible time intervals (e.g., visits 1 day apart when protocol requires 30 days)

- [ ] **Check follow-up data**
  - Flag if: Outcome collected before baseline
  - Flag if: Lost to follow-up not properly coded

---

## Section 6: Cross-Variable Consistency

- [ ] **Check logical relationships**
  - Flag if: Pregnant males
  - Flag if: Children with adult diseases
  - Flag if: Post-menopausal women with pregnancy
  - Flag if: Height/weight values yield implausible BMI

- [ ] **Check derived variables**
  - Flag if: BMI calculated doesn't match reported BMI
  - Flag if: Age calculated from DOB doesn't match reported age

---

## Section 7: Study-Specific Protocol Issues

- [ ] **Check inclusion/exclusion criteria compliance**
  - Flag if: Ages outside protocol range
  - Flag if: Conditions present that should exclude participants

- [ ] **Check intervention/exposure variables**
  - Flag if: Control group has exposure values
  - Flag if: Treatment timing doesn't align with study design

---

## Section 8: Statistical Red Flags

- [ ] **Check for suspiciously perfect data**
  - Flag if: No outliers at all (data cleaning too aggressive?)
  - Flag if: Distributions too perfect/symmetric
  - Flag if: Correlations too high (>0.95 between supposedly independent variables)

- [ ] **Check for duplicates**
  - Flag if: Repeated identical rows across multiple variables
  - Flag if: Copy-paste patterns in data entry

---

## Priority Classification

When documenting issues in `DATA_QUALITY_FINDINGS.md`, use these priorities:

### 🔴 HIGH PRIORITY (Fix immediately)
- Impossible values that invalidate analysis
- Critical variables with >50% missing
- Severe consistency violations
- Data that could identify participants

### 🟡 MEDIUM PRIORITY (Fix before analysis)
- Outliers that need verification
- Missing data 20-50% on important variables
- Unit errors
- Minor consistency issues

### 🟢 LOW PRIORITY (Fix if time permits)
- Cosmetic issues (category labels)
- Very minor outliers
- Low-impact missing data (<10%)
- Formatting inconsistencies

---

## Quick Reference: Common Issues by Variable Type

### Age
- ❌ Negative values
- ❌ > 120 years
- ❌ < 18 for adult studies
- ⚠️  All same age (data entry error?)

### Weight
- ❌ < 2 kg or > 300 kg
- ⚠️  Check if lbs vs kg confusion
- ⚠️  Sudden jumps >50kg between visits

### Blood Pressure
- ❌ Systolic < diastolic
- ❌ Systolic < 50 or > 250
- ❌ Diastolic < 30 or > 150

### Dates
- ❌ Future dates
- ❌ Before study start
- ❌ Chronological violations

### Lab Values
- ❌ Negative when must be positive
- ⚠️  Unit confusion (mmol/L vs mg/dL)
- ⚠️  Values > 10x expected range

### Categorical
- ❌ Numeric codes (1,2,3) instead of labels
- ❌ Typos in categories
- ⚠️  Unexpected "Other" >20%

---

## After Completing Review

- [ ] Update study status in `DATA_QUALITY_FINDINGS.md` to ✅
- [ ] Add review date
- [ ] Prioritize issues for JupyterHub fixes
- [ ] Note any cross-study patterns observed
- [ ] Move to next study using `python review_helper.py --next`

---

## Tips for Efficient Review

1. **Start with quality reports** - Review `DATASET_STATUS_RESEARCH_REPORT.html` first to identify studies with known issues

2. **Use the missing data heatmap** - This often reveals the most systematic issues quickly

3. **Don't fix here** - Just document! All fixes happen in JupyterHub

4. **Look for patterns** - If you see an issue in one study, check others from same network

5. **Trust your instincts** - If something looks weird, it probably is

6. **Be systematic** - Use this checklist for every study to ensure consistency

---

**Remember**: The goal is to identify issues, not fix them. Document clearly so you can batch-fix efficiently in JupyterHub later.
