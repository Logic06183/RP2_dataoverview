# Study Profiles - Usage Guide

## Quick Reference

### View a Complete Study Profile

```bash
cd /home/cparker/incoming/RP2/SVG_Visualizations/Study_Profiles

# View any study profile
cd JHB_ACTG_015/
cat JHB_ACTG_015_report.md

# The report includes:
# - Total variable count
# - ALL biomarkers with statistics
# - Variables organized by category (Demographics, Hematology, Chemistry, etc.)
# - Complete alphabetical list of EVERY variable
# - Data quality metrics
```

### View Visualizations

```bash
# Open SVG files in browser or image viewer
firefox JHB_ACTG_015_biomarker_distributions.svg
firefox JHB_ACTG_015_missing_data.svg
firefox JHB_ACTG_015_summary.svg
```

### Find Studies by Biomarker

```bash
# Find all studies with CD4 data
grep -r "CD4" */JHB_*_report.md

# Find studies with cholesterol
grep -r "CHOLESTEROL" */JHB_*_report.md

# Count biomarkers per study
grep "Total biomarker columns" */JHB_*_report.md
```

### Compare Variable Availability

```bash
# See all variables across all studies
grep -h "^- \`" */JHB_*_report.md | sort -u > all_variables.txt

# Count unique variables  
grep -h "^- \`" */JHB_*_report.md | sort -u | wc -l
```

## What Each File Contains

### 1. `[study]_report.md` - Comprehensive Text Report

Contains:
- **Overview**: Participants, total variables (numeric + categorical)
- **Demographics**: Age, sex distributions  
- **ALL Biomarkers**: Complete table with N, mean, median, min, max, missing %
- **Variable Inventory by Category**:
  - Demographics
  - Anthropometrics (height, weight, BMI)
  - Vital Signs (BP, heart rate, temperature)
  - Hematology (CBC components)
  - Immunology (CD4, viral load)
  - Chemistry (glucose, creatinine, electrolytes)
  - Lipids (cholesterol, LDL, HDL, triglycerides)
  - Liver (ALT, AST, bilirubin)
  - Study Metadata
- **Complete Alphabetical List**: Every single variable extracted
- **Data Quality**: Top 30 most complete variables

### 2. `[study]_missing_data.svg` - Visual Missing Data Analysis

Shows:
- Bar chart of columns with missing data
- Color-coded by severity:
  - Red: >50% missing
  - Yellow: 10-50% missing  
  - Green: <10% missing
- Percentage labels for each column

### 3. `[study]_biomarker_distributions.svg` - Histograms

Shows:
- Top 6 biomarkers with most data
- Distribution patterns
- N, mean overlaid on each plot

### 4. `[study]_summary.svg` - Quick Reference Card

Shows:
- Total participants
- Total records
- Data completeness
- Key demographics

## Advanced Usage

### Extract Specific Variable Stats

```bash
# Get CD4 statistics across all studies
for report in */JHB_*_report.md; do
    echo "$(dirname $report):"
    grep "CD4" $report | grep "|" | head -1
done
```

### Find Studies with Specific Completeness

```bash
# Find studies with >95% complete data
for report in */JHB_*_report.md; do
    comp=$(grep "Data Completeness" $report | grep -oP '\d+\.\d+' | head -1)
    if (( $(echo "$comp > 95" | bc -l) )); then
        echo "$(dirname $report): ${comp}%"
    fi
done
```

### Generate Study Comparison Table

```bash
# Compare key variables across studies
echo "Study,Participants,Variables,CD4,Hemoglobin,Cholesterol"
for report in */JHB_*_report.md; do
    study=$(dirname $report | sed 's|/||g')
    part=$(grep "Unique Participants" $report | grep -oP '\d+' | head -1)
    vars=$(grep "Total Variables" $report | grep -oP '\d+' | head -1)
    cd4=$(grep -o "CD4.*complete" $report | grep -oP '\d+\.\d+' | head -1)
    hgb=$(grep -o "HEMOGLOBIN.*complete" $report | grep -oP '\d+\.\d+' | head -1)
    chol=$(grep -o "CHOLESTEROL.*complete" $report | grep -oP '\d+\.\d+' | head -1)
    echo "$study,$part,$vars,$cd4,$hgb,$chol"
done > study_comparison.csv
```

## Regenerating Profiles

If you update any harmonized data files:

```bash
cd /home/cparker/incoming/RP2/SVG_Visualizations
python3 create_lightweight_study_profiles.py
```

This will:
- Regenerate all profiles with updated data
- Create backups of old profiles (timestamped)
- Complete in seconds (not hours like HTML profiling)
- Won't stall the cluster

## Notes

- **Some studies may be missing markdown reports** due to data quality issues (concatenated strings, mixed types)
  - These studies still have SVG visualizations
  - The raw harmonized CSV files are still intact and usable
  
- **Biomarker counts vary** because:
  - Studies focus on different outcomes (adverse events vs biomarkers vs anthropometrics)
  - Some studies are cross-sectional, others longitudinal
  - Different harmonization completeness levels

- **All variable names are preserved** exactly as they appear in the harmonized files
  - Use these names when querying the actual CSV data
  - Variable naming follows HEAT codebook standards where possible

