import pandas as pd
import plotly.express as px

# || read in data sets ||
# df_episodes = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_episodes.csv')
df_header = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_header.csv')
# df_missing = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_missing.csv')
# df_osc2 = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_oc2.csv')
# df_osc3 = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_oc3.csv')
# df_prevperm = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_prev_perm.csv')
# df_reviews = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_reviews.csv')
# df_uasc = pd.read_csv('/workspaces/D2I-Jupyter-Notebook-Tools/Joe test things/Data/351_2017_uasc.csv')

# || define functions for plotting ||

# #bar chart
def fn_barchart(variable,xval,yval,colval,figurefeatures):
    fig = px.bar(variable, 
                xval, 
                yval,
                color = colval,
                labels={ xval:figurefeatures[0],
                        yval : figurefeatures[1],
                        colval: figurefeatures[2]},
                title= figurefeatures[3])

    gender_rename = {'1':'Male', '2':'Female'}

    fig.for_each_trace(lambda t: t.update(name = gender_rename[t.name],
                                        legendgroup = gender_rename[t.name],
                                        hovertemplate = t.hovertemplate.replace(t.name, gender_rename[t.name])
                                        )
                    )

    fig.show()

# #pie chart 


# || define groupings ||

# child_per_la = df_header.groupby('LA')

# child_per_la_gendersplit = df_header.groupby(['LA','SEX']).agg({'SEX' : 'sum'})

# child_per_la_gendersplit_perc = child_per_la_gendersplit.groupby(level = 0).apply(lambda x: 100*x/float(x.sum()))

# child_per_la_gendersplit = df_header.groupby(['LA','SEX']).agg({'SEX' : 'sum'})
# child_per_la = df_header.groupby('LA').agg({'SEX' : 'sum'})

# child_per_la_gendersplit_perc = child_per_la_gendersplit.div(child_per_la, level='LA') *100

child_per_la_gendersplit = df_header.groupby(['LA','SEX'])

df_header['%'] = 100*df_header['SEX'] /df_header.groupby('LA')['SEX'].transform('sum')
 
print(child_per_la_gendersplit)

print(df_header)

#print(child_per_la_gendersplit_perc)

# child_per_la_gendersplit = df_header.groupby(['LA','SEX']).size().to_frame('Count').reset_index()



# total_per_la = df_header['LA'].value_counts()

# print(total_per_la)



# total_per_la['SEX'] = total_per_la['SEX'].astype(str)                       #convert SEX to str to show as discrete colors when plotting

# male_per_la = total_per_la['SEX'].apply(lambda x : x.str.contains('1').sum())

# print(male_per_la)

# sex_perc = child_per_la_gendersplit['SEX'].value_counts()

# print(child_per_la_gendersplit)

# child_per_la_gendersplit['SEX'] = child_per_la_gendersplit['SEX'].astype(str)                       #convert SEX to str to show as discrete colors when plotting

# print(sex_perc)

# xlabel = "Local Authority"
# ylabel = 'Number of Children'
# collabel = 'Gender'
# title = 'Gender distribution across Local Authorities'

# figlabels = [xlabel, ylabel, collabel, title]

#fn_barchart(child_per_la_gendersplit,'LA','Count',sex_perc,figlabels)

