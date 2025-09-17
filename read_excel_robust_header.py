import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Read the first few rows to understand the header structure
df_raw = pd.read_excel(file_path, header=None)

# Identify the row that contains the main data headers (e.g., 'Types d\'absence', 'Date de début')
# From previous inspection, this seems to be row 6 (0-indexed)
header_row_index = 6

# Extract the header row
headers = df_raw.iloc[header_row_index]

# Read the data starting from the row after the header
df_data = pd.read_excel(file_path, header=header_row_index)

# Clean up column names: remove 'Unnamed' columns and strip whitespace
df_data.columns = [str(col).strip() for col in df_data.columns]
df_data = df_data.loc[:, ~df_data.columns.str.contains('Unnamed:')]

# Drop rows that are entirely NaN (empty rows) from the data part
df_data.dropna(how='all', inplace=True)

print("--- En-têtes identifiés ---")
print(df_data.columns.to_list())
print("\n--- Premières lignes des données de congés ---")
print(df_data.head().to_markdown(index=False))

# Now, let's try to extract the agent information from the top part of the sheet
# This part is more complex as it's not a simple table.
# We need to manually map the cells to agent attributes.

# For example, 'Nom' is in row 2, column 2 (0-indexed: [2, 2])
# 'Prénom' is in row 3, column 2 ([3, 2])
# 'Année d\'entrée dans la FP' is in row 4, column 2 ([4, 2])
# 'Date début contrat' is in row 5, column 2 ([5, 2])
# 'Date de fin' is in row 6, column 2 ([6, 2])
# 'Quotité de travail' is in row 7, column 2 ([7, 2])

# Let's create a dictionary for agent info
agent_info = {
    'Nom': df_raw.iloc[2, 2],
    'Prénom': df_raw.iloc[3, 2],
    'Année d\u0027entrée dans la FP': df_raw.iloc[4, 2],
    'Date début contrat': df_raw.iloc[5, 2],
    'Date de fin': df_raw.iloc[6, 2],
    'Quotité de travail': df_raw.iloc[7, 2]
}

print("\n--- Informations de l\u0027agent ---")
for key, value in agent_info.items():
    print(f"{key}: {value}")


