#!/usr/bin/env python3
"""
Add Data Lineage to Existing YData Profiles

This script reads the existing YData COMBINED_REPORT profiles and adds
comprehensive data lineage information to each one.
"""

import json
import os
import glob

# Paths
LINEAGE_DIR = ".claude/YDATA_LOCAL_PACKAGE/lineage"
PROFILE_DIR = "."

def load_lineage(study_id):
    """Load lineage information for a study."""
    lineage_file = os.path.join(LINEAGE_DIR, f"{study_id}_harmonization_report_v2.json")

    if os.path.exists(lineage_file):
        with open(lineage_file, 'r') as f:
            return json.load(f)
    return None

def create_lineage_html(lineage_data, study_id):
    """Create comprehensive HTML section for data lineage."""
    if not lineage_data:
        return ""

    html = """
    <div class="lineage-section" style="margin: 40px 20px; padding: 30px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff;">
        <h2 style="color: #1a237e; margin-bottom: 20px; font-family: 'Segoe UI', sans-serif;">📋 Data Lineage & Traceability</h2>
        <p style="margin-bottom: 20px; line-height: 1.6;">
            This section provides complete traceability for all variables in this dataset, showing source files,
            transformations, and methodologies used in data harmonization.
        </p>
    """

    # Study Information
    if 'study_id' in lineage_data:
        html += f"""
        <div style="background: white; padding: 20px; border-radius: 4px; margin-bottom: 20px;">
            <h3 style="color: #007bff; margin-bottom: 15px;">Study Information</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 8px; font-weight: 600; width: 200px;">Study ID:</td><td style="padding: 8px;">{lineage_data.get('study_id', 'N/A')}</td></tr>
                <tr><td style="padding: 8px; font-weight: 600;">Version:</td><td style="padding: 8px;">{lineage_data.get('version', 'N/A')}</td></tr>
                <tr><td style="padding: 8px; font-weight: 600;">Harmonization Date:</td><td style="padding: 8px;">{lineage_data.get('harmonization_date', 'N/A')}</td></tr>
                <tr><td style="padding: 8px; font-weight: 600;">Source Path:</td><td style="padding: 8px;"><code>{lineage_data.get('source_path', 'N/A')}</code></td></tr>
            </table>
        </div>
        """

    # Source Files Used
    if 'source_files_used' in lineage_data:
        html += """
        <div style="background: white; padding: 20px; border-radius: 4px; margin-bottom: 20px;">
            <h3 style="color: #007bff; margin-bottom: 15px;">Source Files Used</h3>
            <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background: #007bff; color: white;">
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">File ID</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Description</th>
                        <th style="padding: 12px; text-align: right; border: 1px solid #ddd;">Records</th>
                    </tr>
                </thead>
                <tbody>
        """

        for file_id, info in lineage_data['source_files_used'].items():
            records = info.get('records', 'N/A')
            description = info.get('description', 'N/A')
            html += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;"><code>{file_id}</code></td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{description}</td>
                        <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{records:,}</td>
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
        <div style="background: white; padding: 20px; border-radius: 4px; margin-bottom: 20px;">
            <h3 style="color: #007bff; margin-bottom: 15px;">Variable Lineage & Source Mappings</h3>
            <p style="margin-bottom: 15px; color: #666;">
                This table shows the exact source of each harmonized variable, enabling complete traceability.
            </p>
            <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
                <thead>
                    <tr style="background: #007bff; color: white;">
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Variable Name</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Source</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Description / Mapping</th>
                    </tr>
                </thead>
                <tbody>
        """

        for variable, info in lineage_data['data_lineage'].items():
            # Handle different lineage structures
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
                    for k, v in list(info['mapping'].items())[:5]:  # Show first 5 mappings
                        description += f"• {k} → {v}<br>"
                    if len(info['mapping']) > 5:
                        description += f"<em>...and {len(info['mapping']) - 5} more</em>"

                html += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd; font-weight: 600;">{variable}</td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{source_text}</td>
                        <td style="padding: 10px; border: 1px solid #ddd;">{description}</td>
                    </tr>
                """
            else:
                html += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd; font-weight: 600;">{variable}</td>
                        <td style="padding: 10px; border: 1px solid #ddd;" colspan="2">{str(info)}</td>
                    </tr>
                """

        html += """
                </tbody>
            </table>
        </div>
        """

    # Output Summary
    if 'output_summary' in lineage_data:
        summary = lineage_data['output_summary']
        html += f"""
        <div style="background: white; padding: 20px; border-radius: 4px;">
            <h3 style="color: #007bff; margin-bottom: 15px;">Output Dataset Summary</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 8px; font-weight: 600; width: 200px;">Total Records:</td><td style="padding: 8px;">{summary.get('total_records', 'N/A'):,}</td></tr>
                <tr><td style="padding: 8px; font-weight: 600;">Unique Patients:</td><td style="padding: 8px;">{summary.get('unique_patients', 'N/A'):,}</td></tr>
                <tr><td style="padding: 8px; font-weight: 600;">Records per Patient:</td><td style="padding: 8px;">{summary.get('records_per_patient', 'N/A')}</td></tr>
            </table>
        </div>
        """

    html += """
    </div>
    """

    return html

def add_lineage_to_profile(profile_path, study_id):
    """Add lineage information to an existing profile."""
    print(f"Processing {study_id}...")

    # Load lineage
    lineage = load_lineage(study_id)
    if not lineage:
        print(f"  ⚠️  No lineage file found for {study_id}")
        return False

    # Read profile
    with open(profile_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Check if lineage already exists
    if 'lineage-section' in html_content:
        print(f"  ✓ Lineage already exists in {study_id}")
        return False

    # Create lineage HTML
    lineage_html = create_lineage_html(lineage, study_id)

    # Append lineage section at end of file (YData profiles don't have </body> tags)
    # Add proper HTML closing tags if missing
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{lineage_html}</body>')
    else:
        # Append lineage and add closing tags
        html_content = html_content.rstrip() + '\n' + lineage_html + '</body>\n</html>\n'

    # Write updated profile
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  ✓ Added lineage to {study_id}")
    return True

def main():
    """Main execution."""
    print("="*70)
    print("ADDING DATA LINEAGE TO YDATA PROFILES")
    print("="*70)

    # Find all COMBINED_REPORT files
    profile_files = glob.glob("JHB_*_COMBINED_REPORT.html")

    if not profile_files:
        print("❌ No COMBINED_REPORT files found!")
        return

    print(f"\nFound {len(profile_files)} profile files\n")

    updated = 0
    for profile_path in sorted(profile_files):
        # Extract study ID from filename
        study_id = profile_path.replace('_COMBINED_REPORT.html', '')

        if add_lineage_to_profile(profile_path, study_id):
            updated += 1

    print("\n" + "="*70)
    print(f"SUMMARY: Updated {updated} out of {len(profile_files)} profiles")
    print("="*70)

if __name__ == "__main__":
    main()
