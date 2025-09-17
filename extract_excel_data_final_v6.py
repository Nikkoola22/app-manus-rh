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
# The actual table headers for leave requests seem to be in row 14 (index 13) and row 15 (index 14).
# The data starts from row 16 (index 15).

# Read the header rows specifically for the leave table
header_leaves_df = pd.read_excel(file_path, header=None, skiprows=13, nrows=2)

# Define the final column names based on the Excel structure
# This is a manual mapping after careful inspection of the raw data output
final_leave_column_names = [
    'Type d\u0027absence', 'Date de début', 'Date de fin', 'Demi-journées', 'Motif',
    'Heures supplémentaires', 'Heures en moins', 'Solde CA', 'Solde Bonifications',
    'Nb de jours RTT', 'Nb de jours Jours de sujétions', 'Jours Congés formations',
    'Heures en moins CET', 'Solde CET', 'Nb de jours posés', 'CA restants',
    'CF restants', 'CET restants'
]

# Read the actual data for leaves, starting from row 16 (index 15)
df_leaves = pd.read_excel(file_path, header=None, skiprows=15)

# Drop columns that are entirely NaN before assigning new headers
df_leaves.dropna(axis=1, how='all', inplace=True)

# Assign the manually defined headers to the DataFrame
if len(df_leaves.columns) == len(final_leave_column_names):
    df_leaves.columns = final_leave_column_names
elif len(df_leaves.columns) > len(final_leave_column_names):
    # If there are more columns in the dataframe, truncate to match our defined headers
    df_leaves = df_leaves.iloc[:, :len(final_leave_column_names)]
    df_leaves.columns = final_leave_column_names
else:
    # If there are fewer columns, this indicates an issue with header identification or missing data
    print("Warning: DataFrame has fewer columns than the defined headers. Adjusting headers.")
    # For now, assign what we can and leave the rest as default pandas columns
    df_leaves.columns = final_leave_column_names[:len(df_leaves.columns)]

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


