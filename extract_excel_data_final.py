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

# Manually define the column names based on the Excel structure from row 14 (index 13)
# and combining with relevant information from row 13 (index 12) if necessary.
# Let's re-examine the raw data output to get the exact column names.

# From the `df_raw.head(15)` output, row 13 (index 12) contains: 'Types d\u0027absence', 'Date de début', 'Date de fin', etc.
# Row 14 (index 13) contains: 'CA', 'RTT', 'CET', etc.

# Let's try to read the table starting from row 13 (index 12) and then clean up the headers.

df_leaves = pd.read_excel(file_path, header=12) # Use row 13 (index 12) as the header

# Clean up column names. The first row of the actual table (header=12) contains the main categories.
# The second row (which is now the first data row) contains sub-categories or specific types.
# We need to combine them or select the most relevant ones.

# Let's inspect the columns after reading with header=12
current_columns = df_leaves.columns.to_list()

# Based on the Excel file, the relevant headers for the leave table are:
# Types d'absence, Date de début, Date de fin, Demi-journées, motif, Heures supplémentaires, Heures en moins, Solde, Solde.1, nb de jours, nb de jours.1, Jours, Heures en moins.1, Solde.2, Nb de jours.2, CA, CF, CET

# Let's manually map the column names to be more descriptive
new_column_names = [
    'Type d\u0027absence', 'Date de début', 'Date de fin', 'Demi-journées', 'Motif',
    'Heures supplémentaires', 'Heures en moins', 'Solde CA', 'Solde Bonifications',
    'Nb de jours RTT', 'Nb de jours Jours de sujétions', 'Jours Congés formations',
    'Heures en moins CET', 'Solde CET', 'Nb de jours posés', 'CA restants',
    'CF restants', 'CET restants'
]

# Adjust the dataframe columns to match the new_column_names
# First, drop any columns that are entirely NaN or are not part of the main data structure
df_leaves.dropna(axis=1, how='all', inplace=True)

# Then, rename the columns. We need to ensure the number of columns matches.
if len(df_leaves.columns) == len(new_column_names):
    df_leaves.columns = new_column_names
elif len(df_leaves.columns) > len(new_column_names):
    # If there are more columns in the dataframe, truncate or adjust new_column_names
    df_leaves = df_leaves.iloc[:, :len(new_column_names)]
    df_leaves.columns = new_column_names
else:
    # If there are fewer columns, this indicates an issue with header identification
    print("Warning: Number of columns in DataFrame is less than expected. Check header definition.")
    # Fallback to current columns and try to clean them
    df_leaves.columns = [str(col).strip() for col in df_leaves.columns]

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


