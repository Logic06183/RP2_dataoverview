# RP2 Data Quality Review System

**Systematic tools for identifying data anomalies across 17 clinical studies**

---

## What's Been Set Up

This folder now contains a complete data quality review system with the following components:

### 📋 Documentation Files

1. **`DATA_QUALITY_FINDINGS.md`** - Main findings tracker
   - Status table for all 17 studies
   - Structured templates for documenting issues
   - Priority classification system
   - Summary statistics

2. **`ANOMALY_DETECTION_CHECKLIST.md`** - Comprehensive review checklist
   - Step-by-step guide for what to check in each report
   - Common anomalies by variable type
   - Priority guidelines
   - Quick reference for red flags

3. **`REVIEW_WORKFLOW_GUIDE.md`** - Complete workflow instructions
   - Daily review workflow
   - Tips for efficient review
   - Example review session
   - Troubleshooting guide

4. **`QUALITY_REVIEW_README.md`** (this file) - System overview

### 🛠️ Tools

1. **`review_helper.py`** - Python helper script
   - List all studies
   - Open studies in browser
   - Track review progress
   - Navigate to next unreviewed study

---

## Quick Start

### First Time Setup (30 seconds)

```bash
# 1. Navigate to this folder
cd /Users/craig/Library/CloudStorage/OneDrive-WitsHealthConsortium/RP2_data_overview

# 2. Test the helper script
python review_helper.py --list

# 3. Open the workflow guide
open REVIEW_WORKFLOW_GUIDE.md
```

### Start Reviewing (Daily Use)

```bash
# Check your progress
python review_helper.py --status

# Open next study to review
python review_helper.py --next

# Follow the checklist (keep it open while reviewing)
open ANOMALY_DETECTION_CHECKLIST.md

# Document findings as you go
open DATA_QUALITY_FINDINGS.md
```

---

## File Structure

```
RP2_data_overview/
│
├── QUALITY_REVIEW_README.md          ← You are here
├── REVIEW_WORKFLOW_GUIDE.md          ← How to use the system
├── ANOMALY_DETECTION_CHECKLIST.md    ← What to look for
├── DATA_QUALITY_FINDINGS.md          ← Where to document issues
├── review_helper.py                  ← Navigation tool
│
├── JHB_ACTG_015_profile.html         ← Study 1 report
├── JHB_ACTG_016_profile.html         ← Study 2 report
├── ... (15 more study reports)
│
├── DATASET_STATUS_RESEARCH_REPORT.html       ← Quality overview
├── ENHANCED_DATASET_STATUS_REPORT.html       ← Quality summary
├── ULTRA_COMPREHENSIVE_REPORT.html           ← Complete analysis
│
└── JHB_ACTG_015/                     ← Study 1 visualizations
    ├── JHB_ACTG_015_missing_data.svg
    ├── JHB_ACTG_015_distributions.svg
    └── ... (more visualizations)
```

---

## Review Process Overview

```
┌─────────────────────────────────────────────────────┐
│  1. Open Next Study                                 │
│     python review_helper.py --next                  │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  2. Review HTML Report in Browser                   │
│     • Check summary statistics                      │
│     • Examine missing data heatmap                  │
│     • Review distribution plots                     │
│     • Check categorical frequencies                 │
│     (Use ANOMALY_DETECTION_CHECKLIST.md)           │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  3. Document Issues                                 │
│     • Add to DATA_QUALITY_FINDINGS.md              │
│     • Classify priority (High/Medium/Low)           │
│     • Note variables affected                       │
│     • Describe fix needed in JupyterHub            │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  4. Mark Study as Reviewed                          │
│     • Update status table: ⬜ → ✅                  │
│     • Add review date                               │
│     • Count issues found                            │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│  5. Repeat for Next Study                           │
│     python review_helper.py --next                  │
└─────────────────────────────────────────────────────┘

After reviewing several studies:

┌─────────────────────────────────────────────────────┐
│  6. Batch Fix in JupyterHub                         │
│     • Group by priority (fix High first)            │
│     • Update status in findings doc                 │
│     • Re-generate reports after fixes               │
└─────────────────────────────────────────────────────┘
```

