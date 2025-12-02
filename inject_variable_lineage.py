#!/usr/bin/env python3
"""
Inject Data Lineage Into Each Variable Section

This script modifies YData COMBINED_REPORT profiles to add lineage information
directly to each variable's profile section, not as a separate section at the bottom.
"""

import json
import os
import glob
import re
from bs4 import BeautifulSoup

LINEAGE_DIR = ".claude/YDATA_LOCAL_PACKAGE/lineage"
PROFILE_DIR = "."

def load_lineage(study_id):
    """Load lineage information for a study."""
    lineage_file = os.path.join(LINEAGE_DIR, f"{study_id}_harmonization_report_v2.json")

    if os.path.exists(lineage_file):
        with open(lineage_file, 'r') as f:
            return json.load(f)
    return None

def create_variable_lineage_badge(variable_name, lineage_info):
    """Create a compact lineage badge for a variable."""
    if not lineage_info:
        return ""

    # Extract source information
    sources = []
    if isinstance(lineage_info, dict):
        if 'source' in lineage_info:
            sources.append(lineage_info['source'])
        if 'primary_source' in lineage_info:
            sources.append(f"{lineage_info['primary_source']} (primary)")
        if 'secondary_source' in lineage_info:
            sources.append(f"{lineage_info['secondary_source']} (secondary)")

        description = lineage_info.get('description', '')
    else:
        description = str(lineage_info)

    source_text = ", ".join(sources) if sources else "Computed"

    # Create compact HTML badge
    html = f"""
    <div style="margin: 10px 0; padding: 12px; background: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 4px;">
        <p style="margin: 0; font-size: 0.9em;">
            <strong style="color: #1976d2;">📊 Data Source:</strong>
            <code style="background: #fff; padding: 2px 6px; border-radius: 3px; font-size: 0.85em;">{source_text}</code>
        </p>"""

    if description:
        html += f"""
        <p style="margin: 5px 0 0 0; font-size: 0.85em; color: #555;">
            {description}
        </p>"""

    # Add mapping if present
    if isinstance(lineage_info, dict) and 'mapping' in lineage_info:
        mapping = lineage_info['mapping']
        if isinstance(mapping, dict) and len(mapping) > 0:
            html += """
        <details style="margin-top: 8px;">
            <summary style="cursor: pointer; font-size: 0.85em; color: #1976d2;">View value mappings</summary>
            <div style="margin-top: 5px; padding: 8px; background: #fff; border-radius: 3px; font-size: 0.8em;">"""

            # Show first 10 mappings
            for i, (k, v) in enumerate(list(mapping.items())[:10]):
                html += f"""
                <div style="padding: 2px 0;"><code>{k}</code> → <strong>{v}</strong></div>"""

            if len(mapping) > 10:
                html += f"""
                <div style="padding: 4px 0; color: #666; font-style: italic;">...and {len(mapping) - 10} more mappings</div>"""

            html += """
            </div>
        </details>"""

    html += """
    </div>"""

    return html

def inject_lineage_into_profile(profile_path, study_id):
    """Inject lineage information into each variable section."""
    print(f"Processing {study_id}...")

    # Load lineage
    lineage_data = load_lineage(study_id)
    if not lineage_data:
        print(f"  ⚠️  No lineage file found for {study_id}")
        return False

    data_lineage = lineage_data.get('data_lineage', {})
    if not data_lineage:
        print(f"  ⚠️  No variable lineage data found for {study_id}")
        return False

    # Read profile HTML
    with open(profile_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all variable sections
    variable_sections = soup.find_all('div', class_='variable')
    if not variable_sections:
        variable_sections = soup.find_all('div', class_='variable ignore')

    modifications = 0

    # Process each variable section
    for var_section in variable_sections:
        # Find the variable name
        var_header = var_section.find('p', class_='item-header')
        if not var_header:
            continue

        # Extract variable name from the <a> tag or title attribute
        var_link = var_header.find('a')
        if var_link:
            var_name = var_link.get_text().strip()
        else:
            var_name = var_header.get('title', '').strip()

        if not var_name or var_name not in data_lineage:
            continue

        # Create lineage badge
        lineage_html = create_variable_lineage_badge(var_name, data_lineage[var_name])

        # Find the col-sm-12 div that contains the variable header
        col_div = var_header.find_parent('div', class_='col-sm-12')
        if col_div:
            # Insert lineage badge after the variable description
            lineage_soup = BeautifulSoup(lineage_html, 'html.parser')

            # Find the last <p> tag in col_div (usually the description)
            p_tags = col_div.find_all('p', recursive=False)
            if p_tags:
                p_tags[-1].insert_after(lineage_soup)
            else:
                col_div.append(lineage_soup)

            modifications += 1

    if modifications == 0:
        print(f"  ⚠️  No variables modified for {study_id}")
        return False

    # Write updated HTML
    with open(profile_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"  ✓ Added lineage to {modifications} variables in {study_id}")
    return True

def main():
    """Main execution."""
    print("="*70)
    print("INJECTING VARIABLE LINEAGE INTO YDATA PROFILES")
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

        if inject_lineage_into_profile(profile_path, study_id):
            updated += 1

    print("\n" + "="*70)
    print(f"SUMMARY: Updated {updated} out of {len(profile_files)} profiles")
    print("="*70)

if __name__ == "__main__":
    main()
