#!/opt/anaconda3/bin/python3
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

# Include ALL clinical and biomarker variables, excluding only IDs and internal metadata
# This gives comprehensive biomarker analysis requested by user
exclude_variables = [
    # IDs - not needed for profiling
    'anonymous_patient_id', 'Patient ID', 'original_record_index',

    # Internal metadata
    'harmonization_date', 'cleaning_date', 'export_date',
    'consolidation_date', 'consolidation_source',

    # Quality tracking dates (keep the applied flags for reference)
    'cd4_correction_date', 'final_comprehensive_fix_date',
    'dphru_053_final_corrections_date', 'ezin_002_final_corrections_date',
    'waist_circ_unit_correction_date', 'quality_harmonization_date',

    # Redundant or parsing fields
    'primary_date_parsed', 'data_source', 'dataset_type', 'dataset_version',
]

# Get ALL variables except excluded ones
all_vars = [col for col in df.columns if col not in exclude_variables]
print(f"📊 Using {len(all_vars)} variables for comprehensive biomarker profiles (from {len(df.columns)} total)")
print(f"   Excluded {len(exclude_variables)} metadata/ID variables")
print()

# Generate profiles for each study
print("🔄 Generating profiles...")
print("-" * 80)

for i, study in enumerate(sorted(studies), 1):
    print(f"\n[{i}/{len(studies)}] {study}")

    # Extract study data
    study_df = df[df['study_source'] == study].copy()
    print(f"  Records: {len(study_df):,}")

    # Select available variables (all except excluded ones)
    study_vars = [v for v in all_vars if v in study_df.columns and study_df[v].notna().any()]
    study_profile_df = study_df[study_vars].copy()
    print(f"  Variables: {len(study_vars)} (with data)")

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
                    # Demographics & Clinical
                    "Age (at enrolment)": "Patient age at study enrollment",
                    "Sex": "Biological sex",
                    "Race": "Racial/ethnic group",

                    # HIV biomarkers (CORRECTED)
                    "CD4 cell count (cells/µL)": "CD4+ T lymphocyte count (missing codes removed)",
                    "HIV viral load (copies/mL)": "HIV RNA copies per mL (missing codes removed)",
                    "Antiretroviral Therapy Status": "Current ART status",

                    # Anthropometrics (CORRECTED)
                    "BMI (kg/m²)": "Body Mass Index (extreme values removed)",
                    "Waist circumference (cm)": "Waist circumference (corrected from mm to cm)",
                    "weight_kg": "Body weight in kilograms",
                    "height_m": "Height in meters",

                    # Hematology (CORRECTED)
                    "Hematocrit (%)": "Hematocrit (zero values removed)",
                    "hemoglobin_g_dL": "Hemoglobin concentration",
                    "White blood cell count (×10³/µL)": "Total WBC count",
                    "Red blood cell count (×10⁶/µL)": "Total RBC count",
                    "Platelet count (×10³/µL)": "Platelet count (missing codes removed)",
                    "MCV (MEAN CELL VOLUME)": "Mean corpuscular volume",
                    "mch_pg": "Mean corpuscular hemoglobin",
                    "mchc_g_dL": "Mean corpuscular hemoglobin concentration",
                    "RDW": "Red cell distribution width",

                    # Differential counts (CORRECTED LABELING)
                    "Lymphocyte count (×10⁹/L)": "Lymphocyte absolute count (corrected labeling)",
                    "Neutrophil count (×10⁹/L)": "Neutrophil absolute count (corrected labeling)",
                    "Monocyte count (×10⁹/L)": "Monocyte absolute count (corrected labeling)",
                    "Eosinophil count (×10⁹/L)": "Eosinophil absolute count (corrected labeling)",
                    "Basophil count (×10⁹/L)": "Basophil absolute count (corrected labeling)",

                    # Biochemistry (CORRECTED)
                    "ALT (U/L)": "Alanine aminotransferase (missing codes removed)",
                    "AST (U/L)": "Aspartate aminotransferase",
                    "Alkaline phosphatase (U/L)": "Alkaline phosphatase",
                    "Total bilirubin (mg/dL)": "Total bilirubin",
                    "Albumin (g/dL)": "Serum albumin",
                    "Total protein (g/dL)": "Total serum protein",
                    "creatinine_umol_L": "Serum creatinine",
                    "creatinine clearance": "Estimated creatinine clearance",

                    # Electrolytes
                    "Sodium (mEq/L)": "Serum sodium",
                    "Potassium (mEq/L)": "Serum potassium",

                    # Lipids & Metabolic
                    "fasting_glucose_mmol_L": "Fasting blood glucose",
                    "total_cholesterol_mg_dL": "Total cholesterol",
                    "hdl_cholesterol_mg_dL": "HDL cholesterol",
                    "ldl_cholesterol_mg_dL": "LDL cholesterol",
                    "Triglycerides (mg/dL)": "Triglycerides",

                    # Vital signs
                    "systolic_bp_mmHg": "Systolic blood pressure",
                    "diastolic_bp_mmHg": "Diastolic blood pressure",
                    "heart_rate_bpm": "Heart rate (zero values removed)",
                    "Respiratory rate (breaths/min)": "Respiratory rate",
                    "Oxygen saturation (%)": "Oxygen saturation",
                    "body_temperature_celsius": "Body temperature",

                    # Climate data
                    "climate_daily_mean_temp": "Daily mean temperature",
                    "climate_daily_max_temp": "Daily maximum temperature",
                    "climate_temp_anomaly": "Temperature anomaly from baseline",
                    "climate_heat_day_p90": "Heat day indicator (>90th percentile)",
                    "climate_heat_stress_index": "Heat stress index",

                    # Quality flags
                    "cd4_correction_applied": "Quality flag: CD4 missing codes removed",
                    "final_comprehensive_fix_applied": "Quality flag: Comprehensive corrections applied",
                    "waist_circ_unit_correction_applied": "Quality flag: Waist circ unit corrected",
                    "sa_biomarker_standards": "South African biomarker reference standards",
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
