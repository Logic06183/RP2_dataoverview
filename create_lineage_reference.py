#!/usr/bin/env python3
"""
Create Comprehensive Data Lineage Reference Document

This script generates a single comprehensive HTML document containing
all data lineage information for all 13 studies in the RP2 dataset.
"""

import json
import os
import glob
from datetime import datetime

LINEAGE_DIR = ".claude/YDATA_LOCAL_PACKAGE/lineage"
OUTPUT_FILE = "DATA_LINEAGE_REFERENCE.html"

def load_all_lineage():
    """Load all lineage JSON files."""
    lineage_files = glob.glob(os.path.join(LINEAGE_DIR, "*_harmonization_report_v2.json"))

    all_lineage = {}
    for filepath in sorted(lineage_files):
        study_id = os.path.basename(filepath).replace('_harmonization_report_v2.json', '')
        with open(filepath, 'r') as f:
            all_lineage[study_id] = json.load(f)

    return all_lineage

def create_html_header():
    """Create HTML header with styling."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RP2 Data Lineage Reference - Complete Traceability Documentation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .meta-info {
            background: #f8f9fa;
            padding: 20px 40px;
            border-bottom: 3px solid #007bff;
        }

        .meta-info p {
            margin: 5px 0;
            font-size: 0.95em;
        }

        .toc {
            background: #fff;
            padding: 30px 40px;
            border-bottom: 1px solid #e0e0e0;
        }

        .toc h2 {
            color: #1a237e;
            margin-bottom: 20px;
            font-size: 1.8em;
        }

        .toc ul {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 10px;
        }

        .toc a {
            display: block;
            padding: 12px 20px;
            background: #f8f9fa;
            color: #007bff;
            text-decoration: none;
            border-radius: 6px;
            border-left: 4px solid #007bff;
            transition: all 0.3s ease;
        }

        .toc a:hover {
            background: #007bff;
            color: white;
            transform: translateX(5px);
        }

        .content {
            padding: 40px;
        }

        .study-section {
            margin-bottom: 60px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 5px solid #007bff;
        }

        .study-section h2 {
            color: #1a237e;
            margin-bottom: 20px;
            font-size: 2em;
            padding-bottom: 10px;
            border-bottom: 2px solid #007bff;
        }

        .info-card {
            background: white;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .info-card h3 {
            color: #007bff;
            margin-bottom: 15px;
            font-size: 1.3em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            background: white;
        }

        th {
            background: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0056b3;
        }

        td {
            padding: 10px 12px;
            border: 1px solid #ddd;
        }

        tr:nth-child(even) {
            background: #f8f9fa;
        }

        tr:hover {
            background: #e3f2fd;
        }

        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #d63384;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .stat-box {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #28a745;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .stat-box strong {
            display: block;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .stat-box span {
            display: block;
            font-size: 1.5em;
            color: #28a745;
            font-weight: 700;
        }

        .footer {
            background: #1a237e;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }

        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #007bff;
            color: white;
            padding: 12px 20px;
            border-radius: 50px;
            text-decoration: none;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }

        .back-to-top:hover {
            background: #0056b3;
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 RP2 Data Lineage Reference</h1>
            <p>Complete Traceability Documentation for All Studies</p>
        </div>

        <div class="meta-info">
            <p><strong>Generated:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p><strong>Purpose:</strong> Comprehensive data lineage and traceability documentation for ALCOA+ compliance</p>
            <p><strong>Coverage:</strong> 13 Studies | 73,125 Records | 12,804 Unique Patients</p>
        </div>
"""

def create_toc(all_lineage):
    """Create table of contents."""
    html = """
        <div class="toc">
            <h2>📑 Table of Contents</h2>
            <ul>
"""

    for study_id in sorted(all_lineage.keys()):
        html += f'                <li><a href="#{study_id}">{study_id}</a></li>\n'

    html += """
            </ul>
        </div>
"""

    return html

