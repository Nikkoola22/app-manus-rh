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

# Manually define the column names based on the Excel structure from row 14 (index 13)
# and combining with relevant information from row 15 (index 14).

# Read the header rows specifically for the leave table
header_leaves_df = pd.read_excel(file_path, header=None, skiprows=13, nrows=2)

# Combine the two header rows into a single list of column names
combined_leave_headers = []
for col_idx in range(len(header_leaves_df.columns)):
    header_row1_val = str(header_leaves_df.iloc[0, col_idx]).strip()
    header_row2_val = str(header_leaves_df.iloc[1, col_idx]).strip()

    if header_row1_val == 'nan' and header_row2_val == 'nan':
        combined_leave_headers.append(f'Col_{col_idx}')
    elif header_row1_val == 'nan':
        combined_leave_headers.append(header_row2_val)
    elif header_row2_val == 'nan' or header_row1_val == header_row2_val:
        combined_leave_headers.append(header_row1_val)
    else:
        combined_leave_headers.append(f'{header_row1_val} - {header_row2_val}')

# Read the actual data for leaves, starting from row 16 (index 15)
df_leaves = pd.read_excel(file_path, header=None, skiprows=15)

# Assign the combined headers to the DataFrame
# Ensure the number of columns matches, truncate if too many, or pad if too few
if len(df_leaves.columns) > len(combined_leave_headers):
    df_leaves = df_leaves.iloc[:, :len(combined_leave_headers)]
    df_leaves.columns = combined_leave_headers
elif len(df_leaves.columns) < len(combined_leave_headers):
    # This case is tricky, it means our header definition is wider than the data.
    # We should probably re-evaluate the header definition or fill with NaNs.
    # For now, let's just use the available columns and print a warning.
    print("Warning: DataFrame has fewer columns than the combined header. Adjusting headers.")
    df_leaves.columns = combined_leave_headers[:len(df_leaves.columns)]
else:
    df_leaves.columns = combined_leave_headers

# Drop rows that are entirely NaN (empty rows) from the data part
df_leaves.dropna(how='all', inplace=True)

# Further cleaning: remove columns that are still generic names and contain mostly NaN values
df_leaves = df_leaves.loc[:, ~df_leaves.columns.str.contains('Col_')]

print("\n--- Premières lignes des données de congés ---")
print(df_leaves.head().to_markdown(index=False))
print("\n--- En-têtes des données de congés ---")
print(df_leaves.columns.to_list())


