HEAT RESEARCH STUDY PROFILES - STATIC SITE DEPLOYMENT GUIDE
============================================================

Contents:
---------
1. COMPREHENSIVE_REPORT_LIGHTWEIGHT.html - Main dashboard (start here!)
2. JHB_*/  - Study directories containing SVG visualizations

Quick Deployment Instructions:
------------------------------

METHOD 1: Simple Local Testing
-------------------------------
1. Extract this zip file to any folder
2. Open COMPREHENSIVE_REPORT_LIGHTWEIGHT.html in a web browser
3. All SVG links should work automatically (they use relative paths)

METHOD 2: Static Site Hosting (GitHub Pages, Netlify, Vercel, etc.)
-------------------------------------------------------------------
1. Extract the zip file
2. Upload all files maintaining the directory structure:
   - COMPREHENSIVE_REPORT_LIGHTWEIGHT.html (in root)
   - JHB_*/ directories (containing SVG files)

GitHub Pages:
   - Create a new repository or use existing one
   - Upload all files to the repo root
   - Enable GitHub Pages in Settings > Pages
   - Access via: https://yourusername.github.io/repo-name/COMPREHENSIVE_REPORT_LIGHTWEIGHT.html

Netlify/Vercel:
   - Drag and drop the extracted folder to their web interface
   - The site will be live immediately
   - Rename the HTML file to index.html for a cleaner URL (optional)

METHOD 3: Custom Domain
----------------------
1. Follow METHOD 2 instructions
2. Configure your custom domain in the hosting platform settings

File Structure (must be maintained):
-----------------------------------
.
├── COMPREHENSIVE_REPORT_LIGHTWEIGHT.html
├── JHB_ACTG_015/
│   ├── JHB_ACTG_015_ALL_distributions.svg
│   ├── JHB_ACTG_015_categorical_ALL_page*.svg
│   └── JHB_ACTG_015_missing_data_ALL.svg
├── JHB_ACTG_016/
│   └── (similar SVG files)
└── (additional study directories...)

Features:
---------
- Fully self-contained static site
- No server-side processing required
- Works with any modern web browser
- Responsive design for mobile and desktop
- Interactive SVG visualizations

Troubleshooting:
---------------
If SVG images don't load:
1. Verify the directory structure is intact
2. Check that files weren't renamed during upload
3. Ensure your hosting service serves .svg files correctly
4. Open browser developer console (F12) to check for errors

Support:
--------
For issues or questions, contact the HEAT Research team.

Generated: 2025-11-18
Dataset: RP2 Clinical Trial Harmonization Study Profiles
