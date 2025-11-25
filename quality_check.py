#!/opt/anaconda3/bin/python3
"""
Quality Check Script for RP2 Clinical Dataset
Identifies potential data quality issues for review
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("QUALITY CHECK: RP2 CLINICAL DATASET")
print("="*80)
print()

# Load dataset
print("📊 Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records from {df['study_source'].nunique()} studies")
print()

# Quality checks
quality_issues = []

def add_issue(category, variable, issue_description, count, examples=None):
    """Add a quality issue to the list"""
    quality_issues.append({
        'category': category,
        'variable': variable,
        'issue': issue_description,
        'count': count,
        'percent': round(100 * count / len(df), 2) if len(df) > 0 else 0,
        'examples': examples[:5] if examples is not None and len(examples) > 0 else None
    })

print("🔍 Running quality checks...")
print("-" * 80)
print()

# ============================================================================
# CHECK 1: CD4 Counts
# ============================================================================
print("1. Checking CD4 cell counts...")
cd4_col = 'CD4 cell count (cells/µL)'
if cd4_col in df.columns:
    # Check for zero values
    cd4_zero = df[df[cd4_col] == 0]
    if len(cd4_zero) > 0:
        add_issue(
            'Zero Values',
            cd4_col,
            'CD4 count = 0 (physiologically possible but unusual)',
            len(cd4_zero),
            cd4_zero[['study_source', cd4_col]].to_dict('records')
        )
        print(f"   ⚠️  Found {len(cd4_zero)} records with CD4 = 0")
        print(f"      Distribution by study:")
        for study in cd4_zero['study_source'].value_counts().items():
            print(f"      - {study[0]}: {study[1]} records")

    # Check for extremely low values (< 50)
    cd4_very_low = df[(df[cd4_col] > 0) & (df[cd4_col] < 50)]
    if len(cd4_very_low) > 0:
        print(f"   ℹ️  Found {len(cd4_very_low)} records with CD4 < 50 (severe immunosuppression)")

    # Check for extremely high values (> 2000)
    cd4_very_high = df[df[cd4_col] > 2000]
    if len(cd4_very_high) > 0:
        add_issue(
            'Extreme Values',
            cd4_col,
            'CD4 count > 2000 (unusually high)',
            len(cd4_very_high),
            cd4_very_high[['study_source', cd4_col]].to_dict('records')
        )
        print(f"   ⚠️  Found {len(cd4_very_high)} records with CD4 > 2000")

    if len(cd4_zero) == 0 and len(cd4_very_high) == 0:
        print(f"   ✅ CD4 values look reasonable")
else:
    print(f"   ℹ️  CD4 column not found")
print()

# ============================================================================
# CHECK 2: HIV Viral Load
# ============================================================================
print("2. Checking HIV viral load...")
vl_col = 'HIV viral load (copies/mL)'
if vl_col in df.columns:
    # Check for zero values
    vl_zero = df[df[vl_col] == 0]
    if len(vl_zero) > 0:
        add_issue(
            'Zero Values',
            vl_col,
            'Viral load = 0 (may indicate undetectable or data entry error)',
            len(vl_zero)
        )
        print(f"   ℹ️  Found {len(vl_zero)} records with viral load = 0")

    # Check for extremely high values (> 1,000,000)
    vl_very_high = df[df[vl_col] > 1000000]
    if len(vl_very_high) > 0:
        add_issue(
            'Extreme Values',
            vl_col,
            'Viral load > 1,000,000 (unusually high)',
            len(vl_very_high),
            vl_very_high[['study_source', vl_col]].to_dict('records')
        )
        print(f"   ⚠️  Found {len(vl_very_high)} records with viral load > 1,000,000")

    if len(vl_very_high) == 0:
        print(f"   ✅ Viral load values look reasonable")
else:
    print(f"   ℹ️  Viral load column not found")
print()

# ============================================================================
# CHECK 3: Hematology - Check for zero/impossible values
# ============================================================================
print("3. Checking hematology values...")
hematology_checks = [
    ('Hematocrit (%)', 0, 60),
    ('hemoglobin_g_dL', 0, 20),
    ('White blood cell count (×10³/µL)', 0, 50),
    ('Red blood cell count (×10⁶/µL)', 0, 10),
    ('Platelet count (×10³/µL)', 0, 1000),
]

for col, min_val, max_val in hematology_checks:
    if col in df.columns:
        # Zero values
        zero_vals = df[df[col] == 0]
        if len(zero_vals) > 0:
            add_issue(
                'Zero Values',
                col,
                f'{col} = 0 (impossible value)',
                len(zero_vals),
                zero_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(zero_vals)} records with value = 0")

        # Extreme high values
        high_vals = df[df[col] > max_val]
        if len(high_vals) > 0:
            add_issue(
                'Extreme Values',
                col,
                f'{col} > {max_val} (unusually high)',
                len(high_vals),
                high_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(high_vals)} records > {max_val}")

print()

# ============================================================================
# CHECK 4: Biochemistry - Check for suspicious values
# ============================================================================
print("4. Checking biochemistry values...")
biochem_checks = [
    ('ALT (U/L)', 0, 500),
    ('AST (U/L)', 0, 500),
    ('creatinine_umol_L', 0, 500),
    ('Albumin (g/dL)', 0, 6),
]

for col, min_val, max_val in biochem_checks:
    if col in df.columns:
        # Very low values (< 1)
        very_low = df[(df[col] > 0) & (df[col] < 1)]
        if len(very_low) > 0:
            add_issue(
                'Suspicious Low Values',
                col,
                f'{col} < 1 (possibly missing code or unit error)',
                len(very_low),
                very_low[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(very_low)} records < 1")

        # Extreme high values
        high_vals = df[df[col] > max_val]
        if len(high_vals) > 0:
            add_issue(
                'Extreme Values',
                col,
                f'{col} > {max_val} (unusually high)',
                len(high_vals),
                high_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(high_vals)} records > {max_val}")

print()

# ============================================================================
# CHECK 5: Anthropometrics
# ============================================================================
print("5. Checking anthropometric values...")
anthro_checks = [
    ('BMI (kg/m²)', 10, 70, 'BMI'),
    ('weight_kg', 20, 200, 'Weight'),
    ('height_m', 1.0, 2.5, 'Height'),
    ('Waist circumference (cm)', 40, 200, 'Waist circumference'),
]

for col, min_val, max_val, label in anthro_checks:
    if col in df.columns:
        # Low values
        low_vals = df[(df[col] > 0) & (df[col] < min_val)]
        if len(low_vals) > 0:
            add_issue(
                'Extreme Low Values',
                col,
                f'{label} < {min_val} (physiologically unlikely)',
                len(low_vals),
                low_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(low_vals)} records < {min_val}")

        # High values
        high_vals = df[df[col] > max_val]
        if len(high_vals) > 0:
            add_issue(
                'Extreme High Values',
                col,
                f'{label} > {max_val} (physiologically unlikely)',
                len(high_vals),
                high_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(high_vals)} records > {max_val}")

print()

# ============================================================================
# CHECK 6: Vital Signs
# ============================================================================
print("6. Checking vital signs...")
vital_checks = [
    ('systolic_bp_mmHg', 70, 250, 'Systolic BP'),
    ('diastolic_bp_mmHg', 40, 150, 'Diastolic BP'),
    ('heart_rate_bpm', 40, 200, 'Heart rate'),
    ('body_temperature_celsius', 35, 42, 'Temperature'),
]

for col, min_val, max_val, label in vital_checks:
    if col in df.columns:
        # Zero values
        zero_vals = df[df[col] == 0]
        if len(zero_vals) > 0:
            add_issue(
                'Zero Values',
                col,
                f'{label} = 0 (impossible value)',
                len(zero_vals),
                zero_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(zero_vals)} records with value = 0")

        # Out of range
        low_vals = df[(df[col] > 0) & (df[col] < min_val)]
        high_vals = df[df[col] > max_val]

        if len(low_vals) > 0:
            add_issue(
                'Extreme Low Values',
                col,
                f'{label} < {min_val}',
                len(low_vals),
                low_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(low_vals)} records < {min_val}")

        if len(high_vals) > 0:
            add_issue(
                'Extreme High Values',
                col,
                f'{label} > {max_val}',
                len(high_vals),
                high_vals[['study_source', col]].to_dict('records')
            )
            print(f"   ⚠️  {col}: {len(high_vals)} records > {max_val}")

print()

# ============================================================================
# SUMMARY
# ============================================================================
print("="*80)
print("QUALITY CHECK SUMMARY")
print("="*80)
print()

if len(quality_issues) == 0:
    print("✅ No quality issues found!")
else:
    print(f"⚠️  Found {len(quality_issues)} potential quality issues:")
    print()

    # Group by category
    for category in sorted(set(issue['category'] for issue in quality_issues)):
        cat_issues = [i for i in quality_issues if i['category'] == category]
        print(f"\n{category}:")
        print("-" * 80)
        for issue in cat_issues:
            print(f"  • {issue['variable']}")
            print(f"    {issue['issue']}")
            print(f"    Count: {issue['count']:,} ({issue['percent']}%)")
            if issue['examples']:
                print(f"    Example studies affected: {', '.join(set(str(ex.get('study_source', 'Unknown')) for ex in issue['examples'][:3]))}")

    # Save to file
    print()
    print("-" * 80)
    print("💾 Saving detailed quality report...")

    df_issues = pd.DataFrame(quality_issues)
    df_issues = df_issues[['category', 'variable', 'issue', 'count', 'percent']]
    df_issues.to_csv('QUALITY_CHECK_REPORT.csv', index=False)
    print("✅ Saved to: QUALITY_CHECK_REPORT.csv")

print()
print("="*80)
print(f"Quality check completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
print()
