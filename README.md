# Juoksuloki – Export Suunto Run Data to Excel

A simple Python tool for exporting run data from the **Suunto app** (iOS) into a local Excel file for further analysis.

The script automatically:

- Moves exported `.json` files from your **Downloads** folder into a structured directory.
- Parses key metrics from each run (distance, duration, VO₂max, HR zones, etc.).
- Appends new runs to an Excel log (`juoksuloki.xlsx`), sorted by date.

---

## Requirements

- macOS (tested on macOS with iPhone + Suunto app)
- Python 3.9+
- Libraries:
  - `pandas`
  - `openpyxl`

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Setup

1. Export your Suunto run(s) from the Suunto app on iPhone:

   - Open a workout → Export as **JSON**.
   - Airdrop the file(s) to your Mac → they will appear in `~/Downloads`.

2. Run the script:

   ```bash
   python run.py
   ```

3. The script will:
   - Move JSON files from `~/Downloads` to `~/juoksut/json_juoksut/`.
   - Extract run data and add it into `~/juoksut/juoksuloki.xlsx`.

---

## Output

The generated Excel file contains one row per run with the following fields:

- Päivämäärä
- Kesto (s)
- Matka (m)
- EPOC
- PTE
- VO₂max
- Fiilis (1–5)
- HR Zone 1–5 (s)
- Calories
- FitnessAge / FitnessAgeClass
- LeftGCT (%) / RightGCT (%)
- PauseDuration (s)
- Stride
- Temperature Min (°C)
- TotalEnergy
- VerticalOscillation (m)

---

## Notes

- Duplicate runs (by date) are skipped to avoid duplicates in the Excel log.
- Data is stored entirely on your own computer.
- This tool is niche: built for **Suunto app on iPhone + Mac users** who prefer local run data management and analysis.

---

## Example Workflow

1. Export yesterday’s run from Suunto app → JSON.
2. Airdrop to Mac (goes into `~/Downloads`).
3. Run:

   ```bash
   python run.py
   ```

4. Open `~/juoksut/juoksuloki.xlsx` in Excel or Numbers → create your own graphs, track progress, or analyze HR zones.

---

## License

[MIT License](LICENSE)

Free to use and modify.
