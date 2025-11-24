# RP2 Data Quality Review - Workflow Guide

**Quick Start Guide for Systematic Data Quality Review**

---

## Overview

This workflow helps you systematically review 17 clinical study quality reports to identify data anomalies that need fixing in JupyterHub.

**Key Principle**: You're using these reports as diagnostic tools. Document issues here, fix them in JupyterHub.

---

## Setup (One Time)

1. **Verify you have all files**:
   ```bash
   ls *.html | wc -l  # Should show 22 HTML files
   ```

2. **Make the helper script executable**:
   ```bash
   chmod +x review_helper.py
   ```

3. **Test the helper script**:
   ```bash
   python review_helper.py --list
   ```

---

## Daily Workflow

### Step 1: Start Your Review Session

Open your tracking document:
```bash
open DATA_QUALITY_FINDINGS.md
```

Check your progress:
```bash
python review_helper.py --status
```

### Step 2: Open Next Study

Get the next unreviewed study:
```bash
python review_helper.py --next
```

This will:
- Show which study is next
- Open the profile HTML in your browser
- Display study directory contents

**OR** open a specific study:
```bash
python review_helper.py --open JHB_ACTG_015
```

### Step 3: Review the Study

Follow the **Anomaly Detection Checklist**:
```bash
open ANOMALY_DETECTION_CHECKLIST.md
```

**Key sections to check in each report**:

1. **Summary Statistics** (top of HTML)
   - Sample size reasonable?
   - Date ranges make sense?
   - Key demographics look normal?

2. **Missing Data Heatmap**
   - Look for systematic patterns
   - Flag variables with >20% missing
   - Note if critical variables have any missing

3. **Distribution Plots**
   - Scan for extreme outliers
   - Check for impossible values
   - Look for suspicious spikes/patterns

4. **Categorical Variables**
   - Check category labels make sense
   - Look for unexpected frequencies
   - Note any numeric codes instead of labels

### Step 4: Document Findings

As you find issues, document them in `DATA_QUALITY_FINDINGS.md`:

**Template for each issue**:
```markdown
- [ ] Issue: [Brief description]
  - **Priority**: High/Medium/Low
  - **Variable(s)**: variable_name
  - **Action**: What needs to be done in JupyterHub
  - **Status**: To Do
  - **Notes**: Any additional context
```

**Example**:
```markdown
- [ ] Issue: Age values include negative numbers
  - **Priority**: High
  - **Variable(s)**: age_years
  - **Action**: Filter out records with age < 0, investigate source
  - **Status**: To Do
  - **Notes**: Found 3 records with age = -999, likely missing data code
```

### Step 5: Mark Study as Reviewed

In `DATA_QUALITY_FINDINGS.md`, update the status table:
```markdown
| JHB_ACTG_015 | ✅ Reviewed | 3 high, 2 medium | 2025-11-24 |
```

And update the study section:
```markdown
### JHB_ACTG_015
**Report**: `JHB_ACTG_015_profile.html`
**Status**: ✅ Reviewed on 2025-11-24

**Issues Found:**
[Your documented issues]
```

### Step 6: Move to Next Study

```bash
python review_helper.py --next
```

Repeat steps 3-5 for each study.

---

## Tips for Efficient Review

### Use Two Monitors (if available)
- **Monitor 1**: HTML report in browser
- **Monitor 2**: `DATA_QUALITY_FINDINGS.md` in text editor

### Review in Batches
- Review 3-5 studies, then batch-fix in JupyterHub
- This is more efficient than switching back and forth

### Start with Quality Reports
Before diving into individual studies:
```bash
python review_helper.py --quality
```

These overview reports may highlight studies with known issues.

### Look for Cross-Study Patterns
If you see the same issue across multiple studies from the same network (e.g., all ACTG studies), note it:
```markdown
## Notes & Observations
- All ACTG studies seem to have BMI in lbs instead of kg
```

