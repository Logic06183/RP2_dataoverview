#!/opt/anaconda3/bin/python3
"""
Fix variable naming inconsistencies and regenerate comprehensive profiles
with ALL available variables properly categorized
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("FIXING VARIABLE NAMES AND REGENERATING COMPREHENSIVE PROFILES")
print("="*80)
print()

# Load dataset
print("📊 Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records")
print()

# ============================================================================
# STEP 1: Fix Variable Naming Inconsistencies
# ============================================================================
print("🔧 Fixing variable naming inconsistencies...")
print()

# Fix 1: Standardize 'country' vs 'Country' -> use 'country'
if 'Country' in df.columns:
    print("  • Merging 'Country' into 'country'")
    # If both exist, use Country to fill missing values in country
    if 'country' in df.columns:
        df['country'] = df['country'].fillna(df['Country'])
        df = df.drop(columns=['Country'])
    else:
        df = df.rename(columns={'Country': 'country'})

# Fix 2: Remove 'season' if 'climate_season' exists (climate_season is more specific)
if 'season' in df.columns and 'climate_season' in df.columns:
    print("  • Removing generic 'season' (keeping 'climate_season')")
    df = df.drop(columns=['season'])

# Fix 3: Remove '[mislabeled]' suffix from differential count variables
mislabeled_cols = [col for col in df.columns if '[mislabeled]' in col]
if mislabeled_cols:
    print(f"  • Removing '[mislabeled]' suffix from {len(mislabeled_cols)} variables")
    rename_map = {col: col.replace(' [mislabeled]', '') for col in mislabeled_cols}
    df = df.rename(columns=rename_map)

# Save corrected dataset
print()
print("💾 Saving corrected dataset...")
df.to_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', index=False)
print("✅ Dataset saved with corrected variable names")
print()

# ============================================================================
# STEP 2: Define Comprehensive Variable Categories
# ============================================================================
print("📋 Categorizing ALL variables...")
print()

# Variables to COMPLETELY EXCLUDE from profiles (metadata, IDs, quality flags)
EXCLUDE_VARS = {
    # IDs
    'anonymous_patient_id', 'Patient ID', 'original_record_index',

    # Metadata dates
    'harmonization_date', 'cleaning_date', 'export_date',
    'consolidation_date', 'consolidation_source',

    # Quality correction tracking dates (not needed in profiles)
    'cd4_correction_date', 'final_comprehensive_fix_date',
    'dphru_053_final_corrections_date', 'ezin_002_final_corrections_date',
    'waist_circ_unit_correction_date', 'quality_harmonization_date',

    # Quality flags (SHOULD NOT APPEAR IN PROFILES)
    'cd4_correction_applied',
    'final_comprehensive_fix_applied',
    'waist_circ_unit_correction_applied',
    'dphru_053_final_corrections_applied',
    'ezin_002_final_corrections_applied',
    'sa_biomarker_standards',

    # Redundant/technical fields
    'primary_date_parsed', 'data_source', 'dataset_type', 'dataset_version',
    'quality_harmonization_version',

    # Geographic metadata (too technical for profiles)
    'coordinate_source', 'coordinate_precision', 'geographic_source',
    'johannesburg_metro_valid',
}

# Define category keywords to auto-categorize variables
DEMOGRAPHIC_KEYWORDS = {
    'age', 'sex', 'race', 'gender', 'ethnicity', 'education',
    'enrollment', 'enrolment', 'study_source', 'study_arm', 'study_visit',
    'treatment_arm', 'arm', 'cohort'
}

HEALTH_BIOMARKER_KEYWORDS = {
    # HIV
    'cd4', 'cd8', 'viral', 'hiv', 'art', 'antiretroviral', 'haart',

    # Anthropometry
    'bmi', 'weight', 'height', 'waist', 'hip', 'circumference',

    # Vitals
    'blood_pressure', 'bp', 'systolic', 'diastolic', 'heart_rate', 'pulse',
    'temperature', 'respiratory', 'oxygen', 'saturation',

    # Hematology
    'hematocrit', 'hemoglobin', 'hgb', 'wbc', 'rbc', 'platelet', 'mcv', 'mch',
    'mchc', 'rdw', 'neutrophil', 'lymphocyte', 'monocyte', 'eosinophil',
    'basophil', 'white_blood', 'red_blood',

    # Biochemistry
    'alt', 'ast', 'alkaline', 'phosphatase', 'bilirubin', 'albumin', 'protein',
    'creatinine', 'urea', 'bun', 'egfr', 'clearance',

    # Electrolytes
    'sodium', 'potassium', 'chloride', 'bicarbonate', 'calcium', 'magnesium',
    'phosphate',

    # Lipids
    'cholesterol', 'hdl', 'ldl', 'vldl', 'triglyceride',

    # Metabolic
    'glucose', 'hba1c', 'insulin', 'lactate',

    # Other
    'crp', 'esr', 'coagulation', 'pt', 'inr', 'aptt',
    'uric_acid', 'ldh', 'amylase', 'lipase', 'ck', 'ggt',
}

CLIMATE_KEYWORDS = {
    'climate', 'temperature', 'temp', 'heat', 'humidity', 'precipitation',
    'weather', 'anomaly', 'threshold', 'p90', 'p95', 'p99'
}

def categorize_variable(var_name):
    """Automatically categorize a variable based on its name"""
    var_lower = var_name.lower()

    # Check if it should be excluded
    if var_name in EXCLUDE_VARS:
        return 'EXCLUDE'

    # Check for climate keywords
    if any(keyword in var_lower for keyword in CLIMATE_KEYWORDS):
        return 'climate'

    # Check for health/biomarker keywords
    if any(keyword in var_lower for keyword in HEALTH_BIOMARKER_KEYWORDS):
        return 'health'

    # Check for demographic keywords
    if any(keyword in var_lower for keyword in DEMOGRAPHIC_KEYWORDS):
        return 'demographics'

    # Geographic/location variables -> demographics
    if any(keyword in var_lower for keyword in ['latitude', 'longitude', 'city', 'province', 'country', 'location', 'site', 'region']):
        return 'demographics'

    # Date/time variables -> demographics (for study timeline context)
    if any(keyword in var_lower for keyword in ['date', 'year', 'month', 'week', 'day', 'time', 'visit']):
        return 'demographics'

    # Risk scores and vulnerability -> health
    if any(keyword in var_lower for keyword in ['risk', 'score', 'vulnerability', 'severity']):
        return 'health'

    # Default to health if unclear
    return 'health'

# Categorize all variables in dataset
all_vars = df.columns.tolist()
categorized_vars = {
    'demographics': [],
    'health': [],
    'climate': [],
    'exclude': []
}

for var in all_vars:
    category = categorize_variable(var)
    if category == 'EXCLUDE':
        categorized_vars['exclude'].append(var)
    else:
        categorized_vars[category].append(var)

print(f"  Demographics: {len(categorized_vars['demographics'])} variables")
print(f"  Health & Biomarkers: {len(categorized_vars['health'])} variables")
print(f"  Climate: {len(categorized_vars['climate'])} variables")
print(f"  Excluded (metadata): {len(categorized_vars['exclude'])} variables")
print()

print("Excluded variables:")
for var in sorted(categorized_vars['exclude']):
    print(f"  - {var}")
print()

# ============================================================================
# STEP 3: Generate Profiles with ALL Variables
# ============================================================================

# Check if ydata-profiling is available
try:
    from ydata_profiling import ProfileReport
    print("✅ ydata-profiling is available")
    print()
except ImportError:
    print("❌ ydata-profiling not installed!")
    import subprocess
    subprocess.run(['/opt/anaconda3/bin/pip', 'install', 'ydata-profiling'], check=True)
    from ydata_profiling import ProfileReport
    print("✅ ydata-profiling installed")
    print()

studies = sorted(df['study_source'].unique())

print("🔄 Generating comprehensive profiles with ALL variables...")
print("-" * 80)
print()

for i, study in enumerate(studies, 1):
    print(f"[{i}/{len(studies)}] {study}")

    # Extract study data
    study_df = df[df['study_source'] == study].copy()
    print(f"  Records: {len(study_df):,}")

    # Build ordered variable list: Demographics → Health → Climate
    study_profile_vars = []

    # Add demographics
    demo_vars = [v for v in categorized_vars['demographics']
                 if v in study_df.columns and (study_df[v].notna()).any()]
    study_profile_vars.extend(demo_vars)

    # Add health
    health_vars = [v for v in categorized_vars['health']
                   if v in study_df.columns and (study_df[v].notna()).any()]
    study_profile_vars.extend(health_vars)

    # Add climate
    climate_vars = [v for v in categorized_vars['climate']
                    if v in study_df.columns and (study_df[v].notna()).any()]
    study_profile_vars.extend(climate_vars)

    # Create profile DataFrame
    study_profile_df = study_df[study_profile_vars].copy()

    print(f"  Variables: {len(study_profile_vars)} total")
    print(f"    - Demographics: {len(demo_vars)}")
    print(f"    - Health & Biomarkers: {len(health_vars)}")
    print(f"    - Climate: {len(climate_vars)}")

    # Generate profile
    try:
        profile = ProfileReport(
            study_profile_df,
            title=f"{study} Data Profile",
            dataset={
                "description": f"Quality-verified clinical data for {study}",
                "creator": "HEAT Research Programme",
                "author": "RP2 Clinical Data Team",
                "url": "https://github.com/Logic06183/RP2_dataoverview"
            },
            minimal=False,
            explorative=True,
        )

        # Generate filename
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
        import traceback
        traceback.print_exc()
        continue

    print()

print("="*80)
print("✅ COMPLETE: VARIABLE FIXES AND PROFILE REGENERATION")
print("="*80)
print()
print("Summary:")
print(f"  • Fixed variable naming inconsistencies")
print(f"  • Excluded {len(categorized_vars['exclude'])} metadata/quality flag variables")
print(f"  • Generated profiles with ALL {len(study_profile_vars)} available variables per study")
print(f"  • Profiles organized in 3 sections: Demographics → Health & Biomarkers → Climate")
print()
