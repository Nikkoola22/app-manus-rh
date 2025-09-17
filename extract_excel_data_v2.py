import pandas as pd

file_path = '/home/ubuntu/upload/congés20222maj.xlsx'

# Read the entire sheet without header to inspect
df_raw = pd.read_excel(file_path, header=None)

# --- Extraction des informations de l'agent ---
# Based on visual inspection of df_raw.head(15)
agent_info = {
    'Nom': df_raw.iloc[2, 2], # Row 3, Col C
    'Prénom': df_raw.iloc[3, 2], # Row 4, Col C
    'Année d\u0027entrée dans la FP': df_raw.iloc[4, 2], # Row 5, Col C
    'Date début contrat': df_raw.iloc[5, 2], # Row 6, Col C
    'Date de fin': df_raw.iloc[6, 2], # Row 7, Col C
    'Quotité de travail': df_raw.iloc[7, 2] # Row 8, Col C
}

print("--- Informations de l\u0027agent ---")
for key, value in agent_info.items():
    print(f"{key}: {value}")

# --- Extraction des données de congés ---
# The actual table headers for leave requests seem to be in row 14 (index 13) of the raw DataFrame
# The data starts from row 15 (index 14)

# Read the data starting from row 14, using row 13 as header
df_leaves = pd.read_excel(file_path, header=13)

# Clean up column names: remove 'Unnamed' columns and strip whitespace
df_leaves.columns = [str(col).strip() for col in df_leaves.columns]
df_leaves = df_leaves.loc[:, ~df_leaves.columns.str.contains('Unnamed:')]

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


