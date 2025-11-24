#!/usr/bin/env python3
"""
RP2 Data Quality Review Helper Script

This script helps you systematically review quality reports and identify anomalies.
It can open reports, navigate through studies, and help track your progress.

Usage:
    python review_helper.py --list                  # List all studies
    python review_helper.py --open JHB_ACTG_015     # Open study profile in browser
    python review_helper.py --next                  # Open next unreviewed study
    python review_helper.py --status                # Show review status
    python review_helper.py --quality               # Open quality reports
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import re

# Study list in order
STUDIES = [
    "JHB_ACTG_015",
    "JHB_ACTG_016",
    "JHB_ACTG_017",
    "JHB_ACTG_018",
    "JHB_ACTG_019",
    "JHB_ACTG_021",
    "JHB_Aurum_009",
    "JHB_DPHRU_013",
    "JHB_DPHRU_053",
    "JHB_EZIN_002",
    "JHB_EZIN_025",
    "JHB_JHSPH_005",
    "JHB_SCHARP_004",
    "JHB_SCHARP_006",
    "JHB_VIDA_007",
    "JHB_VIDA_008",
    "JHB_WRHI_001",
    "JHB_WRHI_003"
]

def open_in_browser(filepath):
    """Open HTML file in default browser"""
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", filepath])
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", filepath])
    elif sys.platform == "win32":
        subprocess.run(["start", filepath], shell=True)
    else:
        print(f"Please open manually: {filepath}")

def get_profile_path(study_name):
    """Get the path to a study's profile HTML"""
    # Handle the special case for Ezin_002
    if study_name == "JHB_EZIN_002":
        filename = f"JHB_Ezin_002_profile.html"
    else:
        filename = f"{study_name}_profile.html"
    return Path(filename)

def list_studies():
    """List all studies with their file sizes"""
    print("\n📊 RP2 Clinical Studies")
    print("=" * 70)
    print(f"{'Study':<20} {'Profile Size':<15} {'Directory':<10}")
    print("-" * 70)

    for study in STUDIES:
        profile = get_profile_path(study)
        if profile.exists():
            size_mb = profile.stat().st_size / (1024 * 1024)
            dir_exists = "✓" if Path(study).exists() else "✗"
            print(f"{study:<20} {size_mb:>10.1f} MB    {dir_exists:^10}")
        else:
            print(f"{study:<20} {'NOT FOUND':<15} {'?':^10}")

    print("-" * 70)
    print(f"Total studies: {len(STUDIES)}\n")

def open_study(study_name):
    """Open a study's profile report"""
    if study_name not in STUDIES:
        print(f"❌ Error: '{study_name}' is not a valid study name")
        print(f"Available studies: {', '.join(STUDIES)}")
        return

    profile = get_profile_path(study_name)
    if not profile.exists():
        print(f"❌ Error: Profile file not found: {profile}")
        return

    print(f"📂 Opening {study_name} profile report...")
    print(f"   File: {profile} ({profile.stat().st_size / (1024*1024):.1f} MB)")
    open_in_browser(str(profile))

    # Also show what's in the study directory
    study_dir = Path(study_name)
    if study_dir.exists():
        files = list(study_dir.glob("*"))
        print(f"\n   Study directory contains {len(files)} files:")
        for f in sorted(files)[:5]:  # Show first 5
            print(f"     - {f.name}")
        if len(files) > 5:
            print(f"     ... and {len(files) - 5} more")

def get_review_status():
    """Parse DATA_QUALITY_FINDINGS.md to get review status"""
    findings_file = Path("DATA_QUALITY_FINDINGS.md")
    if not findings_file.exists():
        return {}

    content = findings_file.read_text()
    reviewed = {}

    # Look for status markers in the review status table
    for study in STUDIES:
        # Simple check - look for study name followed by completion marker
        if f"| {study} | ✅" in content or f"| {study} | ✓" in content:
            reviewed[study] = True
        else:
            reviewed[study] = False

    return reviewed

def show_status():
    """Show review progress"""
    status = get_review_status()
    reviewed_count = sum(status.values())

    print("\n📋 Review Progress")
    print("=" * 70)
    print(f"Studies reviewed: {reviewed_count}/{len(STUDIES)} ({reviewed_count/len(STUDIES)*100:.0f}%)")
    print("-" * 70)

    print("\n✅ Reviewed:")
    for study, is_reviewed in status.items():
        if is_reviewed:
            print(f"  - {study}")

    print("\n⬜ Not Reviewed:")
    for study, is_reviewed in status.items():
        if not is_reviewed:
            print(f"  - {study}")
    print()

def open_next_unreviewed():
    """Open the next unreviewed study"""
    status = get_review_status()

    for study in STUDIES:
        if not status.get(study, False):
            print(f"📌 Next unreviewed study: {study}")
            open_study(study)
            return

    print("🎉 All studies have been reviewed!")

def open_quality_reports():
    """Open the main quality/status reports"""
    reports = [
        "DATASET_STATUS_RESEARCH_REPORT.html",
        "ENHANCED_DATASET_STATUS_REPORT.html"
    ]

    print("\n📊 Opening quality reports...")
    for report in reports:
        if Path(report).exists():
            print(f"   - {report}")
            open_in_browser(report)
        else:
            print(f"   ⚠️  Not found: {report}")

def open_comprehensive():
    """Open comprehensive reports"""
    reports = [
        "ULTRA_COMPREHENSIVE_REPORT.html",
        "COMPREHENSIVE_REPORT_LIGHTWEIGHT.html"
    ]

    print("\n📚 Opening comprehensive reports...")
    for report in reports:
        path = Path(report)
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"   - {report} ({size_mb:.1f} MB)")
            open_in_browser(report)
        else:
            print(f"   ⚠️  Not found: {report}")

def main():
    parser = argparse.ArgumentParser(
        description="RP2 Data Quality Review Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python review_helper.py --list
  python review_helper.py --open JHB_ACTG_015
  python review_helper.py --next
  python review_helper.py --status
  python review_helper.py --quality
        """
    )

    parser.add_argument("--list", action="store_true",
                       help="List all studies")
    parser.add_argument("--open", metavar="STUDY",
                       help="Open a specific study profile")
    parser.add_argument("--next", action="store_true",
                       help="Open next unreviewed study")
    parser.add_argument("--status", action="store_true",
                       help="Show review progress")
    parser.add_argument("--quality", action="store_true",
                       help="Open quality/status reports")
    parser.add_argument("--comprehensive", action="store_true",
                       help="Open comprehensive reports")

    args = parser.parse_args()

    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n💡 Quick start: Try 'python review_helper.py --next' to begin review")
        return

    if args.list:
        list_studies()

    if args.open:
        open_study(args.open)

    if args.next:
        open_next_unreviewed()

    if args.status:
        show_status()

    if args.quality:
        open_quality_reports()

    if args.comprehensive:
        open_comprehensive()

if __name__ == "__main__":
    main()
