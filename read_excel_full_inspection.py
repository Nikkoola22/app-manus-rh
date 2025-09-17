import pandas as pd

file_path = '/home/ubuntu/upload/congés2022maj.xlsx'
df_raw = pd.read_excel(file_path, header=None)
print(df_raw.head(15).to_markdown(index=False))