def create_study_section(study_id, lineage_data):
    """Create detailed section for a single study."""
    html = f"""
        <div id="{study_id}" class="study-section">
            <h2>{study_id}</h2>
"""

    # Study Info (handle both old and new structures)
    if 'study_info' in lineage_data:
        info = lineage_data['study_info']
        html += f"""
            <div class="info-card">
                <h3>Study Information</h3>
                <table>
                    <tr><td style="width: 250px; font-weight: 600;">Study Name:</td><td>{info.get('study_name', 'N/A')}</td></tr>
                    <tr><td style="font-weight: 600;">Study Type:</td><td>{info.get('study_type', 'N/A')}</td></tr>
                    <tr><td style="font-weight: 600;">Location:</td><td>{info.get('city', 'N/A')}, {info.get('country', 'N/A')}</td></tr>
                    <tr><td style="font-weight: 600;">Duration:</td><td>{info.get('duration_weeks', 'N/A')} weeks</td></tr>
                    <tr><td style="font-weight: 600;">Data Format:</td><td>{info.get('data_format', 'N/A')}</td></tr>
                </table>
            </div>
"""
    else:
        html += f"""
            <div class="info-card">
                <h3>Study Information</h3>
                <table>
                    <tr><td style="width: 250px; font-weight: 600;">Study ID:</td><td>{lineage_data.get('study_id', study_id)}</td></tr>
                    <tr><td style="font-weight: 600;">Version:</td><td>{lineage_data.get('version', 'N/A')}</td></tr>
                    <tr><td style="font-weight: 600;">Harmonization Date:</td><td>{lineage_data.get('harmonization_date', 'N/A')}</td></tr>
                    <tr><td style="font-weight: 600;">Source Path:</td><td><code>{lineage_data.get('source_path', 'N/A')}</code></td></tr>
                </table>
            </div>
"""

    # Dataset Summary
    if 'output_summary' in lineage_data:
        summary = lineage_data['output_summary']
        html += """
            <div class="info-card">
                <h3>Dataset Summary</h3>
                <div class="stat-grid">
"""
        html += f"""
                    <div class="stat-box">
                        <strong>Total Records</strong>
                        <span>{summary.get('total_records', 'N/A'):,}</span>
                    </div>
                    <div class="stat-box">
                        <strong>Unique Patients</strong>
                        <span>{summary.get('unique_patients', 'N/A'):,}</span>
                    </div>
                    <div class="stat-box">
                        <strong>Records per Patient</strong>
                        <span>{summary.get('records_per_patient', 'N/A')}</span>
                    </div>
"""
        html += """
                </div>
            </div>
"""
    elif 'dataset_summary' in lineage_data:
        summary = lineage_data['dataset_summary']
        html += """
            <div class="info-card">
                <h3>Dataset Summary</h3>
                <div class="stat-grid">
"""
        html += f"""
                    <div class="stat-box">
                        <strong>Total Records</strong>
                        <span>{summary.get('total_records', 'N/A'):,}</span>
                    </div>
                    <div class="stat-box">
                        <strong>Unique Patients</strong>
                        <span>{summary.get('unique_patients', 'N/A'):,}</span>
                    </div>
                    <div class="stat-box">
                        <strong>Records per Patient</strong>
                        <span>{summary.get('records_per_patient_mean', 'N/A')}</span>
                    </div>
                    <div class="stat-box">
                        <strong>Columns</strong>
                        <span>{summary.get('columns', 'N/A')}</span>
                    </div>
"""
        html += """
                </div>
            </div>
"""

    # Source Files
    if 'source_files_used' in lineage_data:
        html += """
            <div class="info-card">
                <h3>Source Files Used</h3>
                <table>
                    <thead>
                        <tr>
                            <th>File ID</th>
                            <th>Description</th>
                            <th style="text-align: right;">Records</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for file_id, info in lineage_data['source_files_used'].items():
            html += f"""
                        <tr>
                            <td><code>{file_id}</code></td>
                            <td>{info.get('description', 'N/A')}</td>
                            <td style="text-align: right;">{info.get('records', 'N/A'):,}</td>
                        </tr>
"""
        html += """
                    </tbody>
                </table>
            </div>
