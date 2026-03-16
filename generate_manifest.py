#!/usr/bin/env python3
"""
generate_manifest.py
====================
Run this script once (or whenever you add/remove CSV files) to regenerate
subjects/manifest.json, which tells Flashcard Pro which files to load.

Usage:
    python generate_manifest.py

Place this file next to flashcard-pro.html and the subjects/ folder.
"""

import os
import json

SUBJECTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subjects")

def build_manifest():
    manifest = {}
    if not os.path.isdir(SUBJECTS_DIR):
        print(f"[!] subjects/ folder not found at: {SUBJECTS_DIR}")
        print("    Create it and add subject sub-folders with .csv files.")
        return

    for entry in sorted(os.listdir(SUBJECTS_DIR)):
        subject_path = os.path.join(SUBJECTS_DIR, entry)
        if not os.path.isdir(subject_path):
            continue
        csv_files = sorted(
            f for f in os.listdir(subject_path)
            if f.lower().endswith(".csv")
        )
        if csv_files:
            manifest[entry] = csv_files
            print(f"  ✓  {entry}  ({len(csv_files)} file{'s' if len(csv_files)!=1 else ''})")

    out_path = os.path.join(SUBJECTS_DIR, "manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total_subjects = len(manifest)
    total_files    = sum(len(v) for v in manifest.values())
    print(f"\n✅  manifest.json written  →  {total_subjects} subject(s), {total_files} file(s)")
    print(f"   {out_path}")

if __name__ == "__main__":
    print("Scanning subjects/ folder...\n")
    build_manifest()
    print("\nNow serve with:  python -m http.server 8080")
    print("Then open:       http://localhost:8080/flashcard-pro.html")