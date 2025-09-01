import pandas as pd
import json

#Config
file_path = "Elden Ring Nightreign map patterns.xlsx"  
output_json = "evergaol_mapping.json"
output_csv = "evergaol_mapping.csv"

# Load spreadsheet
# header=None so we can manually interpret first two rows
df = pd.read_excel(file_path, sheet_name="Patterns", header=None)

# Row 0 = category (Evergaol, Castle, etc.)
# Row 1 = location names
# Row 2+ = actual data rows
categories = df.iloc[0]
locations = df.iloc[1]
data = df.iloc[2:].reset_index(drop=True)

# Metadata columns (the first 3 cols always contain these)
metadata_cols = ["Nightlord", "Shifting Earth", "Map ID"]
metadata = data.iloc[:, :3]
metadata.columns = metadata_cols

#Just keeping gaols for now
evergaol_mask = categories == "Evergaol"
evergaol_cols = df.columns[evergaol_mask]

#Build the structured mapping
mapping = {}
rows = []  # for CSV export

for idx, row in data.iterrows():
    nightlord = row.iloc[0]
    shifting_earth = row.iloc[1]
    map_id = row.iloc[2]
    key = f"{nightlord}-{shifting_earth}-{map_id}"

    entry = {}
    for col in evergaol_cols:
        location_name = locations[col]
        boss_value = row[col]
        if pd.notna(boss_value):  # only keep filled cells
            entry[location_name] = boss_value

    mapping[key] = entry

    # For CSV-friendly tabular output
    for loc, boss in entry.items():
        rows.append({
            "Nightlord": nightlord,
            "Shifting Earth": shifting_earth,
            "Map ID": map_id,
            "Evergaol": loc,
            "Boss": boss
        })

#Save
with open(output_json, "w") as f:
    json.dump(mapping, f, indent=2)

csv_df = pd.DataFrame(rows)
csv_df.to_csv(output_csv, index=False)

print(f"Saved {len(mapping)} map variants to {output_json} and {output_csv}")
