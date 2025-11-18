# RP2 Clinical Dataset - Comprehensive Analysis & Documentation

This repository contains comprehensive statistical analysis, visualizations, and documentation for the RP2 clinical dataset from 17 studies conducted in Johannesburg, South Africa.

## Live Site

**Visit: https://logic06183.github.io/RP2_dataoverview/**

## Overview

The RP2 (HEAT Research Projects) documentation includes de-identified aggregate data from 17 clinical trials focusing on HIV/AIDS research, metabolic studies, vaccine trials, and related health outcomes in South African populations.

### What's Included

- **4 Comprehensive HTML Reports** with interactive visualizations
- **17 Individual Study Profile Pages** with detailed statistics
- **150+ SVG Visualizations** including distributions, categorical analyses, and missing data heatmaps
- **Markdown Documentation** with methodology, variable definitions, and usage guides
- **De-identified Aggregate Data** safe for public sharing and academic use

## Site Structure

### Main Navigation Hub
- **index.html** - Landing page with links to all documentation

### Comprehensive Reports
- **main_report.html** - Main analysis dashboard with summary statistics for all 17 studies
- **ULTRA_COMPREHENSIVE_REPORT.html** - Complete in-depth analysis (16MB)
- **DATASET_STATUS_RESEARCH_REPORT.html** - Data quality overview and completeness metrics
- **ENHANCED_DATASET_STATUS_REPORT.html** - Concise status report

### Individual Study Profiles

Each study has a dedicated HTML profile page with:
- Complete demographics and participant statistics
- Biomarker distributions and key findings
- Categorical variable analysis
- Missing data visualizations
- Study-specific methodology

#### ACTG Studies (6)
- JHB_ACTG_015, 016, 017, 018, 019, 021

#### Other Research Networks (11)
- JHB_Aurum_009 (Aurum Institute)
- JHB_DPHRU_013, 053 (Developmental Pathways for Health Research Unit)
- JHB_EZIN_002, 025 (EZIN Research)
- JHB_JHSPH_005 (Johns Hopkins School of Public Health)
- JHB_SCHARP_004, 006 (Statistical Center for HIV/AIDS Research and Prevention)
- JHB_VIDA_007, 008 (VIDA Research)
- JHB_WRHI_001, 003 (Wits Reproductive Health and HIV Institute)

### Visualizations

Each study directory contains SVG files:
- `*_ALL_distributions.svg` - Distribution plots for continuous variables
- `*_biomarker_distributions.svg` - Top biomarker histograms
- `*_categorical_ALL_*.svg` - Categorical variable frequencies (paginated)
- `*_missing_data.svg` - Missing data heatmaps
- `*_summary.svg` - Quick reference cards

### Documentation Files

- **README.md** - This file
- **USAGE_GUIDE.md** - How to navigate the documentation
- **MASTER_VARIABLE_SUMMARY.md** - Complete variable definitions
- **COMPREHENSIVE_PROFILES_README.md** - Study profiles guide
- **PRIVACY_README.txt** - Privacy protection notice

## Privacy & Data Protection

All data in this repository is:
- **De-identified**: No personally identifiable information (PII)
- **Aggregated**: Statistical summaries only, no individual records
- **Safe for public sharing**: Suitable for GitHub, academic presentations, publications
- **IRB compliant**: Follows minimum cell size requirements (>5 participants)

## Usage

### View Locally
```bash
# Clone the repository
git clone https://github.com/Logic06183/RP2_dataoverview.git
cd RP2_dataoverview

# Open in browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

### Explore Studies
1. Start at `index.html` - the main navigation hub
2. Browse comprehensive reports for overview statistics
3. Click individual study profiles for detailed analysis
4. Review markdown documentation for methodology

## Citation

When using this data in publications, please cite:

```
HEAT Research Projects. (2025). RP2 Clinical Trial Data Harmonization
Study Profiles: Johannesburg, South Africa. Aggregate Statistics and
Visualizations. https://logic06183.github.io/RP2_dataoverview/
```

## Technology Stack

- **HTML5** - Interactive reports
- **SVG** - Scalable vector graphics for visualizations
- **Markdown** - Documentation
- **GitHub Pages** - Static site hosting

## Repository Statistics

- **Total Files**: 193 files
- **Total Studies**: 17 clinical trials
- **Total Visualizations**: 150+ SVG files
- **Documentation**: 7 markdown guides
- **HTML Reports**: 22 files

## Research Networks

- **ACTG** - AIDS Clinical Trials Group
- **Aurum** - Aurum Institute
- **DPHRU** - Developmental Pathways for Health Research Unit
- **EZIN** - EZIN Research Network
- **JHSPH** - Johns Hopkins School of Public Health
- **SCHARP** - Statistical Center for HIV/AIDS Research and Prevention
- **VIDA** - VIDA Research
- **WRHI** - Wits Reproductive Health and HIV Institute

## Contact & Support

For questions about this documentation package:
- Review the USAGE_GUIDE.md and individual study COMPREHENSIVE_REPORT.md files
- Check the MASTER_VARIABLE_SUMMARY.md for variable definitions
- Visit the GitHub repository: https://github.com/Logic06183/RP2_dataoverview

## License

This documentation contains de-identified aggregate research data suitable for public sharing. Individual-level data requests require IRB approval and data sharing agreements.

---

**HEAT Research Projects** - Climate Health Analysis in African Populations
Generated: November 2025 | Package Version: 1.0
