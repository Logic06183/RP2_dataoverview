#!/opt/anaconda3/bin/python3
"""
Audit variable names across all studies to identify:
1. Naming inconsistencies
2. Variables that should be comparable but have different names
3. Total variable inventory per study
"""

import pandas as pd
import numpy as np
from collections import defaultdict

print("="*80)
print("VARIABLE NAME AUDIT ACROSS STUDIES")
print("="*80)
print()

# Load dataset
print("📊 Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records from {df['study_source'].nunique()} studies")
print()

# Get all studies
studies = sorted(df['study_source'].unique())

# Metadata/ID columns to exclude from analysis
metadata_cols = [
    'study_source',
    'anonymous_patient_id', 'Patient ID', 'original_record_index',
    'harmonization_date', 'cleaning_date', 'export_date',
    'consolidation_date', 'consolidation_source',
    'cd4_correction_date', 'final_comprehensive_fix_date',
    'dphru_053_final_corrections_date', 'ezin_002_final_corrections_date',
    'waist_circ_unit_correction_date', 'quality_harmonization_date',
    'primary_date_parsed', 'data_source', 'dataset_type', 'dataset_version',
    # Quality correction flags - THESE SHOULD NOT BE IN PROFILES
    'cd4_correction_applied',
    'final_comprehensive_fix_applied',
    'waist_circ_unit_correction_applied',
    'dphru_053_final_corrections_applied',
    'ezin_002_final_corrections_applied',
    'sa_biomarker_standards',
]

# Build variable inventory by study
print("Building variable inventory by study...")
print()

study_vars = {}
var_by_study = defaultdict(list)

for study in studies:
    study_df = df[df['study_source'] == study]
    # Get all columns except metadata
    cols = [c for c in study_df.columns if c not in metadata_cols]
    # Filter to columns that have at least one non-null value
    cols_with_data = [c for c in cols if study_df[c].notna().any()]
    study_vars[study] = sorted(cols_with_data)

    for var in cols_with_data:
        var_by_study[var].append(study)

print(f"Found {len(var_by_study)} unique variables across all studies")
print()

# Analyze variable distribution
print("="*80)
print("VARIABLE INVENTORY BY STUDY")
print("="*80)
print()

for study in studies:
    n_vars = len(study_vars[study])
    print(f"{study}: {n_vars} variables")

print()
print("="*80)
print("VARIABLE NAMING CONSISTENCY CHECK")
print("="*80)
print()

# Look for potential naming issues
# Group variables by similarity (lowercase, spaces removed)
def normalize_name(name):
    """Normalize variable name for comparison"""
    return name.lower().replace(' ', '').replace('_', '').replace('(', '').replace(')', '')

normalized_groups = defaultdict(list)
for var in var_by_study.keys():
    norm = normalize_name(var)
    normalized_groups[norm].append(var)

# Find groups with multiple names
inconsistent_naming = []
for norm, var_list in normalized_groups.items():
    if len(var_list) > 1:
        inconsistent_naming.append(var_list)

if inconsistent_naming:
    print(f"⚠️  Found {len(inconsistent_naming)} variable groups with inconsistent naming:")
    print()
    for i, var_group in enumerate(inconsistent_naming, 1):
        print(f"{i}. {', '.join(var_group)}")
        # Show which studies have each variant
        for var in var_group:
            studies_with = var_by_study[var]
            print(f"   '{var}': {len(studies_with)} studies - {', '.join(studies_with[:3])}{'...' if len(studies_with) > 3 else ''}")
        print()
else:
    print("✅ No obvious naming inconsistencies detected")
    print()

# Check for similar variable names (potential duplicates)
print("="*80)
print("SIMILAR VARIABLE NAMES (Potential Duplicates)")
print("="*80)
print()

# Look for variables that differ only in case, units, or minor variations
similar_pairs = []
var_list = list(var_by_study.keys())

for i in range(len(var_list)):
    for j in range(i+1, len(var_list)):
        var1 = var_list[i]
        var2 = var_list[j]

        # Check if they're similar
        norm1 = normalize_name(var1)
        norm2 = normalize_name(var2)

        # If normalized versions are very similar (differ by few chars)
        if norm1 != norm2:
            # Check Levenshtein-like similarity
            if len(norm1) > 5 and len(norm2) > 5:
                # Simple check: one contains the other
                if norm1 in norm2 or norm2 in norm1:
                    similar_pairs.append((var1, var2))

if similar_pairs:
    print(f"⚠️  Found {len(similar_pairs)} pairs of similar variable names:")
    print()
    for var1, var2 in similar_pairs[:20]:  # Show first 20
        print(f"  • '{var1}' vs '{var2}'")
        studies1 = set(var_by_study[var1])
        studies2 = set(var_by_study[var2])
        overlap = studies1 & studies2
        if overlap:
            print(f"    ⚠️  Both present in: {', '.join(list(overlap)[:3])}")
        print()
else:
    print("✅ No similar variable names detected")
    print()

# Check for variables present in all studies
print("="*80)
print("COMMON VARIABLES (Present in multiple studies)")
print("="*80)
print()

# Count how many studies have each variable
var_counts = [(var, len(studies_list)) for var, studies_list in var_by_study.items()]
var_counts.sort(key=lambda x: x[1], reverse=True)

print("Variables present in 10+ studies:")
for var, count in var_counts:
    if count >= 10:
        print(f"  {var}: {count}/17 studies")

print()
print("Variables present in 5-9 studies:")
for var, count in var_counts:
    if 5 <= count < 10:
        print(f"  {var}: {count}/17 studies")

print()

# Save detailed inventory
print("="*80)
print("SAVING DETAILED INVENTORY")
print("="*80)
print()

# Create a matrix showing which studies have which variables
all_vars = sorted(var_by_study.keys())
matrix_data = []

for var in all_vars:
    row = {'variable': var, 'total_studies': len(var_by_study[var])}
    for study in studies:
        row[study] = 'X' if var in study_vars[study] else ''
    matrix_data.append(row)

matrix_df = pd.DataFrame(matrix_data)
matrix_df.to_csv('VARIABLE_INVENTORY_MATRIX.csv', index=False)
print("✅ Saved: VARIABLE_INVENTORY_MATRIX.csv")

# Save study-specific variable lists
with open('STUDY_VARIABLE_LISTS.txt', 'w') as f:
    for study in studies:
        f.write(f"\n{'='*80}\n")
        f.write(f"{study} ({len(study_vars[study])} variables)\n")
        f.write(f"{'='*80}\n\n")
        for var in study_vars[study]:
            f.write(f"  - {var}\n")
        f.write("\n")

print("✅ Saved: STUDY_VARIABLE_LISTS.txt")

print()
print("="*80)
print("AUDIT COMPLETE")
print("="*80)
print()
