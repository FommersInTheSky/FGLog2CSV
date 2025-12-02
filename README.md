# FGLog2CSV
# 🧩 Log Fieldname to CSV Converter

A lightweight, memory-efficient Python tool that converts log-like text files containing key-value pairs into structured CSV files — even for very large input files (hundreds of MB or more).

It has been tested on Fortigate and Fortianalyzer log output files.

---

## 💡 Overview

This script reads log files where each line follows the pattern:
```
"itime=1764342944","date=""2025-11-28""","time=""16:15:44""","devid=""FG100FTK20000000""", ...
```
Each field uses the syntax:
```
fieldname=fieldvalue
```
If the field value is text, it’s surrounded by additional quotes (`""`):
```
date=""2025-11-28""
```

The script:

1. **Detects all unique fieldnames** found across the entire file.
2. **Generates a CSV file** where:
   - Columns = fieldnames
   - Each line = one input record
   - Missing values = empty cells
3. Writes the output **sequentially**, keeping memory usage minimal.

---

## 🚀 Features

- ✅ Handles files of any size (tested > 300 MB)
- ✅ Displays **progress percentage** for both scanning and writing phases
- ✅ UTF‑8 and quote-safe
- ✅ Two-pass sequential algorithm for accuracy and low RAM use
- ✅ Automatically names the output file as `<input_filename>.csv` in the current working directory

---

## 🛠️ Requirements

- **Python 3.8+**
- No third-party libraries required

---

## 📦 Installation

No installation required — just download the script.

## Option 1: Clone the repository
```
bash
git clone https://github.com/yourusername/log-to-csv.git
cd log-to-csv
```

## Option 2: Download the single file
Download parse_log_to_csv.py directly from the repository and place it anywhere on your system.

---

## 🧰 Usage
Run the script from your terminal, passing your input log filename:
```
python parse_log_to_csv.py /path/to/input.txt
```
The CSV is written automatically as: ./input.txt.csv

Example:
```
python parse_log_to_csv.py firewall_logs.txt
```
This creates: firewall_logs.txt.csv

## ⚙️ How It Works
1️⃣ Field Discovery Phase -> scans the file once to find every distinct fieldname.  
2️⃣ CSV Writing Phase -> re‑reads the file and streams each parsed record directly to CSV.

Progress percentage is printed based on bytes processed versus total file size.

## 📈 Performance
- Constant memory footprint (suitable for multi‑GB logs)
- Progress updates every ≈ 5 MB processed
- Gracefully ignores malformed or excess quotes
- No temporary data or intermediate buffers
