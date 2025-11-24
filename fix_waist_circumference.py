#!/usr/bin/env python3
"""
Fix waist circumference unit error: Convert from mm to cm
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("📊 Loading dataset...")
df = pd.read_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv')

print(f"✅ Loaded {len(df):,} records")
print()

# Check current waist circumference values
if 'Waist circumference (cm)' in df.columns:
    wc = df['Waist circumference (cm)'].dropna()
    print("BEFORE CORRECTION:")
    print(f"  Mean: {wc.mean():.2f} cm")
    print(f"  Median: {wc.median():.2f} cm")
    print(f"  Min: {wc.min():.2f} cm")
    print(f"  Max: {wc.max():.2f} cm")
    print(f"  Records with data: {len(wc)}")
    print()

    # Fix: Divide by 10 to convert mm to cm
    print("🔧 Applying correction: Dividing by 10 (mm → cm)...")
    df['Waist circumference (cm)'] = df['Waist circumference (cm)'] / 10.0

    # Verify correction
    wc_corrected = df['Waist circumference (cm)'].dropna()
    print()
    print("AFTER CORRECTION:")
    print(f"  Mean: {wc_corrected.mean():.2f} cm")
    print(f"  Median: {wc_corrected.median():.2f} cm")
    print(f"  Min: {wc_corrected.min():.2f} cm")
    print(f"  Max: {wc_corrected.max():.2f} cm")
    print()

    # Sanity check
    if 70 < wc_corrected.mean() < 120:
        print("✅ Values now in reasonable range for waist circumference!")
    else:
        print("⚠️  Values still outside reasonable range - check calculation")

    # Add correction tracking
    df['waist_circ_unit_correction_applied'] = df['Waist circumference (cm)'].notna()
    df['waist_circ_unit_correction_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print()
    print("💾 Saving corrected dataset...")
    df.to_csv('.claude/CLINICAL_DATASET_QUALITY_HARMONIZED.csv', index=False)
    print("✅ Dataset saved with waist circumference corrected!")
else:
    print("⚠️  Waist circumference variable not found in dataset")

print()
print("="*60)
print("WAIST CIRCUMFERENCE CORRECTION COMPLETE")
print("="*60)
