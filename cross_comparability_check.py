#!/opt/anaconda3/bin/python3
"""
Cross-Comparability Analysis for Biomarkers
Checks for:
1. Duplicate biomarkers with different naming/units
2. Unit consistency across studies
3. Value range consistency
"""
import pandas as pd
import numpy as np
import sys

print("="*100)
print("CROSS-COMPARABILITY ANALYSIS")
print("="*100)
print()

# Load data
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)

# Define biomarker groups that should be checked for duplicates/inconsistencies
biomarker_groups = {
    'Neutrophil Count': [
        'Neutrophil count (×10³/µL)',
        'Neutrophil count (×10⁹/L)',
        'Neutrophil count (×10⁹/L).1'
    ],
    'Lymphocyte Count': [
        'Lymphocyte count (×10³/µL)',
        'Lymphocyte count (×10⁹/L)',
        'Lymphocyte count (×10⁹/L).1'
    ],
    'Monocyte Count': [
        'Monocyte count (×10⁹/L)',
        'Monocyte count (×10⁹/L).1'
    ],
    'Eosinophil Count': [
        'Eosinophil count (×10⁹/L)',
        'Eosinophil count (×10⁹/L).1'
    ],
    'Basophil Count': [
        'Basophil count (×10⁹/L)',
        'Basophil count (×10⁹/L).1'
    ],
    'HDL Cholesterol': [
        'hdl_cholesterol_mg_dL',
        'FASTING HDL'
    ],
    'LDL Cholesterol': [
        'ldl_cholesterol_mg_dL',
        'FASTING LDL'
    ],
    'Total Cholesterol': [
        'total_cholesterol_mg_dL'
    ],
    'Triglycerides': [
        'Triglycerides (mg/dL)',
        'FASTING TRIGLYCERIDES'
    ],
    'Mean Corpuscular Hemoglobin': [
        'mch_pg'
    ],
    'Mean Corpuscular Hemoglobin Concentration': [
        'mchc_g_dL'
    ],
    'Red Cell Distribution Width': [
        'RDW'
    ],
    'Mean Corpuscular Volume': [
        'MCV (MEAN CELL VOLUME)',
        'Mean corpuscular volume (fL)'
    ],
    'Creatinine': [
        'creatinine_umol_L'
    ],
    'Creatinine Clearance': [
        'creatinine clearance'
    ],
    'Fasting Glucose': [
        'fasting_glucose_mmol_L'
    ],
    'Potassium': [
        'Potassium (mEq/L)'
    ]
}

# Check each biomarker group
issues_found = []
additional_biomarkers = []

for biomarker_name, column_names in biomarker_groups.items():
    # Filter to columns that exist
    existing_cols = [col for col in column_names if col in df.columns]

    if not existing_cols:
        continue

    print(f"\n{biomarker_name}")
    print("-" * 100)

    # Check if multiple columns exist (potential duplicate/unit issue)
    if len(existing_cols) > 1:
        issues_found.append(f"⚠️  {biomarker_name}: Multiple columns with different naming/units")
        print(f"  ⚠️  WARNING: Multiple columns detected (potential unit inconsistency)")

    for col in existing_cols:
        non_null = df[col].notna().sum()
        if non_null > 0:
            pct = (non_null / len(df)) * 100

            # Get stats
            values = df[col].dropna()
            mean_val = values.mean()
            median_val = values.median()
            min_val = values.min()
            max_val = values.max()

            print(f"  Column: {col}")
            print(f"    Records: {non_null:,} ({pct:.1f}%)")
            print(f"    Range: {min_val:.2f} - {max_val:.2f}")
            print(f"    Mean: {mean_val:.2f}, Median: {median_val:.2f}")

            # Check which studies contribute
            study_col = 'Clinical Study ID'
            if study_col in df.columns:
                study_counts = df[df[col].notna()].groupby(study_col)[col].agg(['count', 'mean', 'min', 'max'])
                print(f"    Contributing studies:")
                for study, row in study_counts.iterrows():
                    print(f"      {study}: n={int(row['count'])}, mean={row['mean']:.2f}, range=[{row['min']:.2f}, {row['max']:.2f}]")

            # Mark as additional biomarker if it has substantial data
            if non_null >= 100:
                additional_biomarkers.append((biomarker_name, col, non_null))

# Unit conversion analysis for neutrophils/lymphocytes (×10⁹/L vs ×10³/µL)
print("\n" + "="*100)
print("UNIT CONVERSION CHECK: Neutrophils and Lymphocytes")
print("="*100)
print("\nNote: ×10³/µL = ×10⁹/L (same unit, different notation)")
print("Values should be identical if properly harmonized\n")

# Check if values are consistent between ×10³/µL and ×10⁹/L columns
for cell_type in ['Neutrophil', 'Lymphocyte']:
    col_1 = f'{cell_type} count (×10³/µL)'
    col_2 = f'{cell_type} count (×10⁹/L).1'

    if col_1 in df.columns and col_2 in df.columns:
        # Find rows with data in both columns
        both_present = df[[col_1, col_2]].notna().all(axis=1)
        if both_present.sum() > 0:
            comparison = df[both_present][[col_1, col_2]]
            correlation = comparison[col_1].corr(comparison[col_2])
            mean_diff = (comparison[col_1] - comparison[col_2]).abs().mean()
            print(f"{cell_type} count:")
            print(f"  Rows with both values: {both_present.sum()}")
            print(f"  Correlation: {correlation:.4f}")
            print(f"  Mean absolute difference: {mean_diff:.4f}")
            if correlation < 0.99:
                issues_found.append(f"⚠️  {cell_type} count: Poor correlation between unit formats ({correlation:.4f})")

# Summary
print("\n" + "="*100)
print("SUMMARY")
print("="*100)

print(f"\n✅ ADDITIONAL BIOMARKERS DISCOVERED: {len(additional_biomarkers)}")
print("\nThese biomarkers were not in the original analysis but have substantial data:")
for biomarker, col, count in sorted(additional_biomarkers, key=lambda x: x[2], reverse=True):
    print(f"  • {biomarker:40} ({col}): {count:,} records")

print(f"\n⚠️  CROSS-COMPARABILITY ISSUES DETECTED: {len(issues_found)}")
if issues_found:
    print("\nIssues that need attention:")
    for issue in issues_found:
        print(f"  {issue}")
else:
    print("\n✅ No cross-comparability issues detected!")

print("\n" + "="*100)
