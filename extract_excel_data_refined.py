import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Read the entire sheet without header to inspect
df_raw = pd.read_excel(file_path, header=None)

# --- Extraction des informations de l'agent ---
# Based on visual inspection of df_raw.head(15)
agent_info = {
    'Nom': df_raw.iloc[2, 2], # Row 3, Col C
    'Prénom': df_raw.iloc[3, 2], # Row 4, Col C
    'Année d\'entrée dans la FP': df_raw.iloc[4, 2], # Row 5, Col C
    'Date début contrat': df_raw.iloc[5, 2], # Row 6, Col C
    'Date de fin': df_raw.iloc[6, 2], # Row 7, Col C
    'Quotité de travail': df_raw.iloc[7, 2] # Row 8, Col C
}

print("--- Informations de l'agent ---")
for key, value in agent_info.items():
    print(f"{key}: {value}")

# --- Extraction des données de congés ---
# From the `df_raw.head(15)` output, the actual leave request table seems to start around row 14 (index 13).
# The headers for this table are in row 14 (index 13) and row 15 (index 14).
# Let's try to read the data starting from row 14 (index 13) and then clean up the headers.

# Read the data, using row 14 (index 13) as the header row
df_leaves = pd.read_excel(file_path, header=13)

# The actual column names are in the first row of the data frame after setting header=13.
# Let's take the first row as the new column names and then drop it.
new_header = df_leaves.iloc[0] # Grab the first row for the headers
df_leaves = df_leaves[1:] # Take the data less the header row
df_leaves.columns = new_header # Set the header row as the df header

# Clean up column names: remove 'Unnamed' columns and strip whitespace
df_leaves.columns = [str(col).strip() for col in df_leaves.columns]
df_leaves = df_leaves.loc[:, ~df_leaves.columns.str.contains('Unnamed:')]

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


