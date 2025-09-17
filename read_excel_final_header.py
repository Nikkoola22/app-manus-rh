import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Read the header rows specifically
header_df = pd.read_excel(file_path, header=None, nrows=7)

# Extracting the main header row (index 5) and sub-header row (index 6)
main_header = header_df.iloc[5]
sub_header = header_df.iloc[6]

# Combine the headers. We need to handle NaN values and duplicate names.
combined_header = []
for i in range(len(main_header)):
    main_val = str(main_header[i]).strip()
    sub_val = str(sub_header[i]).strip()

    if main_val == 'nan' and sub_val == 'nan':
        combined_header.append(f'Col_{i}') # Use a generic name for completely empty columns
    elif main_val == 'nan':
        combined_header.append(sub_val)
    elif sub_val == 'nan' or main_val == sub_val:
        combined_header.append(main_val)
    else:
        combined_header.append(f'{main_val} - {sub_val}')

# Read the actual data starting from row 8 (index 7)
df = pd.read_excel(file_path, header=None, skiprows=7)

# Assign the combined headers to the DataFrame
# Ensure the number of columns matches
if len(combined_header) > len(df.columns):
    df.columns = combined_header[:len(df.columns)]
elif len(combined_header) < len(df.columns):
    # If the dataframe has more columns than our combined header, pad with generic names
    df.columns = combined_header + [f'Col_{i}' for i in range(len(combined_header), len(df.columns))]
else:
    df.columns = combined_header

# Drop rows that are entirely NaN (empty rows)
df.dropna(how='all', inplace=True)

# Further cleaning: drop columns that are still generic names and contain mostly NaN values
# This step might need refinement based on actual data, but for now, let's keep it simple.
# df = df.loc[:, ~df.columns.str.contains('Col_')] # This might remove useful columns if generic names are used for actual data

print(df.head().to_markdown(index=False))
print(df.columns.to_list())


