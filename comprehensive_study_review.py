#!/opt/anaconda3/bin/python3
"""
Comprehensive Study-by-Study Quality Review
Analyzes each study's profile for notable patterns, issues, and characteristics
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("COMPREHENSIVE STUDY-BY-STUDY QUALITY REVIEW")
print("="*80)
print()

# Load dataset
print("📊 Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records from {df['study_source'].nunique()} studies")
print()

# Get all studies
studies = sorted(df['study_source'].unique())

# Define key variables to check
key_demographics = ['Age (at enrolment)', 'Sex', 'Race']
key_hiv_markers = ['CD4 cell count (cells/µL)', 'HIV viral load (copies/mL)', 'Antiretroviral Therapy Status']
key_hematology = ['Hematocrit (%)', 'hemoglobin_g_dL', 'White blood cell count (×10³/µL)',
                  'Platelet count (×10³/µL)']
key_biochemistry = ['ALT (U/L)', 'AST (U/L)', 'creatinine_umol_L', 'Albumin (g/dL)']
key_anthropometry = ['BMI (kg/m²)', 'weight_kg', 'height_m', 'Waist circumference (cm)']
key_vitals = ['systolic_bp_mmHg', 'diastolic_bp_mmHg', 'heart_rate_bpm', 'body_temperature_celsius']
key_climate = ['climate_daily_mean_temp', 'climate_daily_max_temp', 'climate_heat_stress_index']

all_key_vars = (key_demographics + key_hiv_markers + key_hematology +
                key_biochemistry + key_anthropometry + key_vitals + key_climate)

def get_var_stats(study_df, var):
    """Get statistics for a variable"""
    if var not in study_df.columns:
        return None

    data = study_df[var].dropna()
    if len(data) == 0:
        return None

    if pd.api.types.is_numeric_dtype(data):
        return {
            'n': len(data),
            'missing': len(study_df) - len(data),
            'missing_pct': 100 * (len(study_df) - len(data)) / len(study_df),
            'mean': data.mean(),
            'std': data.std(),
            'min': data.min(),
            'q25': data.quantile(0.25),
            'median': data.median(),
            'q75': data.quantile(0.75),
            'max': data.max(),
            'zeros': (data == 0).sum(),
            'type': 'numeric'
        }
    else:
        return {
            'n': len(data),
            'missing': len(study_df) - len(data),
            'missing_pct': 100 * (len(study_df) - len(data)) / len(study_df),
            'unique': data.nunique(),
            'top': data.value_counts().index[0] if len(data) > 0 else None,
            'freq': data.value_counts().values[0] if len(data) > 0 else None,
            'type': 'categorical'
        }

def identify_issues(study_name, study_df, stats_dict):
    """Identify notable issues or patterns in a study"""
    issues = []

    # Check demographics
    if 'Age (at enrolment)' in stats_dict and stats_dict['Age (at enrolment)']:
        age_stats = stats_dict['Age (at enrolment)']
        if age_stats['type'] == 'numeric':
            if age_stats['mean'] < 25:
                issues.append(f"✓ Young cohort (mean age {age_stats['mean']:.1f} years)")
            elif age_stats['mean'] > 50:
                issues.append(f"✓ Older cohort (mean age {age_stats['mean']:.1f} years)")

            if age_stats['min'] < 18:
                issues.append(f"ℹ️  Includes minors (min age {age_stats['min']:.0f} years)")

    # Check CD4
    if 'CD4 cell count (cells/µL)' in stats_dict and stats_dict['CD4 cell count (cells/µL)']:
        cd4_stats = stats_dict['CD4 cell count (cells/µL)']
        if cd4_stats['type'] == 'numeric':
            if cd4_stats['missing_pct'] > 50:
                issues.append(f"⚠️  HIGH CD4 missingness: {cd4_stats['missing_pct']:.1f}%")

            if cd4_stats['zeros'] > 0:
                issues.append(f"⚠️  CD4 = 0: {cd4_stats['zeros']} records")

            if cd4_stats['mean'] < 200:
                issues.append(f"✓ Severely immunosuppressed cohort (mean CD4 {cd4_stats['mean']:.0f})")
            elif cd4_stats['mean'] > 500:
                issues.append(f"✓ Well-controlled cohort (mean CD4 {cd4_stats['mean']:.0f})")

            if cd4_stats['max'] > 2000:
                issues.append(f"⚠️  Extreme CD4 value: {cd4_stats['max']:.0f}")

    # Check viral load
    if 'HIV viral load (copies/mL)' in stats_dict and stats_dict['HIV viral load (copies/mL)']:
        vl_stats = stats_dict['HIV viral load (copies/mL)']
        if vl_stats['type'] == 'numeric':
            if vl_stats['missing_pct'] > 50:
                issues.append(f"⚠️  HIGH viral load missingness: {vl_stats['missing_pct']:.1f}%")

            if vl_stats['zeros'] > 0:
                zero_pct = 100 * vl_stats['zeros'] / vl_stats['n']
                issues.append(f"ℹ️  VL = 0: {vl_stats['zeros']} records ({zero_pct:.1f}% - likely undetectable)")

            if vl_stats['max'] > 1000000:
                issues.append(f"⚠️  Extreme viral load: {vl_stats['max']:.0f}")

    # Check hematology
    for var in ['Hematocrit (%)', 'hemoglobin_g_dL', 'White blood cell count (×10³/µL)', 'Platelet count (×10³/µL)']:
        if var in stats_dict and stats_dict[var] and stats_dict[var]['type'] == 'numeric':
            var_stats = stats_dict[var]
            if var_stats['zeros'] > 0:
                issues.append(f"⚠️  {var} has {var_stats['zeros']} zero values (impossible)")

            if var_stats['missing_pct'] > 80:
                issues.append(f"⚠️  {var}: {var_stats['missing_pct']:.1f}% missing")

    # Check albumin (known issue)
    if 'Albumin (g/dL)' in stats_dict and stats_dict['Albumin (g/dL)']:
        alb_stats = stats_dict['Albumin (g/dL)']
        if alb_stats['type'] == 'numeric':
            if alb_stats['max'] > 6:
                high_alb = (study_df['Albumin (g/dL)'] > 6).sum()
                issues.append(f"🔴 ALBUMIN ISSUE: {high_alb} records > 6 g/dL (max: {alb_stats['max']:.1f}) - UNIT ERROR")

    # Check waist circumference
    if 'Waist circumference (cm)' in stats_dict and stats_dict['Waist circumference (cm)']:
        waist_stats = stats_dict['Waist circumference (cm)']
        if waist_stats['type'] == 'numeric':
            if waist_stats['min'] < 40:
                issues.append(f"⚠️  Waist circumference min {waist_stats['min']:.1f} cm (too small)")
            if waist_stats['max'] > 200:
                issues.append(f"⚠️  Waist circumference max {waist_stats['max']:.1f} cm (too large)")

    # Check for overall completeness
    total_vars = len([v for v in all_key_vars if v in study_df.columns])
    vars_with_data = len([v for v in all_key_vars if v in stats_dict and stats_dict[v] and stats_dict[v]['missing_pct'] < 90])

    if total_vars > 0:
        completeness = 100 * vars_with_data / total_vars
        if completeness < 30:
            issues.append(f"⚠️  LOW DATA COMPLETENESS: {completeness:.0f}% of key variables have data")

    # Check climate data
    climate_vars_present = len([v for v in key_climate if v in study_df.columns and study_df[v].notna().any()])
    if climate_vars_present == 0:
        issues.append(f"ℹ️  No climate data available")
    elif climate_vars_present < len(key_climate):
        issues.append(f"ℹ️  Partial climate data ({climate_vars_present}/{len(key_climate)} variables)")

    return issues

# Generate report
print("="*80)
print("STUDY-BY-STUDY QUALITY REVIEW")
print("="*80)
print()

report_lines = []
report_lines.append("# Comprehensive Study-by-Study Quality Review\n")
report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
report_lines.append(f"**Dataset:** CLINICAL_DATASET_QUALITY_HARMONIZED.csv\n")
report_lines.append(f"**Total Records:** {len(df):,} across {len(studies)} studies\n")
report_lines.append("\n---\n\n")

# Analyze each study
for i, study in enumerate(studies, 1):
    study_df = df[df['study_source'] == study].copy()
    n_records = len(study_df)

    print(f"[{i}/{len(studies)}] {study}")
    print(f"  Records: {n_records:,}")

    report_lines.append(f"## {i}. {study}\n")
    report_lines.append(f"**Records:** {n_records:,}\n\n")

    # Get statistics for all key variables
    stats_dict = {}
    for var in all_key_vars:
        stats = get_var_stats(study_df, var)
        if stats:
            stats_dict[var] = stats

    # Count available variables by category
    demo_count = sum(1 for v in key_demographics if v in stats_dict)
    hiv_count = sum(1 for v in key_hiv_markers if v in stats_dict)
    heme_count = sum(1 for v in key_hematology if v in stats_dict)
    biochem_count = sum(1 for v in key_biochemistry if v in stats_dict)
    anthro_count = sum(1 for v in key_anthropometry if v in stats_dict)
    vitals_count = sum(1 for v in key_vitals if v in stats_dict)
    climate_count = sum(1 for v in key_climate if v in stats_dict)

    print(f"  Variables available:")
    print(f"    Demographics: {demo_count}/{len(key_demographics)}")
    print(f"    HIV markers: {hiv_count}/{len(key_hiv_markers)}")
    print(f"    Hematology: {heme_count}/{len(key_hematology)}")
    print(f"    Biochemistry: {biochem_count}/{len(key_biochemistry)}")
    print(f"    Anthropometry: {anthro_count}/{len(key_anthropometry)}")
    print(f"    Vitals: {vitals_count}/{len(key_vitals)}")
    print(f"    Climate: {climate_count}/{len(key_climate)}")

    report_lines.append("### Data Availability\n")
    report_lines.append(f"- Demographics: {demo_count}/{len(key_demographics)}\n")
    report_lines.append(f"- HIV Markers: {hiv_count}/{len(key_hiv_markers)}\n")
    report_lines.append(f"- Hematology: {heme_count}/{len(key_hematology)}\n")
    report_lines.append(f"- Biochemistry: {biochem_count}/{len(key_biochemistry)}\n")
    report_lines.append(f"- Anthropometry: {anthro_count}/{len(key_anthropometry)}\n")
    report_lines.append(f"- Vitals: {vitals_count}/{len(key_vitals)}\n")
    report_lines.append(f"- Climate: {climate_count}/{len(key_climate)}\n\n")

    # Key findings
    report_lines.append("### Key Statistics\n")

    # Age
    if 'Age (at enrolment)' in stats_dict:
        age = stats_dict['Age (at enrolment)']
        report_lines.append(f"- **Age:** {age['mean']:.1f} ± {age['std']:.1f} years (range: {age['min']:.0f}-{age['max']:.0f})\n")

    # CD4
    if 'CD4 cell count (cells/µL)' in stats_dict:
        cd4 = stats_dict['CD4 cell count (cells/µL)']
        report_lines.append(f"- **CD4 count:** {cd4['mean']:.0f} ± {cd4['std']:.0f} cells/µL (median: {cd4['median']:.0f})\n")
        report_lines.append(f"  - Missing: {cd4['missing_pct']:.1f}%\n")

    # Viral load
    if 'HIV viral load (copies/mL)' in stats_dict:
        vl = stats_dict['HIV viral load (copies/mL)']
        report_lines.append(f"- **Viral load:** median {vl['median']:.0f} copies/mL (range: {vl['min']:.0f}-{vl['max']:.0f})\n")
        report_lines.append(f"  - Missing: {vl['missing_pct']:.1f}%\n")

    # Identify issues
    issues = identify_issues(study, study_df, stats_dict)

    if issues:
        print(f"  Issues/Notes:")
        for issue in issues:
            print(f"    {issue}")

        report_lines.append("\n### ⚠️ Notable Findings\n")
        for issue in issues:
            report_lines.append(f"{issue}\n")
    else:
        print(f"  ✅ No major issues detected")
        report_lines.append("\n✅ **No major issues detected**\n")

    report_lines.append("\n---\n\n")
    print()

# Save report
with open('COMPREHENSIVE_STUDY_REVIEW.md', 'w') as f:
    f.writelines(report_lines)

print("="*80)
print("REVIEW COMPLETE")
print("="*80)
print()
print(f"Reviewed {len(studies)} studies")
print(f"Report saved to: COMPREHENSIVE_STUDY_REVIEW.md")
print()
