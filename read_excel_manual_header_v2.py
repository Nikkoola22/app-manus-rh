import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Read the Excel file without any header to inspect the raw data
df_raw = pd.read_excel(file_path, header=None)

# Based on the previous inspection, the relevant headers are spread across multiple rows.
# Let's try to extract the main categories from row 1 (index 0) and row 2 (index 1)
# and the specific column names from row 6 (index 5) and row 7 (index 6) for the actual data.

# For the main data table, it seems the headers are in row 6 (index 5) and row 7 (index 6)
# Let's try to combine them. The actual data starts from row 8 (index 7).

# Read the header rows specifically
header_df = pd.read_excel(file_path, header=None, nrows=8)

# Extracting the main header row (index 5) and sub-header row (index 6)
main_header = header_df.iloc[5]
sub_header = header_df.iloc[6]

# Combine the headers. We need to handle NaN values and duplicate names.
combined_header = []
for i in range(len(main_header)):
    main_val = str(main_header[i]).strip()
    sub_val = str(sub_header[i]).strip()

    if main_val == 'nan' and sub_val == 'nan':
        combined_header.append(f'Unnamed_Col_{i}')
    elif main_val == 'nan':
        combined_header.append(sub_val)
    elif sub_val == 'nan' or main_val == sub_val:
        combined_header.append(main_val)
    else:
        combined_header.append(f'{main_val} - {sub_val}')

# Read the actual data starting from row 8 (index 7)
df = pd.read_excel(file_path, header=None, skiprows=7)

# Assign the combined headers to the DataFrame
df.columns = combined_header[:len(df.columns)]

# Drop rows that are entirely NaN (empty rows)
df.dropna(how='all', inplace=True)

# Further cleaning: drop columns that are still 'Unnamed_Col_X' and contain mostly NaN values
df = df.loc[:, ~df.columns.str.contains('Unnamed_Col_')]

print(df.head().to_markdown(index=False))
print(df.columns.to_list())


