import pandas as pd
import plotly.express as px

df = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/choropleth/header.csv')

# chne = df['ETHNIC'] == 'CHNE'
# bracknell = df['LA'] == 'Bracknell Forest'

# print(chne)

# df_chne = df[(chne & bracknell) | (df['ETHNIC'] == 'BAFR')]

# df_c_b = df[df['ETHNIC'].isin(['CHNE', 'BAFR'])]

# mother_df = df[df['MOTHER'].notna()]
# not_mother_df = df[df['MOTHER'].isna()]

child_per_la = df.groupby('LA').size().to_frame('Count').reset_index()

fig = px.bar(child_per_la, 
             'LA', 
             'Count',
             labels={'Count':'Number of Children'},
             title='Good title')

fig.show()