"""

    # Variable Lineage
    if 'data_lineage' in lineage_data:
        html += """
            <div class="info-card">
                <h3>Variable Lineage & Source Mappings</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Variable Name</th>
                            <th>Source</th>
                            <th>Description / Mapping</th>
                        </tr>
                    </thead>
                    <tbody>
"""

        for variable, info in lineage_data['data_lineage'].items():
            if isinstance(info, dict):
                sources = []
                if 'source' in info:
                    sources.append(f"<code>{info['source']}</code>")
                if 'primary_source' in info:
                    sources.append(f"<code>{info['primary_source']}</code> (primary)")
                if 'secondary_source' in info:
                    sources.append(f"<code>{info['secondary_source']}</code> (secondary)")

                source_text = "<br>".join(sources) if sources else "Multiple sources"

                description = info.get('description', '')
                if 'mapping' in info and isinstance(info['mapping'], dict):
                    description += "<br><strong>Mappings:</strong><br>"
                    for k, v in list(info['mapping'].items())[:10]:
                        description += f"• {k} → {v}<br>"
                    if len(info['mapping']) > 10:
                        description += f"<em>...and {len(info['mapping']) - 10} more</em>"

                html += f"""
                        <tr>
                            <td style="font-weight: 600;">{variable}</td>
                            <td>{source_text}</td>
                            <td>{description}</td>
                        </tr>
"""
            else:
                html += f"""
                        <tr>
                            <td style="font-weight: 600;">{variable}</td>
                            <td colspan="2">{str(info)}</td>
                        </tr>
"""

        html += """
                    </tbody>
                </table>
            </div>
"""

    # Biomarker Coverage
    if 'biomarker_coverage' in lineage_data:
        html += """
            <div class="info-card">
                <h3>Biomarker Coverage</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Biomarker</th>
                            <th style="text-align: right;">Total Measurements</th>
                            <th style="text-align: right;">Unique Patients</th>
                            <th style="text-align: right;">Measurements per Patient</th>
                        </tr>
                    </thead>
                    <tbody>
"""

        for biomarker, info in lineage_data['biomarker_coverage'].items():
            if isinstance(info, dict):
                html += f"""
                        <tr>
                            <td style="font-weight: 600;">{biomarker}</td>
                            <td style="text-align: right;">{info.get('total_measurements', info):,}</td>
                            <td style="text-align: right;">{info.get('unique_patients', 'N/A'):,}</td>
                            <td style="text-align: right;">{info.get('measurements_per_patient', 'N/A')}</td>
                        </tr>
"""
            else:
                html += f"""
                        <tr>
                            <td style="font-weight: 600;">{biomarker}</td>
                            <td style="text-align: right;" colspan="3">{info:,}</td>
                        </tr>
"""

        html += """
                    </tbody>
                </table>
            </div>
"""

    html += """
        </div>
"""

    return html

def create_html_footer():
    """Create HTML footer."""
    return """
        <div class="footer">
            <p><strong>RP2 Data Overview Project</strong></p>
            <p>ALCOA+ Compliant Data Lineage Documentation</p>
            <p>Generated automatically from harmonization metadata</p>
        </div>
    </div>

    <a href="#" class="back-to-top">↑ Back to Top</a>
</body>
</html>
"""

def main():
    """Main execution."""
    print("="*70)
    print("CREATING COMPREHENSIVE DATA LINEAGE REFERENCE")
    print("="*70)

    # Load all lineage data
    print("\nLoading lineage data...")
    all_lineage = load_all_lineage()
    print(f"✓ Loaded {len(all_lineage)} studies")

    # Build HTML document
    print("\nBuilding HTML document...")
    html = create_html_header()
    html += create_toc(all_lineage)
    html += '<div class="content">\n'

    for study_id, lineage_data in sorted(all_lineage.items()):
        print(f"  • Processing {study_id}")
        html += create_study_section(study_id, lineage_data)

    html += '</div>\n'
    html += create_html_footer()

    # Write output
    print(f"\nWriting {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Created {OUTPUT_FILE}")
    print(f"  File size: {len(html):,} bytes")
    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
