#!/opt/anaconda3/bin/python3
"""
Comprehensive Biomarker Availability Analysis
Creates visualizations and reports showing:
1. Which studies contribute which biomarkers
2. Variable naming consistency for cross-study comparability
3. Data availability and completeness
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("BIOMARKER AVAILABILITY ANALYSIS")
print("="*80)
print()

# Load dataset
print("📊 Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', low_memory=False)
print(f"✅ Loaded {len(df):,} records from {df['study_source'].nunique()} studies")
print()

# ============================================================================
# STEP 1: Define Biomarker Categories
# ============================================================================
print("🔬 Defining biomarker categories...")
print()

BIOMARKER_CATEGORIES = {
    'HIV Markers': [
        'CD4 cell count (cells/µL)',
        'CD8 cell count (cells/µL)',
        'HIV viral load (copies/mL)',
        'Antiretroviral Therapy Status',
    ],

    'Hematology': [
        'Hematocrit (%)',
        'hemoglobin_g_dL',
        'White blood cell count (×10³/µL)',
        'Platelet count (×10³/µL)',
        'Mean corpuscular volume (fL)',
        'Mean corpuscular hemoglobin (pg)',
        'Mean corpuscular hemoglobin concentration (g/dL)',
        'Red cell distribution width (%)',
        'Neutrophil count (×10³/µL)',
        'Lymphocyte count (×10³/µL)',
        'Monocyte count (×10³/µL)',
        'Eosinophil count (×10³/µL)',
        'Basophil count (×10³/µL)',
        'neutrophils_percent',
        'lymphocytes_percent',
        'monocytes_percent',
        'eosinophils_percent',
        'basophils_percent',
    ],

    'Biochemistry - Liver': [
        'ALT (U/L)',
        'AST (U/L)',
        'Alkaline phosphatase (U/L)',
        'Total bilirubin (mg/dL)',
        'Direct bilirubin (mg/dL)',
        'Albumin (g/dL)',
        'Total protein (g/dL)',
        'Gamma-glutamyl transferase (U/L)',
    ],

    'Biochemistry - Renal': [
        'creatinine_umol_L',
        'Blood urea nitrogen (mg/dL)',
        'urea_mmol_L',
        'Estimated glomerular filtration rate (mL/min/1.73m²)',
        'Creatinine clearance (mL/min)',
    ],

    'Electrolytes': [
        'sodium_mmol_L',
        'potassium_mmol_L',
        'chloride_mmol_L',
        'bicarbonate_mmol_L',
        'calcium_mmol_L',
        'magnesium_mmol_L',
        'phosphate_mmol_L',
    ],

    'Lipids': [
        'Total cholesterol (mg/dL)',
        'HDL cholesterol (mg/dL)',
        'LDL cholesterol (mg/dL)',
        'VLDL cholesterol (mg/dL)',
        'Triglycerides (mg/dL)',
        'cholesterol_hdl_ratio',
    ],

    'Metabolic': [
        'glucose_mmol_L',
        'Fasting glucose (mg/dL)',
        'HbA1c (%)',
        'Insulin (µIU/mL)',
        'Lactate (mmol/L)',
    ],

    'Inflammatory': [
        'C-reactive protein (mg/L)',
        'Erythrocyte sedimentation rate (mm/hr)',
    ],

    'Other Labs': [
        'Uric acid (mg/dL)',
        'Lactate dehydrogenase (U/L)',
        'Amylase (U/L)',
        'Lipase (U/L)',
        'Creatine kinase (U/L)',
    ],

    'Coagulation': [
        'Prothrombin time (seconds)',
        'International normalized ratio',
        'Activated partial thromboplastin time (seconds)',
    ],
}

# Flatten all biomarkers
all_biomarkers = []
for category, biomarkers in BIOMARKER_CATEGORIES.items():
    all_biomarkers.extend(biomarkers)

print(f"Total biomarker variables defined: {len(all_biomarkers)}")
print()

# ============================================================================
# STEP 2: Build Availability Matrix
# ============================================================================
print("📋 Building biomarker availability matrix...")
print()

studies = sorted(df['study_source'].unique())
availability_data = []

for biomarker in all_biomarkers:
    if biomarker not in df.columns:
        # Biomarker not in dataset at all
        row = {'Biomarker': biomarker, 'Total_Studies': 0, 'Total_Records': 0}
        for study in studies:
            row[study] = 0
        availability_data.append(row)
        continue

    # Count how many studies have this biomarker with data
    studies_with_data = 0
    total_records_with_data = 0
    row = {'Biomarker': biomarker}

    for study in studies:
        study_df = df[df['study_source'] == study]
        n_with_data = study_df[biomarker].notna().sum()

        if n_with_data > 0:
            studies_with_data += 1
            total_records_with_data += n_with_data
            row[study] = n_with_data
        else:
            row[study] = 0

    row['Total_Studies'] = studies_with_data
    row['Total_Records'] = total_records_with_data
    availability_data.append(row)

availability_df = pd.DataFrame(availability_data)

# Reorder columns: Biomarker, Total_Studies, Total_Records, then studies
cols = ['Biomarker', 'Total_Studies', 'Total_Records'] + studies
availability_df = availability_df[cols]

# Sort by Total_Studies descending
availability_df = availability_df.sort_values('Total_Studies', ascending=False)

print(f"✅ Availability matrix built: {len(availability_df)} biomarkers × {len(studies)} studies")
print()

# ============================================================================
# STEP 3: Summary Statistics
# ============================================================================
print("="*80)
print("BIOMARKER AVAILABILITY SUMMARY")
print("="*80)
print()

for category, biomarkers in BIOMARKER_CATEGORIES.items():
    category_biomarkers = [b for b in biomarkers if b in df.columns]
    if not category_biomarkers:
        print(f"❌ {category}: 0/{len(biomarkers)} biomarkers available")
        continue

    print(f"📊 {category}: {len(category_biomarkers)}/{len(biomarkers)} biomarkers available")

    # For each biomarker in category, show availability
    for biomarker in biomarkers:
        if biomarker not in df.columns:
            print(f"  ❌ {biomarker}: NOT FOUND IN DATASET")
            continue

        row = availability_df[availability_df['Biomarker'] == biomarker].iloc[0]
        n_studies = row['Total_Studies']
        n_records = row['Total_Records']

        if n_studies == 0:
            print(f"  ⚠️  {biomarker}: 0 studies, 0 records")
        elif n_studies < 3:
            print(f"  ⚠️  {biomarker}: {n_studies} studies, {n_records:,} records (LIMITED)")
        else:
            print(f"  ✅ {biomarker}: {n_studies} studies, {n_records:,} records")

    print()

# ============================================================================
# STEP 4: Create Heatmap Visualization
# ============================================================================
print("="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)
print()

# Create binary matrix for heatmap (has data = 1, no data = 0)
heatmap_data = availability_df[studies].copy()
heatmap_data = (heatmap_data > 0).astype(int)
heatmap_data.index = availability_df['Biomarker']

# Create figure with better size
fig, ax = plt.subplots(figsize=(20, 30))

# Create heatmap
sns.heatmap(
    heatmap_data,
    cmap=['white', '#2E7D32'],  # white = no data, green = has data
    cbar_kws={'label': 'Data Available'},
    linewidths=0.5,
    linecolor='lightgray',
    ax=ax,
    yticklabels=True,
    xticklabels=True,
    cbar=True
)

# Customize
ax.set_title('Biomarker Availability Across Studies', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('Study', fontsize=14, fontweight='bold')
ax.set_ylabel('Biomarker', fontsize=14, fontweight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=9)

plt.tight_layout()
plt.savefig('biomarker_availability_heatmap.png', dpi=300, bbox_inches='tight')
print("✅ Saved: biomarker_availability_heatmap.png")

# ============================================================================
# STEP 5: Create Category Summary Visualization
# ============================================================================

# Count biomarkers per category per study
category_summary = []

for study in studies:
    study_df = df[df['study_source'] == study]
    row = {'Study': study}

    for category, biomarkers in BIOMARKER_CATEGORIES.items():
        available = sum(1 for b in biomarkers if b in df.columns and study_df[b].notna().any())
        row[category] = available

    category_summary.append(row)

category_df = pd.DataFrame(category_summary)
category_df = category_df.set_index('Study')

# Create stacked bar chart
fig, ax = plt.subplots(figsize=(16, 10))

category_df.plot(
    kind='bar',
    stacked=True,
    ax=ax,
    colormap='tab20',
    width=0.8
)

ax.set_title('Biomarker Categories Available by Study', fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Study', fontsize=14, fontweight='bold')
ax.set_ylabel('Number of Biomarkers', fontsize=14, fontweight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('biomarker_categories_by_study.png', dpi=300, bbox_inches='tight')
print("✅ Saved: biomarker_categories_by_study.png")

plt.close('all')

# ============================================================================
# STEP 6: Variable Naming Consistency Check
# ============================================================================
print()
print("="*80)
print("VARIABLE NAMING CONSISTENCY CHECK")
print("="*80)
print()

print("🔍 Checking for potential naming inconsistencies...")
print()

# Look for similar variable names that might represent the same thing
all_columns = df.columns.tolist()

# Check for case variations
naming_issues = []

def normalize_name(name):
    """Normalize name for comparison"""
    return name.lower().replace(' ', '').replace('_', '').replace('(', '').replace(')', '').replace('×', 'x')

normalized_groups = {}
for col in all_columns:
    norm = normalize_name(col)
    if norm not in normalized_groups:
        normalized_groups[norm] = []
    normalized_groups[norm].append(col)

# Find groups with multiple variants
inconsistent = [(variants) for norm, variants in normalized_groups.items() if len(variants) > 1]

if inconsistent:
    print(f"⚠️  Found {len(inconsistent)} variable groups with potential naming inconsistencies:")
    print()
    for variants in inconsistent[:10]:  # Show first 10
        print(f"  • {', '.join(variants)}")
    print()
    if len(inconsistent) > 10:
        print(f"  ... and {len(inconsistent) - 10} more")
        print()
else:
    print("✅ No obvious naming inconsistencies detected")
    print()

# ============================================================================
# STEP 7: Cross-Study Comparability Report
# ============================================================================
print("="*80)
print("CROSS-STUDY COMPARABILITY")
print("="*80)
print()

print("Checking key biomarkers for cross-study comparability...")
print()

key_biomarkers = [
    'CD4 cell count (cells/µL)',
    'HIV viral load (copies/mL)',
    'hemoglobin_g_dL',
    'White blood cell count (×10³/µL)',
    'Platelet count (×10³/µL)',
    'ALT (U/L)',
    'AST (U/L)',
    'creatinine_umol_L',
    'glucose_mmol_L',
]

comparability_report = []

for biomarker in key_biomarkers:
    if biomarker not in df.columns:
        print(f"❌ {biomarker}: NOT IN DATASET")
        continue

    # Get data range across all studies
    data = df[biomarker].dropna()

    if len(data) == 0:
        print(f"❌ {biomarker}: NO DATA")
        continue

    # Check for potential unit inconsistencies (huge range variations)
    studies_with_data = []
    for study in studies:
        study_df = df[df['study_source'] == study]
        study_data = study_df[biomarker].dropna()

        if len(study_data) > 0:
            studies_with_data.append({
                'study': study,
                'mean': study_data.mean(),
                'median': study_data.median(),
                'min': study_data.min(),
                'max': study_data.max(),
                'n': len(study_data)
            })

    if len(studies_with_data) < 2:
        print(f"ℹ️  {biomarker}: Only {len(studies_with_data)} study has data")
        continue

    # Check for outlier studies (mean > 10x different from median study)
    all_means = [s['mean'] for s in studies_with_data]
    median_mean = np.median(all_means)

    outliers = [s for s in studies_with_data if abs(s['mean'] - median_mean) > 10 * median_mean]

    if outliers:
        print(f"⚠️  {biomarker}: POTENTIAL UNIT INCONSISTENCY")
        print(f"   Median mean across studies: {median_mean:.2f}")
        for outlier in outliers:
            print(f"   {outlier['study']}: mean={outlier['mean']:.2f} (OUTLIER)")
        print()
    else:
        print(f"✅ {biomarker}: Comparable across {len(studies_with_data)} studies")

print()

# ============================================================================
# STEP 8: Save Reports
# ============================================================================
print("="*80)
print("SAVING REPORTS")
print("="*80)
print()

# Save availability matrix
availability_df.to_csv('biomarker_availability_matrix.csv', index=False)
print("✅ Saved: biomarker_availability_matrix.csv")

# Save category summary
category_df.to_csv('biomarker_categories_summary.csv')
print("✅ Saved: biomarker_categories_summary.csv")

# Create summary report
with open('BIOMARKER_AVAILABILITY_REPORT.md', 'w') as f:
    f.write("# Biomarker Availability Report\n\n")
    f.write(f"**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Dataset**: CLINICAL_DATASET_QUALITY_HARMONIZED.csv\n")
    f.write(f"**Total Records**: {len(df):,}\n")
    f.write(f"**Total Studies**: {len(studies)}\n\n")
    f.write("---\n\n")

    # Overall statistics
    total_biomarkers = len(all_biomarkers)
    available_biomarkers = len([b for b in all_biomarkers if b in df.columns and df[b].notna().any()])

    f.write("## Overall Statistics\n\n")
    f.write(f"- **Biomarkers Defined**: {total_biomarkers}\n")
    f.write(f"- **Biomarkers Available**: {available_biomarkers} ({100*available_biomarkers/total_biomarkers:.1f}%)\n")
    f.write(f"- **Biomarkers Missing**: {total_biomarkers - available_biomarkers}\n\n")

    # Category breakdown
    f.write("## Biomarker Availability by Category\n\n")

    for category, biomarkers in BIOMARKER_CATEGORIES.items():
        category_available = len([b for b in biomarkers if b in df.columns and df[b].notna().any()])
        f.write(f"### {category}\n")
        f.write(f"**Available**: {category_available}/{len(biomarkers)} biomarkers\n\n")

        for biomarker in biomarkers:
            if biomarker not in df.columns:
                f.write(f"- ❌ **{biomarker}**: Not in dataset\n")
            else:
                row = availability_df[availability_df['Biomarker'] == biomarker].iloc[0]
                n_studies = row['Total_Studies']
                n_records = row['Total_Records']

                if n_studies == 0:
                    f.write(f"- ⚠️  **{biomarker}**: No data\n")
                else:
                    f.write(f"- ✅ **{biomarker}**: {n_studies} studies, {n_records:,} records\n")

        f.write("\n")

    # Study summary
    f.write("## Biomarker Counts by Study\n\n")
    f.write("| Study | Total Biomarkers |\n")
    f.write("|-------|------------------|\n")

    for study in studies:
        study_df = df[df['study_source'] == study]
        n_biomarkers = sum(1 for b in all_biomarkers if b in df.columns and study_df[b].notna().any())
        f.write(f"| {study} | {n_biomarkers} |\n")

    f.write("\n")

print("✅ Saved: BIOMARKER_AVAILABILITY_REPORT.md")

print()
print("="*80)
print("✅ BIOMARKER AVAILABILITY ANALYSIS COMPLETE")
print("="*80)
print()
print(f"Generated files:")
print(f"  • biomarker_availability_heatmap.png")
print(f"  • biomarker_categories_by_study.png")
print(f"  • biomarker_availability_matrix.csv")
print(f"  • biomarker_categories_summary.csv")
print(f"  • BIOMARKER_AVAILABILITY_REPORT.md")
print()
