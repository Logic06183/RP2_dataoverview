#!/opt/anaconda3/bin/python3
"""
Generate Complete Study Profiles with All Biomarkers
Uses the harmonized biomarker dataset
"""
import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import os

print("="*100)
print("GENERATING COMPLETE STUDY PROFILES WITH ALL BIOMARKERS")
print("="*100)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load harmonized dataset
print("Loading harmonized biomarker dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_BIOMARKERS_HARMONIZED.csv', low_memory=False)
print(f"  Loaded {len(df):,} records with {len(df.columns)} columns\n")

# Define all biomarker columns (harmonized names)
biomarker_columns = [
    # HIV Markers
    'cd4_count_cells_uL',
    'hiv_vl_copies_mL',
    'art_status',

    # Hematology
    'hemoglobin_g_dL',
    'hematocrit_percent',
    'wbc_count_10e9_L',
    'platelet_count_10e9_L',
    'neutrophil_count_10e9_L',
    'lymphocyte_count_10e9_L',
    'monocyte_count_10e9_L',
    'eosinophil_count_10e9_L',
    'basophil_count_10e9_L',
    'mcv_fL',
    'mch_pg',
    'mchc_g_dL',
    'rdw_percent',

    # Liver Function
    'alt_U_L',
    'ast_U_L',
    'alkaline_phosphatase_U_L',
    'total_bilirubin_mg_dL',
    'albumin_g_dL',
    'total_protein_g_dL',

    # Renal Function
    'creatinine_umol_L',
    'creatinine_clearance_mL_min',

    # Electrolytes
    'sodium_mEq_L',
    'potassium_mEq_L',

    # Lipids
    'total_cholesterol_mmol_L',
    'hdl_cholesterol_mmol_L_consolidated',
    'ldl_cholesterol_mmol_L_consolidated',
    'triglycerides_mmol_L_consolidated',

    # Metabolic
    'fasting_glucose_mmol_L',
]

# Get list of all studies
study_col = 'study_source'
studies = sorted(df[study_col].dropna().unique())

print(f"Generating profiles for {len(studies)} studies...")
print(f"Biomarkers to include: {len(biomarker_columns)}\n")

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

    # Select relevant columns: demographics, visit info, and biomarkers
    # Get all columns that exist in the dataframe
    demographic_cols = ['PARTICIPANT_ID', 'Age (at enrolment)', 'Sex', 'BMI (kg/m²)',
                        'city_name', 'province_name', 'country_name']
    visit_cols = ['Visit Date', 'study_week', 'Visit Type']

    columns_to_include = []

    # Add demographic columns if they exist
    for col in demographic_cols:
        if col in study_df.columns:
            columns_to_include.append(col)

    # Add visit columns if they exist
    for col in visit_cols:
        if col in study_df.columns:
            columns_to_include.append(col)

    # Add biomarker columns if they exist and have data
    biomarkers_included = 0
    for col in biomarker_columns:
        if col in study_df.columns:
            if study_df[col].notna().sum() > 0:
                columns_to_include.append(col)
                biomarkers_included += 1

    # Create subset
    profile_df = study_df[columns_to_include].copy()

    print(f"  Records: {len(profile_df):,}")
    print(f"  Biomarkers with data: {biomarkers_included}")

    try:
        # Generate profile
        profile = ProfileReport(
            profile_df,
            title=f"{study} - Complete Data Profile",
            minimal=False,
            explorative=True
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
    # Select key columns for overall profile
    overall_cols = [study_col]

    # Add demographic columns if they exist
    for col in ['Age (at enrolment)', 'Sex', 'BMI (kg/m²)']:
        if col in df.columns:
            overall_cols.append(col)

    # Add all biomarkers that have any data
    for col in biomarker_columns:
        if col in df.columns and df[col].notna().sum() > 0:
            overall_cols.append(col)

    overall_df = df[overall_cols].copy()

    print(f"Generating overall profile with {len(overall_cols)} columns...")

    profile = ProfileReport(
        overall_df,
        title="Complete Dataset - All Studies Combined",
        minimal=False,
        explorative=True
    )

    output_file = 'data_profiles/00_COMPLETE_DATASET_PROFILE.html'
    profile.to_file(output_file)

    print(f"✅ Overall profile saved: {output_file}\n")

except Exception as e:
    print(f"❌ ERROR generating overall profile: {str(e)}\n")

# Summary
print("="*100)
print("PROFILE GENERATION COMPLETE")
print("="*100)
print(f"\nSuccessfully generated: {successful}/{len(studies)} study profiles")

if failed:
    print(f"\nFailed profiles ({len(failed)}):")
    for study in failed:
        print(f"  - {study}")

print(f"\nAll profiles saved to: data_profiles/")
print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)
