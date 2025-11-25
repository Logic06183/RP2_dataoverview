#!/opt/anaconda3/bin/python3
"""
Generate Comprehensive Study Profiles from QA Dataset
Uses the quality-assured JOHANNESBURG_CLINICAL_ANALYSIS_READY dataset
with full ALCOA+ compliance and integrated climate data
"""
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import os
import json

print("="*100)
print("GENERATING PROFILES FROM QUALITY-ASSURED DATASET WITH CLIMATE LINKAGE")
print("="*100)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load QA dataset
qa_dataset_path = 'data_profiles/25111548/JOHANNESBURG_CLINICAL_ANALYSIS_READY.csv'
print(f"Loading QA dataset from: {qa_dataset_path}")
df = pd.read_csv(qa_dataset_path, low_memory=False)
print(f"  ✅ Loaded {len(df):,} records with {len(df.columns)} columns")

# Load QA report
qa_report_path = 'data_profiles/25111548/COMPREHENSIVE_QA_REPORT.json'
with open(qa_report_path, 'r') as f:
    qa_report = json.load(f)

print(f"  ✅ QA Framework: {qa_report['report_metadata']['framework']}")
print(f"  ✅ Unique patients: {qa_report['dataset_overview']['unique_patients']:,}")
print(f"  ✅ Studies: {qa_report['dataset_overview']['studies_included']}\n")

# Define variable groups for profiling
demographic_vars = ['patient_id', 'age_years', 'sex', 'race', 'city']
visit_vars = ['visit_date', 'year', 'month', 'season', 'latitude', 'longitude']

hiv_vars = ['hiv_status', 'hiv_positive', 'on_art', 'virally_suppressed',
            'cd4_count', 'viral_load', 'viral_load_undetectable', 'log10_viral_load']

hematology_vars = ['hemoglobin', 'hematocrit', 'rbc_count', 'wbc_count',
                   'platelet_count', 'mcv', 'mch', 'mchc', 'rdw',
                   'neutrophils_pct', 'lymphocytes_pct', 'monocytes_pct',
                   'eosinophils_pct', 'basophils_pct']

biochemistry_vars = ['fasting_glucose', 'total_cholesterol', 'hdl_cholesterol',
                     'ldl_cholesterol', 'triglycerides', 'creatinine',
                     'creatinine_clearance', 'bun', 'alt', 'ast', 'alp',
                     'total_bilirubin', 'albumin', 'total_protein',
                     'sodium', 'potassium', 'calcium']

vitals_vars = ['systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature',
               'respiratory_rate', 'oxygen_saturation']

anthropometry_vars = ['height_m', 'weight_kg', 'bmi', 'waist_circumference']

climate_vars = ['temp_mean_c', 'temp_max_c', 'temp_min_c', 'temp_range_c',
                'temp_lag1d', 'temp_lag3d', 'temp_lag7d', 'temp_lag14d',
                'temp_lag21d', 'temp_lag30d', 'temp_variability_7d',
                'temp_variability_30d', 'apparent_temp', 'temp_anomaly',
                'heat_wave_day', 'heat_stress_category']

# Get list of all studies
study_col = 'study_source'
studies = sorted(df[study_col].dropna().unique())

print(f"Generating profiles for {len(studies)} studies...")
print("Variable groups:")
print(f"  • Demographics: {len(demographic_vars)} variables")
print(f"  • HIV markers: {len(hiv_vars)} variables")
print(f"  • Hematology: {len(hematology_vars)} variables")
print(f"  • Biochemistry: {len(biochemistry_vars)} variables")
print(f"  • Vital signs: {len(vitals_vars)} variables")
print(f"  • Anthropometry: {len(anthropometry_vars)} variables")
print(f"  • Climate exposures: {len(climate_vars)} variables\n")

# Create profiles directory
os.makedirs('data_profiles', exist_ok=True)

# Generate profile for each study
successful = 0
failed = []

