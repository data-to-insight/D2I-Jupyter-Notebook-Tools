import pandas as pd
statne = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Statistical Neighbours.xlsx', sheet_name='Stats Neighbours')
print(statne)
region = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Statistical Neighbours.xlsx', sheet_name='Regions and MCA')
print(region)
# The files above only changes once Stats Neighbours updated
ofsted = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/ofsted_csc_send_overview.xlsx' ,usecols=['la_code','outcome_grade','previous_inspection_date'],engine='openpyxl')
print(ofsted) #update ofsted file every quarter - needs to be downloaded from SEND OFSTED Inspections Scrapes (Rob)
