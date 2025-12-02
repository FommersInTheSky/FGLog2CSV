#!/usr/bin/env python3
import csv
import re
import os
import sys
from pathlib import Path

# Regex pattern to match key=value with optional double quotes
FIELD_PATTERN = re.compile(r'"?([\w-]+)=(?:""?([^",]*)""?)"?')

def parse_line(line: str) -> dict:
    """Extract all key=value fields from a log line into a dictionary."""
    return {key: val.strip('"') for key, val in FIELD_PATTERN.findall(line)}

def show_progress(bytes_read: int, total_bytes: int, phase: str):
    """Print progress as percentage based on bytes read."""
    percent = (bytes_read / total_bytes) * 100 if total_bytes > 0 else 0
    print(f"\r{phase}: {percent:6.2f}%", end='', flush=True)

def extract_all_fieldnames(filepath: Path) -> list[str]:
    """First pass: collect all unique fieldnames (streaming)."""
    total_bytes = os.path.getsize(filepath)
    bytes_read = 0
    fieldnames = set()

    with filepath.open('r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            bytes_read += len(line.encode('utf-8'))
            if not line.strip():
                continue
            parsed = parse_line(line)
            fieldnames.update(parsed.keys())
            if bytes_read % (5 * 1024 * 1024) < 200:  # update every ~5 MB
                show_progress(bytes_read, total_bytes, "Scanning fields")
    show_progress(total_bytes, total_bytes, "Scanning fields")
    print()
    return sorted(fieldnames)

def write_csv(filepath: Path, fieldnames: list[str], output_path: Path):
    """Second pass: write output line-by-line to CSV."""
    total_bytes = os.path.getsize(filepath)
    bytes_read = 0

    with open(output_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        with filepath.open('r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                bytes_read += len(line.encode('utf-8'))
                if not line.strip():
                    continue
                writer.writerow(parse_line(line))
                if bytes_read % (5 * 1024 * 1024) < 200:
                    show_progress(bytes_read, total_bytes, "Writing CSV")
    show_progress(total_bytes, total_bytes, "Writing CSV")
    print()

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_log_to_csv.py <input_filename>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"❌ Error: file not found → {input_path}")
        sys.exit(1)

    output_path = Path.cwd() / (input_path.name + ".csv")
    print(f"Input : {input_path}")
    print(f"Output: {output_path}")

    # Step 1. Identify all fieldnames
    print("\nAnalyzing fields...")
    all_fields = extract_all_fieldnames(input_path)
    print(f"Found {len(all_fields)} unique fields.")

    # Step 2. Write CSV
    print("\nConverting to CSV...")
    write_csv(input_path, all_fields, output_path)

    print(f"\n✅ Done! Output written to '{output_path}'")

if __name__ == "__main__":
    main()
