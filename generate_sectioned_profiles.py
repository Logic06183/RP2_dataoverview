#!/opt/anaconda3/bin/python3
"""
Generate study profile reports with variables organized into sections:
1. Demographics
2. Health & Biomarkers
3. Climate

This presents the current, quality-verified data state.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("GENERATING SECTIONED STUDY PROFILES")
print("="*80)
print()

# Read the corrected harmonized dataset
print("📊 Loading corrected dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records")
print()

# Define variable sections
# ========================

# SECTION 1: DEMOGRAPHICS
demographics_vars = [
    'study_source',
    'Age (at enrolment)',
    'Sex',
    'Race',
    'enrollment_date',
    'visit_date',
    'primary_date',
    'study_arm',
    'study_visit',
    'Antiretroviral Therapy Status',
]

# SECTION 2: HEALTH & BIOMARKERS
health_biomarker_vars = [
    # Anthropometrics
    'BMI (kg/m²)',
    'weight_kg',
    'height_m',
    'Waist circumference (cm)',
    'hip_circumference_cm',
    'waist_hip_ratio',

    # Vital Signs
    'systolic_bp_mmHg',
    'diastolic_bp_mmHg',
    'heart_rate_bpm',
    'Respiratory rate (breaths/min)',
    'Oxygen saturation (%)',
    'body_temperature_celsius',

    # HIV Markers
    'CD4 cell count (cells/µL)',
    'HIV viral load (copies/mL)',
    'cd4_percent',
    'cd8_count_cells_uL',
    'cd4_cd8_ratio',

    # Hematology - Complete Blood Count
    'Hematocrit (%)',
    'hemoglobin_g_dL',
    'White blood cell count (×10³/µL)',
    'Red blood cell count (×10⁶/µL)',
    'Platelet count (×10³/µL)',
    'MCV (MEAN CELL VOLUME)',
    'mch_pg',
    'mchc_g_dL',
    'RDW',

    # Hematology - Differential
    'Lymphocyte count (×10⁹/L)',
    'Neutrophil count (×10⁹/L)',
    'Monocyte count (×10⁹/L)',
    'Eosinophil count (×10⁹/L)',
    'Basophil count (×10⁹/L)',
    'lymphocyte_percent',
    'neutrophil_percent',
    'monocyte_percent',
    'eosinophil_percent',
    'basophil_percent',

    # Liver Function
    'ALT (U/L)',
    'AST (U/L)',
    'Alkaline phosphatase (U/L)',
    'Total bilirubin (mg/dL)',
    'direct_bilirubin_mg_dL',
    'indirect_bilirubin_mg_dL',
    'Albumin (g/dL)',
    'Total protein (g/dL)',
    'ggt_u_L',

    # Renal Function
    'creatinine_umol_L',
    'creatinine_mg_dL',
    'creatinine clearance',
    'bun_mg_dL',
    'urea_mmol_L',
    'egfr_ml_min',

    # Electrolytes
    'Sodium (mEq/L)',
    'Potassium (mEq/L)',
    'chloride_mEq_L',
    'bicarbonate_mEq_L',
    'calcium_mg_dL',
    'magnesium_mg_dL',
    'phosphate_mg_dL',

    # Lipid Profile
    'total_cholesterol_mg_dL',
    'hdl_cholesterol_mg_dL',
    'ldl_cholesterol_mg_dL',
    'Triglycerides (mg/dL)',
    'vldl_cholesterol_mg_dL',
    'cholesterol_hdl_ratio',

    # Metabolic
    'fasting_glucose_mmol_L',
    'glucose_mg_dL',
    'hba1c_percent',
    'insulin_uIU_mL',
    'lactate_mmol_L',

    # Inflammatory Markers
    'crp_mg_L',
    'esr_mm_hr',

    # Coagulation
    'pt_seconds',
    'inr',
    'aptt_seconds',

    # Other Biomarkers
    'uric_acid_mg_dL',
    'ldh_u_L',
    'ck_u_L',
    'amylase_u_L',
    'lipase_u_L',

    # Quality Flags (for reference)
    'cd4_correction_applied',
    'final_comprehensive_fix_applied',
    'waist_circ_unit_correction_applied',
    'sa_biomarker_standards',
]

# SECTION 3: CLIMATE
climate_vars = [
    'climate_daily_mean_temp',
    'climate_daily_max_temp',
    'climate_daily_min_temp',
    'climate_temp_anomaly',
    'climate_heat_day_p90',
    'climate_heat_day_p95',
    'climate_heat_stress_index',
    'climate_humidity',
    'climate_precipitation',
    'climate_season',
]

# Exclude metadata variables
exclude_variables = [
    'anonymous_patient_id', 'Patient ID', 'original_record_index',
    'harmonization_date', 'cleaning_date', 'export_date',
    'consolidation_date', 'consolidation_source',
    'cd4_correction_date', 'final_comprehensive_fix_date',
    'dphru_053_final_corrections_date', 'ezin_002_final_corrections_date',
    'waist_circ_unit_correction_date', 'quality_harmonization_date',
    'primary_date_parsed', 'data_source', 'dataset_type', 'dataset_version',
]

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

# Variable descriptions
var_descriptions = {
    # Demographics
    "study_source": "Study identifier",
    "Age (at enrolment)": "Patient age at study enrollment",
    "Sex": "Biological sex",
    "Race": "Racial/ethnic group",
    "enrollment_date": "Date of study enrollment",
    "visit_date": "Date of clinic visit",
    "primary_date": "Primary reference date",
    "study_arm": "Study treatment arm",
    "study_visit": "Study visit number",
    "Antiretroviral Therapy Status": "Current ART status",

    # Anthropometrics
    "BMI (kg/m²)": "Body Mass Index",
    "weight_kg": "Body weight in kilograms",
    "height_m": "Height in meters",
    "Waist circumference (cm)": "Waist circumference in centimeters",
    "hip_circumference_cm": "Hip circumference in centimeters",
    "waist_hip_ratio": "Waist-to-hip ratio",

    # Vital Signs
    "systolic_bp_mmHg": "Systolic blood pressure",
    "diastolic_bp_mmHg": "Diastolic blood pressure",
    "heart_rate_bpm": "Heart rate in beats per minute",
    "Respiratory rate (breaths/min)": "Respiratory rate",
    "Oxygen saturation (%)": "Oxygen saturation",
    "body_temperature_celsius": "Body temperature in Celsius",

    # HIV Markers
    "CD4 cell count (cells/µL)": "CD4+ T lymphocyte count",
    "HIV viral load (copies/mL)": "HIV RNA copies per mL",
    "cd4_percent": "CD4+ percentage",
    "cd8_count_cells_uL": "CD8+ T lymphocyte count",
    "cd4_cd8_ratio": "CD4/CD8 ratio",

    # Hematology
    "Hematocrit (%)": "Hematocrit",
    "hemoglobin_g_dL": "Hemoglobin concentration",
    "White blood cell count (×10³/µL)": "Total WBC count",
    "Red blood cell count (×10⁶/µL)": "Total RBC count",
    "Platelet count (×10³/µL)": "Platelet count",
    "MCV (MEAN CELL VOLUME)": "Mean corpuscular volume",
    "mch_pg": "Mean corpuscular hemoglobin",
    "mchc_g_dL": "Mean corpuscular hemoglobin concentration",
    "RDW": "Red cell distribution width",
    "Lymphocyte count (×10⁹/L)": "Lymphocyte absolute count",
    "Neutrophil count (×10⁹/L)": "Neutrophil absolute count",
    "Monocyte count (×10⁹/L)": "Monocyte absolute count",
    "Eosinophil count (×10⁹/L)": "Eosinophil absolute count",
    "Basophil count (×10⁹/L)": "Basophil absolute count",
    "lymphocyte_percent": "Lymphocyte percentage",
    "neutrophil_percent": "Neutrophil percentage",
    "monocyte_percent": "Monocyte percentage",
    "eosinophil_percent": "Eosinophil percentage",
    "basophil_percent": "Basophil percentage",

    # Liver Function
    "ALT (U/L)": "Alanine aminotransferase",
    "AST (U/L)": "Aspartate aminotransferase",
    "Alkaline phosphatase (U/L)": "Alkaline phosphatase",
    "Total bilirubin (mg/dL)": "Total bilirubin",
    "direct_bilirubin_mg_dL": "Direct bilirubin",
    "indirect_bilirubin_mg_dL": "Indirect bilirubin",
    "Albumin (g/dL)": "Serum albumin",
    "Total protein (g/dL)": "Total serum protein",
    "ggt_u_L": "Gamma-glutamyl transferase",

    # Renal Function
    "creatinine_umol_L": "Serum creatinine (µmol/L)",
    "creatinine_mg_dL": "Serum creatinine (mg/dL)",
    "creatinine clearance": "Estimated creatinine clearance",
    "bun_mg_dL": "Blood urea nitrogen",
    "urea_mmol_L": "Serum urea",
    "egfr_ml_min": "Estimated glomerular filtration rate",

    # Electrolytes
    "Sodium (mEq/L)": "Serum sodium",
    "Potassium (mEq/L)": "Serum potassium",
    "chloride_mEq_L": "Serum chloride",
    "bicarbonate_mEq_L": "Serum bicarbonate",
    "calcium_mg_dL": "Serum calcium",
    "magnesium_mg_dL": "Serum magnesium",
    "phosphate_mg_dL": "Serum phosphate",

    # Lipids
    "total_cholesterol_mg_dL": "Total cholesterol",
    "hdl_cholesterol_mg_dL": "HDL cholesterol",
    "ldl_cholesterol_mg_dL": "LDL cholesterol",
    "Triglycerides (mg/dL)": "Triglycerides",
    "vldl_cholesterol_mg_dL": "VLDL cholesterol",
    "cholesterol_hdl_ratio": "Total cholesterol/HDL ratio",

    # Metabolic
    "fasting_glucose_mmol_L": "Fasting blood glucose (mmol/L)",
    "glucose_mg_dL": "Blood glucose (mg/dL)",
    "hba1c_percent": "Glycated hemoglobin",
    "insulin_uIU_mL": "Serum insulin",
    "lactate_mmol_L": "Blood lactate",

    # Inflammatory
    "crp_mg_L": "C-reactive protein",
    "esr_mm_hr": "Erythrocyte sedimentation rate",

    # Coagulation
    "pt_seconds": "Prothrombin time",
    "inr": "International normalized ratio",
    "aptt_seconds": "Activated partial thromboplastin time",

    # Other
    "uric_acid_mg_dL": "Serum uric acid",
    "ldh_u_L": "Lactate dehydrogenase",
    "ck_u_L": "Creatine kinase",
    "amylase_u_L": "Serum amylase",
    "lipase_u_L": "Serum lipase",

    # Climate
    "climate_daily_mean_temp": "Daily mean temperature",
    "climate_daily_max_temp": "Daily maximum temperature",
    "climate_daily_min_temp": "Daily minimum temperature",
    "climate_temp_anomaly": "Temperature anomaly from baseline",
    "climate_heat_day_p90": "Heat day indicator (>90th percentile)",
    "climate_heat_day_p95": "Heat day indicator (>95th percentile)",
    "climate_heat_stress_index": "Heat stress index",
    "climate_humidity": "Relative humidity",
    "climate_precipitation": "Precipitation",
    "climate_season": "Season",

    # Quality Flags
    "cd4_correction_applied": "Quality flag: CD4 corrections applied",
    "final_comprehensive_fix_applied": "Quality flag: Comprehensive corrections applied",
    "waist_circ_unit_correction_applied": "Quality flag: Waist circumference unit corrected",
    "sa_biomarker_standards": "South African biomarker reference standards applied",
}

# Generate profiles for each study
print("🔄 Generating sectioned profiles...")
print("-" * 80)

for i, study in enumerate(sorted(studies), 1):
    print(f"\n[{i}/{len(studies)}] {study}")

    # Extract study data
    study_df = df[df['study_source'] == study].copy()
    print(f"  Records: {len(study_df):,}")

    # Build combined variable list in order: Demographics → Health → Climate
    all_section_vars = demographics_vars + health_biomarker_vars + climate_vars

    # Filter to only variables that exist in this study and have data
    study_vars = [v for v in all_section_vars
                  if v in study_df.columns
                  and v not in exclude_variables
                  and study_df[v].notna().any()]

    study_profile_df = study_df[study_vars].copy()

    # Count variables by section
    demo_count = sum(1 for v in study_vars if v in demographics_vars)
    health_count = sum(1 for v in study_vars if v in health_biomarker_vars)
    climate_count = sum(1 for v in study_vars if v in climate_vars)

    print(f"  Variables: {len(study_vars)} total")
    print(f"    - Demographics: {demo_count}")
    print(f"    - Health & Biomarkers: {health_count}")
    print(f"    - Climate: {climate_count}")

    # Create profile report
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
            variables={
                "descriptions": var_descriptions
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
        import traceback
        traceback.print_exc()
        continue

print()
print("="*80)
print("✅ SECTIONED PROFILE GENERATION COMPLETE")
print("="*80)
print()
print("Profiles now organized in sections:")
print("  1. Demographics")
print("  2. Health & Biomarkers")
print("  3. Climate")
print()