---

## Helper Script Commands

```bash
# List all studies with file sizes
python review_helper.py --list

# Open a specific study
python review_helper.py --open JHB_ACTG_015

# Open next unreviewed study
python review_helper.py --next

# Check review progress
python review_helper.py --status

# Open quality/status reports
python review_helper.py --quality

# Open comprehensive reports
python review_helper.py --comprehensive

# Show help
python review_helper.py --help
```

---

## Common Anomalies to Watch For

### 🔴 Critical Issues (Fix Immediately)
- Negative ages or ages > 120
- Impossible biomarker values (e.g., negative blood pressure)
- Critical variables >50% missing
- Logical impossibilities (pregnant males, etc.)

### 🟡 Important Issues (Fix Before Analysis)
- Outliers >4 SD from mean
- Unit errors (lbs vs kg, mmol/L vs mg/dL)
- Missing data 20-50% on key variables
- Inconsistent category labels

### 🟢 Minor Issues (Fix When Convenient)
- Cosmetic labeling issues
- Minor outliers within plausible range
- Low-level missing data (<10%)

---

## Tips for Efficient Review

### Time Estimates
- **First study**: ~30 minutes (getting familiar)
- **Subsequent studies**: ~15-20 minutes each
- **Total for 17 studies**: ~6-8 hours spread over several sessions

### Best Practices

1. **Review in batches**
   - Do 3-5 studies per session
   - Then batch-fix in JupyterHub
   - More efficient than constant switching

2. **Start with quality reports**
   ```bash
   python review_helper.py --quality
   ```
   These highlight studies with known issues

3. **Use the visualizations**
   - Missing data heatmaps show patterns instantly
   - Distribution plots reveal outliers quickly
   - Don't read every number - let visuals guide you

4. **Look for patterns across studies**
   - Same issue in multiple studies from one network?
   - May indicate systematic data collection issue

5. **Don't fix here - just document**
   - All fixes happen in JupyterHub
   - This repo is read-only for diagnostics

---

## Example Finding Entry

When you spot an issue, document it like this:

```markdown
- [ ] Issue: BMI values appear to be in pounds instead of kg
  - **Priority**: High
  - **Variable(s)**: bmi_calculated, weight_kg
  - **Action**: Divide BMI by 2.20462 to convert from lbs to kg
  - **Status**: To Do
  - **Notes**: Affects 45% of records. Values range 150-250 which is
    implausible for BMI but reasonable for weight in lbs.
```

---

## Tracking Your Progress

The `DATA_QUALITY_FINDINGS.md` file maintains:

- ✅ / ⬜ Status for each study
- Count of issues by priority
- Total studies reviewed
- Issues fixed in JupyterHub

Check progress anytime:
```bash
python review_helper.py --status
```

---

## Integration with JupyterHub

**This folder**: Diagnostic/reporting tool
**JupyterHub**: Where actual data cleaning happens

**Workflow**:
1. Review reports here → Document issues
2. Go to JupyterHub → Fix data
3. Re-run report generation → Get updated reports
4. Pull updated reports here → Verify fixes
5. Repeat until clean

---

## Need Help?

- **Not sure what to look for?** → Read `ANOMALY_DETECTION_CHECKLIST.md`
- **Not sure how to proceed?** → Read `REVIEW_WORKFLOW_GUIDE.md`
- **Need to document an issue?** → Use `DATA_QUALITY_FINDINGS.md`
- **Script not working?** → Check troubleshooting in `REVIEW_WORKFLOW_GUIDE.md`

---

## Summary

You now have:
- ✅ Systematic review process
- ✅ Comprehensive checklist of what to look for
- ✅ Structured documentation system
- ✅ Helper tools for navigation
- ✅ Priority classification system

**Ready to start?**

```bash
python review_helper.py --next
```

---

**Created**: 2025-11-24
**System Version**: 1.0
