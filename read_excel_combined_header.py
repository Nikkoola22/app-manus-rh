import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'

# Read the first few rows to understand the header structure
df_header = pd.read_excel(file_path, header=None, nrows=7)

# Extract relevant parts for combined headers
# Row 2 (index 1) contains 'Année', 'Congés annuels', 'Bonifications', 'RTT', 'Jours de sujétions', 'Congés formations', 'CET'
# Row 3 (index 2) contains 'Nom', 'Prénom'
# Row 4 (index 3) contains 'Année d'entrée dans la FP', 'Date début contrat', 'Date de fin', 'Quotité de travail'
# Row 6 (index 5) contains the actual data headers for the leave requests

# Let's try to construct the headers more systematically.
# First, get the main categories from row 1 (index 0) and row 2 (index 1)
# Then, the sub-categories from row 3 (index 2) and row 4 (index 3)
# And finally, the detailed headers from row 6 (index 5)

# For simplicity, let's assume the actual data starts from row 7 (index 6)
# and the headers are in row 6 (index 5)

df = pd.read_excel(file_path, header=5) # Try header=5 (6th row, 0-indexed)

# Clean up column names - remove unnamed columns and strip whitespace
df.columns = [col for col in df.columns if not 'Unnamed:' in str(col)]
df.columns = [str(col).strip() for col in df.columns]

print(df.head().to_markdown(index=False))
print(df.columns.to_list())


