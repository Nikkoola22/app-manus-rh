import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

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

# Let's define the column names manually based on the structure observed in the Excel file
leave_column_names = [
    'Type d\u0027absence', 'Date de début', 'Date de fin', 'Demi-journées', 'Motif',
    'Heures supplémentaires', 'Heures en moins', 'Solde CA', 'Solde Bonifications',
    'Nb de jours RTT', 'Nb de jours Jours de sujétions', 'Jours Congés formations',
    'Heures en moins CET', 'Solde CET', 'Nb de jours posés', 'CA restants',
    'CF restants', 'CET restants', 'Planning Jours', 'Planning Horaires début',
    'Planning Horaires fin', 'Planning nb', 'Planning Congés posés'
]

# Read the data starting from row 14 (index 13), and assign the custom column names
df_leaves = pd.read_excel(file_path, header=13) # header=13 means the 14th row is the header

# Rename columns to match our defined list, assuming they are in order
# We need to be careful here, as the actual number of columns might differ.
# Let's try to map them based on the first few columns and then use generic names for the rest if needed.

# For now, let's just clean the existing column names and inspect.
# If the number of columns in df_leaves is different from len(leave_column_names),
# we will need to adjust the leave_column_names list.

# Clean up column names: remove 'Unnamed' columns and strip whitespace
df_leaves.columns = [str(col).strip() for col in df_leaves.columns]
df_leaves = df_leaves.loc[:, ~df_leaves.columns.str.contains('Unnamed:')]

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


