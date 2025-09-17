import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'
df = pd.read_excel(file_path, header=None)
print(df.head(10).to_markdown(index=False))