---

## Common Keyboard Shortcuts

### macOS
- `Cmd + F` in browser: Search for specific variables
- `Cmd + T` in browser: New tab for multiple studies
- `Cmd + Tab`: Switch between browser and editor

### Review Speed Tips
1. **Scan, don't read everything** - Focus on visualizations first
2. **Trust the heatmaps** - Missing data patterns jump out visually
3. **Use Cmd+F** to find specific variables quickly
4. **Take breaks** - Reviewing data is mentally taxing

---

## Priority Guidelines

### 🔴 HIGH - Stop and Document Immediately
- Impossible values (negative ages, extreme outliers)
- Critical variables >50% missing
- Severe logical inconsistencies
- Anything that would invalidate analysis

### 🟡 MEDIUM - Document Before Moving On
- Questionable outliers that need verification
- Missing data 20-50%
- Suspected unit errors
- Minor inconsistencies

### 🟢 LOW - Quick Note is Fine
- Cosmetic issues (labels, formatting)
- Very minor outliers within plausible range
- Missing data <10% on non-critical variables

---

## Example Review Session (30 minutes)

```bash
# Start session
python review_helper.py --status  # Check progress

# Open next study
python review_helper.py --next    # Opens JHB_ACTG_015

# Review in browser while documenting in DATA_QUALITY_FINDINGS.md
# [15-20 minutes per study when you're in the groove]

# Mark complete and move on
python review_helper.py --next    # Opens JHB_ACTG_016
```

**Target**: 2-4 studies per hour once you're familiar with the checklist

---

## Fixing Issues in JupyterHub

When you're ready to fix issues:

1. **Group by priority**: Fix all high priority issues first
2. **Group by study**: Or fix all issues for one study at a time
3. **Group by issue type**: Or fix all "age" issues across studies

**After fixing in JupyterHub**:
Update `DATA_QUALITY_FINDINGS.md`:
```markdown
- [x] Issue: Age values include negative numbers
  - **Status**: Fixed on 2025-11-25
```

Update summary statistics:
```markdown
**Issues Fixed in JupyterHub**: 5 / 12
```

---

## Completion Checklist

By the end of this review process, you should have:

- [ ] Reviewed all 17 study profiles
- [ ] Documented all anomalies in `DATA_QUALITY_FINDINGS.md`
- [ ] Prioritized issues (High/Medium/Low)
- [ ] Identified cross-study patterns
- [ ] Created action plan for JupyterHub fixes

---

## Helper Commands Quick Reference

```bash
# List all studies
python review_helper.py --list

# Open specific study
python review_helper.py --open JHB_ACTG_015

# Open next unreviewed study
python review_helper.py --next

# Check review progress
python review_helper.py --status

# Open quality overview reports
python review_helper.py --quality

# Open comprehensive reports
python review_helper.py --comprehensive

# Open any report directly in browser
open JHB_ACTG_015_profile.html

# Search for specific term in all reports
grep -r "missing" DATA_QUALITY_FINDINGS.md
```

---

## Troubleshooting

### Python script won't run
```bash
# Make sure you're in the right directory
pwd

# Check Python is available
python --version

# Try with python3
python3 review_helper.py --list
```

### Reports won't open in browser
```bash
# Try opening manually
open JHB_ACTG_015_profile.html

# Or specify full path
open /full/path/to/JHB_ACTG_015_profile.html
```

### Can't find a file
```bash
# List all HTML files
ls -lh *.html

# Search for a specific file
find . -name "*ACTG_015*"
```

---

## Getting Help

- **Checklist**: `ANOMALY_DETECTION_CHECKLIST.md` - Detailed what to look for
- **Findings Doc**: `DATA_QUALITY_FINDINGS.md` - Where to document issues
- **This Guide**: Quick reference for workflow

---

**Ready to start?**

```bash
python review_helper.py --next
```

Good luck with your review! 🔍📊
