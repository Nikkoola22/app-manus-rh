import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'
df = pd.read_excel(file_path)
print(df.head().to_markdown(index=False))
print(df.columns.to_list())