for i, study in enumerate(studies, 1):
    print(f"[{i}/{len(studies)}] Processing {study}...")

    # Filter data for this study
    study_df = df[df[study_col] == study].copy()

    if len(study_df) == 0:
        print(f"  ⚠️  No data for {study}, skipping\n")
        failed.append(study)
        continue

    # Build column list - only include columns with data
    columns_to_include = [study_col]  # Always include study source

    # Check each variable group
    for var_group in [demographic_vars, visit_vars, hiv_vars, hematology_vars,
                      biochemistry_vars, vitals_vars, anthropometry_vars, climate_vars]:
        for col in var_group:
            if col in study_df.columns and study_df[col].notna().sum() > 0:
                columns_to_include.append(col)

    # Remove duplicates while preserving order
    columns_to_include = list(dict.fromkeys(columns_to_include))

    # Create subset
    profile_df = study_df[columns_to_include].copy()

    # Count variables by type
    n_biomarkers = len([c for c in columns_to_include if c in hematology_vars + biochemistry_vars + hiv_vars])
    n_climate = len([c for c in columns_to_include if c in climate_vars])

    print(f"  Records: {len(profile_df):,}")
    print(f"  Total variables: {len(columns_to_include)}")
    print(f"  Biomarkers: {n_biomarkers}")
    print(f"  Climate variables: {n_climate}")

    try:
        # Generate profile (minimal=True for GitHub compatibility)
        profile = ProfileReport(
            profile_df,
            title=f"{study} - QA Dataset Profile (ALCOA+ Compliant)",
            minimal=True,
            explorative=False,
            config_file=None
        )

        # Save profile
        output_file = f'data_profiles/{study}_complete_profile.html'
        profile.to_file(output_file)

        print(f"  ✅ Profile saved: {output_file}\n")
        successful += 1

    except Exception as e:
        print(f"  ❌ ERROR generating profile: {str(e)}\n")
        failed.append(study)
        continue

# Generate overall dataset profile
print("\n" + "="*100)
print("GENERATING OVERALL DATASET PROFILE")
print("="*100 + "\n")

try:
    # Select all columns with at least some data
    overall_cols = [study_col]

    for col in df.columns:
        if col != study_col and df[col].notna().sum() > 0:
            overall_cols.append(col)

    overall_df = df[overall_cols].copy()

    print(f"Generating overall profile with {len(overall_cols)} columns...")
    print(f"  Total records: {len(overall_df):,}")
    print(f"  Unique patients: {qa_report['dataset_overview']['unique_patients']:,}")
    print(f"  Studies: {qa_report['dataset_overview']['studies_included']}")

    profile = ProfileReport(
        overall_df,
        title="Complete QA Dataset - All Studies Combined (ALCOA+ Compliant)",
        minimal=True,
        explorative=False
    )

    output_file = 'data_profiles/00_COMPLETE_DATASET_PROFILE.html'
    profile.to_file(output_file)

    print(f"\n✅ Overall profile saved: {output_file}\n")

except Exception as e:
    print(f"❌ ERROR generating overall profile: {str(e)}\n")

# Summary
print("="*100)
print("PROFILE GENERATION COMPLETE")
print("="*100)
print(f"\n✅ Successfully generated: {successful}/{len(studies)} study profiles")

if failed:
    print(f"\n❌ Failed profiles ({len(failed)}):")
    for study in failed:
        print(f"  - {study}")

print(f"\n📁 All profiles saved to: data_profiles/")
print(f"\n📊 Dataset Quality Metrics:")
print(f"  • QA Framework: {qa_report['report_metadata']['framework']}")
print(f"  • Total QA steps completed: {len(qa_report['report_metadata']['qa_steps_completed'])}")
print(f"  • Overall compliance: {qa_report['quality_metrics']['overall_compliance']['pass_rate']}")

print(f"\n🌡️  Climate Integration:")
print(f"  • Temperature metrics: Daily mean, max, min, range")
print(f"  • Lag periods: 1, 3, 7, 14, 21, 30 days")
print(f"  • Heat wave detection: Binary flag")
print(f"  • Heat stress categories: Categorical classification")

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)
