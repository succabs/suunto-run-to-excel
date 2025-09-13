import os
import json
import shutil
import pandas as pd

# Polut
downloads_path = os.path.expanduser("~/Downloads")
folder_path = os.path.expanduser("~/juoksut/json_juoksut")  # Tavoitekansio
output_path = os.path.expanduser("~/juoksut/juoksuloki.xlsx")

# Luo kansio jos ei ole
os.makedirs(folder_path, exist_ok=True)

# 🔁 Siirretään kaikki JSONit Downloadsista omaan kansioon
for file in os.listdir(downloads_path):
    if file.endswith(".json"):
        src = os.path.join(downloads_path, file)
        dst = os.path.join(folder_path, file)
        try:
            shutil.move(src, dst)
            print(f"↪ Siirretty: {file}")
        except Exception as e:
            print(f"⚠️ Virhe siirrossa {file}: {e}")

# Alusta tyhjä DataFrame tarvittavilla sarakkeilla
columns = [
    "Päivämäärä", "Kesto (s)", "Matka (m)", "EPOC", "PTE", "VO2max", "Fiilis (1-5)",
    "HR Zone 1 (s)", "HR Zone 2 (s)", "HR Zone 3 (s)", "HR Zone 4 (s)", "HR Zone 5 (s)",
    "Calories", "FitnessAge", "FitnessAgeClass", "LeftGCT (%)", "RightGCT (%)",
    "PauseDuration (s)", "Stride", "Temperature Min (°C)", "TotalEnergy", "VerticalOscillation (m)"
]

# Jos tiedosto on jo olemassa, lue se
if os.path.exists(output_path):
    df_all = pd.read_excel(output_path)
else:
    df_all = pd.DataFrame(columns=columns)

# Kerää JSON-tiedostot
new_rows = []

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                header = data["DeviceLog"]["Header"]
                hr_zones = header.get("HrZones", {})

                date = header["DateTime"][:10]

                # Duplikaattisuodatus
                if date in df_all["Päivämäärä"].astype(str).values:
                    continue

                row = {
                    "Päivämäärä": date,
                    "Kesto (s)": round(header.get("Duration", 0)),
                    "Matka (m)": header.get("Distance", None),
                    "EPOC": header.get("EPOC", None),
                    "PTE": header.get("PeakTrainingEffect", None),
                    "VO2max": header.get("MAXVO2", None),
                    "Fiilis (1-5)": header.get("Feeling", None),
                    "HR Zone 1 (s)": hr_zones.get("Zone1Duration", None),
                    "HR Zone 2 (s)": hr_zones.get("Zone2Duration", None),
                    "HR Zone 3 (s)": hr_zones.get("Zone3Duration", None),
                    "HR Zone 4 (s)": hr_zones.get("Zone4Duration", None),
                    "HR Zone 5 (s)": hr_zones.get("Zone5Duration", None),
                    "Calories": header.get("CarbohydrateConsumption", None),
                    "FitnessAge": header.get("FitnessAge", None),
                    "FitnessAgeClass": header.get("FitnessAgeClassification", None),
                    "LeftGCT (%)": header.get("LeftGroundContactBalance", {}).get("Avg", None),
                    "RightGCT (%)": header.get("RightGroundContactBalance", {}).get("Avg", None),
                    "PauseDuration (s)": header.get("PauseDuration", None),
                    "Stride": header.get("Stride", {}).get("Avg", None),
                    "Temperature Min (°C)": header.get("Temperature", {}).get("Min", None),
                    "TotalEnergy": header.get("TotalEnergy", None),
                    "VerticalOscillation (m)": header.get("VerticalOscillation", {}).get("Avg", None)
                }

                new_rows.append(row)
                print(f"✅ Lisätään lokiin: {date}")
            except Exception as e:
                print(f"⚠️ Virhe tiedostossa {filename}: {e}")

# Lisää ja järjestä
if new_rows:
    df_all = pd.concat([df_all, pd.DataFrame(new_rows)], ignore_index=True)
    df_all["Päivämäärä"] = pd.to_datetime(df_all["Päivämäärä"])
    df_all.sort_values("Päivämäärä", inplace=True)
    df_all["Päivämäärä"] = df_all["Päivämäärä"].dt.date

# Tallenna
df_all.to_excel(output_path, index=False)
print("✅ Juoksuloki päivitetty:", output_path)
