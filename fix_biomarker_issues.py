#!/opt/anaconda3/bin/python3
"""
Biomarker Harmonization and Correction Script
Fixes:
1. Lipid panel unit mislabeling (mg/dL → mmol/L)
2. Duplicate column consolidation
3. Creates final harmonized biomarker dataset
"""
import pandas as pd
import numpy as np
import sys
from datetime import datetime

print("="*100)
print("BIOMARKER HARMONIZATION AND CORRECTION")
print("="*100)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Load data
print("Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"  Loaded {len(df):,} records with {len(df.columns)} columns")
print()

# Track all changes
changes_log = []

# =============================================================================
# STEP 1: FIX LIPID PANEL UNIT LABELS
# =============================================================================
print("STEP 1: Fixing Lipid Panel Unit Labels")
print("-" * 100)

lipid_renames = {
    'hdl_cholesterol_mg_dL': 'hdl_cholesterol_mmol_L',
    'ldl_cholesterol_mg_dL': 'ldl_cholesterol_mmol_L',
    'total_cholesterol_mg_dL': 'total_cholesterol_mmol_L',
    'Triglycerides (mg/dL)': 'triglycerides_mmol_L'
}

for old_name, new_name in lipid_renames.items():
    if old_name in df.columns:
        df.rename(columns={old_name: new_name}, inplace=True)
        changes_log.append(f"Renamed: {old_name} → {new_name}")
        print(f"  ✅ Renamed: {old_name} → {new_name}")

print()

# =============================================================================
# STEP 2: CONSOLIDATE DUPLICATE COLUMNS
# =============================================================================
print("STEP 2: Consolidating Duplicate Columns")
print("-" * 100)

# Define column consolidation rules
# Format: 'unified_name': [list of column names to merge, with priority order]
consolidation_rules = {
    # White blood cell differentials - consolidate different naming conventions
    'neutrophil_count_10e9_L': [
        'Neutrophil count (×10⁹/L).1',
        'Neutrophil count (×10⁹/L)',
        'Neutrophil count (×10³/µL)'
    ],
    'lymphocyte_count_10e9_L': [
        'Lymphocyte count (×10⁹/L).1',
        'Lymphocyte count (×10⁹/L)',
        'Lymphocyte count (×10³/µL)'
    ],
    'monocyte_count_10e9_L': [
        'Monocyte count (×10⁹/L).1',
        'Monocyte count (×10⁹/L)'
    ],
    'eosinophil_count_10e9_L': [
        'Eosinophil count (×10⁹/L).1',
        'Eosinophil count (×10⁹/L)'
    ],
    'basophil_count_10e9_L': [
        'Basophil count (×10⁹/L).1',
        'Basophil count (×10⁹/L)'
    ],

    # Mean corpuscular volume
    'mcv_fL': [
        'Mean corpuscular volume (fL)',
        'MCV (MEAN CELL VOLUME)'
    ],

    # Lipid panel - consolidate FASTING vs non-fasting (prefer FASTING as it has more data)
    'hdl_cholesterol_mmol_L_consolidated': [
        'FASTING HDL',
        'hdl_cholesterol_mmol_L'
    ],
    'ldl_cholesterol_mmol_L_consolidated': [
        'FASTING LDL',
        'ldl_cholesterol_mmol_L'
    ],
    'triglycerides_mmol_L_consolidated': [
        'FASTING TRIGLYCERIDES',
        'triglycerides_mmol_L'
    ],
}

consolidated_columns = {}

for unified_name, source_columns in consolidation_rules.items():
    # Find which source columns actually exist
    existing_sources = [col for col in source_columns if col in df.columns]

    if not existing_sources:
        continue

    print(f"\n  Consolidating: {unified_name}")
    print(f"    Source columns: {existing_sources}")

    # Create new consolidated column
    # Start with the first (highest priority) column
    consolidated = df[existing_sources[0]].copy()
    records_from_primary = consolidated.notna().sum()

    # Fill in missing values from subsequent columns
    for source_col in existing_sources[1:]:
        missing_mask = consolidated.isna()
        filled_count = missing_mask.sum()
        consolidated[missing_mask] = df.loc[missing_mask, source_col]
        records_added = filled_count - consolidated.isna().sum()

        if records_added > 0:
            print(f"      Added {records_added} records from {source_col}")

    # Add to dataframe
    df[unified_name] = consolidated
    consolidated_columns[unified_name] = existing_sources

    total_records = consolidated.notna().sum()
    print(f"    ✅ Created {unified_name}: {total_records:,} total records")
    changes_log.append(f"Consolidated {len(existing_sources)} columns into {unified_name}: {total_records} records")

print()

# =============================================================================
# STEP 3: RENAME OTHER COLUMNS FOR CONSISTENCY
# =============================================================================
print("STEP 3: Standardizing Column Names")
print("-" * 100)

# Rename columns to consistent snake_case format with units
standard_renames = {
    'hemoglobin_g_dL': 'hemoglobin_g_dL',  # Already good
    'creatinine_umol_L': 'creatinine_umol_L',  # Already good
    'mch_pg': 'mch_pg',  # Already good
    'mchc_g_dL': 'mchc_g_dL',  # Already good
    'RDW': 'rdw_percent',
    'creatinine clearance': 'creatinine_clearance_mL_min',
    'Potassium (mEq/L)': 'potassium_mEq_L',
    'Sodium (mEq/L)': 'sodium_mEq_L',
    'CD4 cell count (cells/µL)': 'cd4_count_cells_uL',
    'HIV viral load (copies/mL)': 'hiv_vl_copies_mL',
    'Antiretroviral Therapy Status': 'art_status',
    'White blood cell count (×10³/µL)': 'wbc_count_10e9_L',
    'Hematocrit (%)': 'hematocrit_percent',
    'Platelet count (×10³/µL)': 'platelet_count_10e9_L',
    'ALT (U/L)': 'alt_U_L',
    'AST (U/L)': 'ast_U_L',
    'Albumin (g/dL)': 'albumin_g_dL',
    'Total protein (g/dL)': 'total_protein_g_dL',
    'Alkaline phosphatase (U/L)': 'alkaline_phosphatase_U_L',
    'Total bilirubin (mg/dL)': 'total_bilirubin_mg_dL',
}

for old_name, new_name in standard_renames.items():
    if old_name in df.columns and new_name not in df.columns:
        df.rename(columns={old_name: new_name}, inplace=True)
        print(f"  ✅ Renamed: {old_name} → {new_name}")
        changes_log.append(f"Standardized: {old_name} → {new_name}")

print()

# =============================================================================
# STEP 4: REMOVE OLD DUPLICATE COLUMNS
# =============================================================================
print("STEP 4: Removing Old Duplicate Columns")
print("-" * 100)

columns_to_remove = set()
for unified_name, source_columns in consolidated_columns.items():
    columns_to_remove.update(source_columns)

# Only remove columns that were actually consolidated
columns_to_remove = [col for col in columns_to_remove if col in df.columns]

if columns_to_remove:
    print(f"  Removing {len(columns_to_remove)} duplicate columns:")
    for col in columns_to_remove:
        print(f"    - {col}")
        changes_log.append(f"Removed duplicate: {col}")

    df.drop(columns=columns_to_remove, inplace=True)
    print(f"  ✅ Removed {len(columns_to_remove)} columns")
else:
    print("  No duplicate columns to remove")

print()

# =============================================================================
# STEP 5: CREATE BIOMARKER INVENTORY
# =============================================================================
print("STEP 5: Creating Final Biomarker Inventory")
print("-" * 100)

# Define all biomarker columns (standardized names)
biomarker_categories = {
    'HIV Markers': [
        'cd4_count_cells_uL',
        'hiv_vl_copies_mL',
        'art_status'
    ],
    'Hematology': [
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
        'rdw_percent'
    ],
    'Liver Function': [
        'alt_U_L',
        'ast_U_L',
        'alkaline_phosphatase_U_L',
        'total_bilirubin_mg_dL',
        'albumin_g_dL',
        'total_protein_g_dL'
    ],
    'Renal Function': [
        'creatinine_umol_L',
        'creatinine_clearance_mL_min'
    ],
    'Electrolytes': [
        'sodium_mEq_L',
        'potassium_mEq_L'
    ],
    'Lipids': [
        'total_cholesterol_mmol_L',
        'hdl_cholesterol_mmol_L_consolidated',
        'ldl_cholesterol_mmol_L_consolidated',
        'triglycerides_mmol_L_consolidated'
    ],
    'Metabolic': [
        'fasting_glucose_mmol_L'
    ]
}

# Count available biomarkers
biomarker_summary = []
total_biomarkers = 0
available_biomarkers = 0

for category, biomarkers in biomarker_categories.items():
    category_available = 0
    category_total = len(biomarkers)

    print(f"\n  {category}:")
    for biomarker in biomarkers:
        if biomarker in df.columns:
            count = df[biomarker].notna().sum()
            if count > 0:
                pct = (count / len(df)) * 100
                print(f"    ✅ {biomarker:45} {count:6,} records ({pct:5.1f}%)")
                category_available += 1
                available_biomarkers += 1
            else:
                print(f"    ⚠️  {biomarker:45} Column exists, no data")
        else:
            print(f"    ❌ {biomarker:45} Not in dataset")

        total_biomarkers += 1

    biomarker_summary.append({
        'Category': category,
        'Available': category_available,
        'Total': category_total,
        'Percentage': f"{(category_available/category_total)*100:.1f}%"
    })

print()
print("="*100)
print(f"BIOMARKER SUMMARY: {available_biomarkers}/{total_biomarkers} available ({(available_biomarkers/total_biomarkers)*100:.1f}%)")
print("="*100)

# =============================================================================
# STEP 6: SAVE CORRECTED DATASET
# =============================================================================
print("\nSTEP 6: Saving Corrected Dataset")
print("-" * 100)

output_file = '.claude/CLINICAL_DATASET_BIOMARKERS_HARMONIZED.csv'
df.to_csv(output_file, index=False)
print(f"  ✅ Saved corrected dataset: {output_file}")
print(f"  Records: {len(df):,}")
print(f"  Columns: {len(df.columns)}")

# Create backup of original if it doesn't exist
import shutil
backup_file = '.claude/CLINICAL_DATASET_QUALITY_HARMONIZED_BACKUP.csv'
original_file = '.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv'

try:
    if not os.path.exists(backup_file):
        shutil.copy(original_file, backup_file)
        print(f"  ✅ Created backup: {backup_file}")
except Exception as e:
    print(f"  ⚠️  Could not create backup: {e}")

# =============================================================================
# STEP 7: GENERATE CHANGE LOG
# =============================================================================
print("\nSTEP 7: Generating Change Log")
print("-" * 100)

change_log_file = 'BIOMARKER_HARMONIZATION_CHANGES.md'
with open(change_log_file, 'w') as f:
    f.write("# Biomarker Harmonization Change Log\n\n")
    f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Input**: CLINICAL_DATASET_QUALITY_HARMONIZED.csv\n")
    f.write(f"**Output**: CLINICAL_DATASET_BIOMARKERS_HARMONIZED.csv\n\n")
    f.write("---\n\n")

    f.write("## Changes Applied\n\n")
    f.write(f"**Total Changes**: {len(changes_log)}\n\n")

    f.write("### 1. Lipid Panel Unit Corrections\n\n")
    for change in changes_log:
        if 'cholesterol' in change.lower() or 'triglyceride' in change.lower():
            if 'Renamed' in change:
                f.write(f"- {change}\n")

    f.write("\n### 2. Column Consolidations\n\n")
    for change in changes_log:
        if 'Consolidated' in change:
            f.write(f"- {change}\n")

    f.write("\n### 3. Standardized Column Names\n\n")
    for change in changes_log:
        if 'Standardized' in change:
            f.write(f"- {change}\n")

    f.write("\n### 4. Removed Duplicate Columns\n\n")
    for change in changes_log:
        if 'Removed duplicate' in change:
            f.write(f"- {change}\n")

    f.write("\n---\n\n")
    f.write("## Final Biomarker Summary\n\n")
    f.write(f"| Category | Available | Total | Coverage |\n")
    f.write(f"|----------|-----------|-------|----------|\n")
    for item in biomarker_summary:
        f.write(f"| {item['Category']} | {item['Available']} | {item['Total']} | {item['Percentage']} |\n")

    f.write(f"\n**TOTAL**: {available_biomarkers}/{total_biomarkers} biomarkers available ({(available_biomarkers/total_biomarkers)*100:.1f}%)\n")

print(f"  ✅ Change log saved: {change_log_file}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print()
print("="*100)
print("HARMONIZATION COMPLETE")
print("="*100)
print(f"\n✅ All corrections applied successfully!")
print(f"\nKey Changes:")
print(f"  • Fixed lipid panel unit labels (mg/dL → mmol/L)")
print(f"  • Consolidated {len(consolidated_columns)} sets of duplicate columns")
print(f"  • Standardized column naming conventions")
print(f"  • Final dataset: {available_biomarkers} biomarkers with data")
print()
print(f"Output files:")
print(f"  • {output_file}")
print(f"  • {change_log_file}")
print()
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*100)
