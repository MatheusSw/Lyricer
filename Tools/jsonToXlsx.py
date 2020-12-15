import pandas as pd
import pathlib

# From json to xlsx, just because it's easier to feed to the AI
path = str(pathlib.Path(__file__).parent.absolute().parent)
json_path = pathlib.PurePath(path, 'Lyrics/BROCKHAMPTON_filtered.json')
new_excel_path = pathlib.PurePath(path, 'Lyrics/BROCKHAMPTON_filtered.xlsx')

df = pd.read_json(json_path)

df = df.to_excel(new_excel_path, encoding='utf-8')
df = pd.read_excel(new_excel_path)
df = df.dropna()

df = df.drop(['title', 'release', 'album'], axis=1)
df = df.drop(df.columns[0], axis=1)
df.to_excel(new_excel_path, encoding='utf-8')
