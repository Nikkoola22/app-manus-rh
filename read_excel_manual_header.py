import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Manually identified relevant columns and their intended names based on visual inspection
column_names = [
    'ID', 'Nom', 'Prénom', 'Année d\'entrée dans la FP', 'Date début contrat', 'Date de fin', 'Quotité de travail',
    'Congés annuels acquis', 'Bonifications', 'Ancienneté suite 1607h', 'RTT acquis', 'Jours de sujétions', 'Congés formations', 'CET',
    'Déduits après arrêts', 'Ouverture droit aux journées de bonification 1er janv au 30 avril', 'Ouverture droit aux journées de bonification 1er Nov au 31 déc', 'Total bonification',
    'Nb de jours posés', 'CA restants', 'CF restants', 'CET restants',
    'Planning Jours', 'Planning Horaires début', 'Planning Horaires fin', 'Planning nb', 'Planning Congés posés'
]

# Read the Excel file, skipping initial rows and then re-assigning column names
df = pd.read_excel(file_path, header=None, skiprows=5) # Skip initial rows that are not part of the data

# Adjust column names if the DataFrame has more columns than defined
if df.shape[1] > len(column_names):
    df = df.iloc[:, :len(column_names)]
elif df.shape[1] < len(column_names):
    # If there are fewer columns, we need to adjust column_names to match df.shape[1]
    column_names = column_names[:df.shape[1]]

df.columns = column_names

# Drop rows where 'Nom' and 'Prénom' are NaN, as these are likely empty rows or part of the header structure
df.dropna(subset=['Nom', 'Prénom'], inplace=True)

print(df.head().to_markdown(index=False))
print(df.columns.to_list())


