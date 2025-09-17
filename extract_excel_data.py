import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Read the entire sheet to inspect
df_raw = pd.read_excel(file_path, header=None)

# --- Extraction des informations de l'agent ---
agent_info = {
    'Nom': df_raw.iloc[2, 2],
    'Prénom': df_raw.iloc[3, 2],
    'Année d\u0027entrée dans la FP': df_raw.iloc[4, 2],
    'Date début contrat': df_raw.iloc[5, 2],
    'Date de fin': df_raw.iloc[6, 2],
    'Quotité de travail': df_raw.iloc[7, 2]
}

print("--- Informations de l\u0027agent ---")
for key, value in agent_info.items():
    print(f"{key}: {value}")

# --- Extraction des données de congés ---
# The actual table headers are in row 6 (index 6) of the raw DataFrame
# The data starts from row 7 (index 7)

# Read the data starting from row 7, using row 6 as header
df_leaves = pd.read_excel(file_path, header=6)

# Clean up column names: remove 'Unnamed' columns and strip whitespace
df_leaves.columns = [str(col).strip() for col in df_leaves.columns]
df_leaves = df_leaves.loc[:, ~df_leaves.columns.str.contains('Unnamed:')]

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


