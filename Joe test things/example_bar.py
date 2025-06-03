import pandas as pd
import plotly.express as px

df = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/choropleth/header.csv')

child_per_la = df.groupby('LA').size().to_frame('Count').reset_index()

fig = px.bar(child_per_la, 
             'LA', 
             'Count',
             labels={'Count':'Number of Children'},
             title='Good title')

fig.show()