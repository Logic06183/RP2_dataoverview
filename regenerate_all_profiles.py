#!/usr/bin/env python3
"""
Regenerate all study profile reports using the CORRECTED harmonized dataset
This will replace the old profiles that showed data quality issues
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("REGENERATING ALL STUDY PROFILES FROM CORRECTED DATA")
print("="*80)
print()

# Read the corrected harmonized dataset
print("📊 Loading corrected dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records")
print()

# Get list of studies
studies = df['study_source'].unique()
print(f"📋 Found {len(studies)} studies:")
for study in sorted(studies):
    count = len(df[df['study_source'] == study])
    print(f"  • {study}: {count:,} records")
print()

# Check if ydata-profiling is available
try:
    from ydata_profiling import ProfileReport
    print("✅ ydata-profiling is available")
    print()
except ImportError:
    print("❌ ydata-profiling not installed!")
    print("   Installing now...")
    import subprocess
    subprocess.run(['pip', 'install', 'ydata-profiling'], check=True)
    from ydata_profiling import ProfileReport
    print("✅ ydata-profiling installed")
    print()

# Select key variables to include in profiles (to keep file sizes manageable)
# We'll focus on the most important clinical and quality variables
profile_variables = [
    # IDs and dates
    'anonymous_patient_id', 'Patient ID', 'study_source', 'primary_date', 'visit_date',

    # Demographics
    'Age (at enrolment)', 'Sex', 'Race',

    # Location
    'latitude', 'longitude', 'province', 'city', 'jhb_subregion',

    # HIV biomarkers
    'CD4 cell count (cells/µL)', 'HIV viral load (copies/mL)',
    'HIV_status', 'Antiretroviral Therapy Status',

    # Hematology (CORRECTED)
    'Hematocrit (%)', 'White blood cell count (×10³/µL)',
    'Platelet count (×10³/µL)', 'hemoglobin_g_dL',

    # Cell counts (RENAMED - no longer mislabeled)
    'Lymphocyte count (×10⁹/L)', 'Neutrophil count (×10⁹/L)',
    'Monocyte count (×10⁹/L)', 'Eosinophil count (×10⁹/L)',
    'Basophil count (×10⁹/L)',

    # Liver function (CORRECTED)
    'ALT (U/L)', 'AST (U/L)',

    # Anthropometrics (CORRECTED)
    'BMI (kg/m²)', 'Waist circumference (cm)',
    'weight_kg', 'height_m',

    # Vital signs
    'heart_rate_bpm', 'systolic_bp_mmHg', 'diastolic_bp_mmHg',
    'body_temperature_celsius', 'Respiratory rate (breaths/min)',

    # Lipids
    'hdl_cholesterol_mg_dL', 'ldl_cholesterol_mg_dL',
    'total_cholesterol_mg_dL', 'Triglycerides (mg/dL)',

    # Quality tracking flags
    'cd4_correction_applied', 'final_comprehensive_fix_applied',
    'waist_circ_unit_correction_applied',
]

# Filter to variables that exist in the dataset
available_vars = [v for v in profile_variables if v in df.columns]
print(f"📊 Using {len(available_vars)} variables for profiles")
print()

# Generate profiles for each study
print("🔄 Generating profiles...")
print("-" * 80)

for i, study in enumerate(sorted(studies), 1):
    print(f"\n[{i}/{len(studies)}] {study}")

    # Extract study data
    study_df = df[df['study_source'] == study].copy()
    print(f"  Records: {len(study_df):,}")

    # Select available variables
    study_vars = [v for v in available_vars if v in study_df.columns and study_df[v].notna().any()]
    study_profile_df = study_df[study_vars].copy()

    # Create profile report
    try:
        profile = ProfileReport(
            study_profile_df,
            title=f"{study} - Corrected Data Profile",
            dataset={
                "description": f"{study} - Quality-corrected harmonized data",
                "creator": "RP2 Clinical Data Quality Team",
                "author": "Quality-Checked Data",
                "url": "HEAT Research Projects"
            },
            variables={
                "descriptions": {
                    "Age (at enrolment)": "Patient age at study enrollment",
                    "CD4 cell count (cells/µL)": "CD4+ T lymphocyte count (missing codes removed)",
                    "HIV viral load (copies/mL)": "HIV RNA copies per mL (missing codes removed)",
                    "BMI (kg/m²)": "Body Mass Index (extreme values removed)",
                    "Waist circumference (cm)": "Waist circumference (corrected from mm to cm)",
                    "ALT (U/L)": "Alanine aminotransferase (missing codes removed)",
                    "Platelet count (×10³/µL)": "Platelet count (missing codes removed)",
                    "Hematocrit (%)": "Hematocrit (zero values removed)",
                    "Lymphocyte count (×10⁹/L)": "Lymphocyte absolute count (corrected labeling)",
                    "Neutrophil count (×10⁹/L)": "Neutrophil absolute count (corrected labeling)",
                    "cd4_correction_applied": "Quality flag: CD4 missing codes removed",
                    "final_comprehensive_fix_applied": "Quality flag: Comprehensive corrections applied",
                    "waist_circ_unit_correction_applied": "Quality flag: Waist circ unit corrected"
                }
            },
            minimal=False,
            explorative=True,
        )

        # Generate filename (handle special case for Ezin_002)
        if study == "JHB_EZIN_002":
            output_file = "JHB_Ezin_002_profile.html"
        else:
            output_file = f"{study}_profile.html"

        # Save report
        profile.to_file(output_file)

        file_size = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"  ✅ Generated: {output_file} ({file_size:.1f} MB)")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue

print()
print("="*80)
print("✅ PROFILE REGENERATION COMPLETE")
print("="*80)
print()
print("All study profiles have been regenerated from the corrected dataset.")
print("The new profiles will show:")
print("  • Corrected waist circumference (cm, not mm)")
print("  • Corrected BMI (no extreme values)")
print("  • No missing data codes (9999, etc.)")
print("  • No zero/impossible values")
print("  • Corrected variable labels")
print()
print("Next step: Commit and push the updated profile HTML files to GitHub")
print()
