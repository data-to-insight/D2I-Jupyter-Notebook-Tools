import pandas as pd
statne = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Statistical Neighbours.xlsx', sheet_name='Stats Neighbours')
region = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Statistical Neighbours.xlsx', sheet_name='Regions and MCA')
# The files above only changes once Stats Neighbours updated
ofsted = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/ofsted_csc_send_overview.xlsx' ,usecols=['la_code','outcome_grade','previous_inspection_date'],engine='openpyxl')
#update ofsted file every quarter - needs to be downloaded from SEND OFSTED Inspections Scrapes (Rob)
region_merged=region.merge(ofsted,left_on='LA Code', right_on='la_code',how='left')
region_merged=region_merged.drop(columns=['la_code','previous_inspection_date'])
population = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/ONS Mid Year 2024 - corrected names.xlsx',sheet_name='CreateCustomGroup',skiprows=4)
#Upload Population Statistic (needed for Rates Calculations)
population=population.drop(population.columns[[0,2,3,4]],axis=1)
table = region_merged.merge(population,left_on='LA Code', right_on='Code',how='left')
table=table.drop(columns=['Code'])
statnejoin=statne.merge(table,left_on='Stats Neighbour LA Code',right_on='LA Code',how='left')
statnejoin=statnejoin.drop(statnejoin.columns[[4,5,6,7,8,9]],axis=1)
statnejoin_filtered = statnejoin[statnejoin["LANo"] != statnejoin["Stats Neighbour LA Code"]]
statnejoin_filtered=statnejoin_filtered.drop(statnejoin_filtered.columns[[2,3]],axis=1)
statnejoin_filtered.columns=["LANo","LAName","Pop_0_17","Pop_0_25","Pop_0_4","Pop_5_10","Pop_11_15","Pop_16_19","Pop_20_25","Pop_5_16"]
#Join Table with Stats Neighbours and drop columns (Data prep)
statnejoin_filtered=statnejoin_filtered.apply(pd.to_numeric,errors="coerce")
statnejoin_filtered["Pop_17_25"]=statnejoin_filtered["Pop_0_25"]-statnejoin_filtered["Pop_0_4"]-statnejoin_filtered["Pop_5_16"]
statne_groupby=statnejoin_filtered.groupby("LANo").sum(numeric_only=True)
statne_groupby=statne_groupby.drop(columns=['LAName'])
#Statne_groupby has all population aggregated by statistical neighbours for each LA (LA No)
table.columns=["LACode","LAName","Region","MCA","TypeLA","Outcome_OFSTED","Pop_0_17","Pop_0_25","Pop_0_4","Pop_5_10","Pop_11_15","Pop_16_19","Pop_20_25","Pop_5_16"]
cols=["Pop_0_17","Pop_0_25","Pop_0_4","Pop_5_10","Pop_11_15","Pop_16_19","Pop_20_25","Pop_5_16"]
table[cols]=table[cols].apply(pd.to_numeric,errors="coerce")
table["Pop_17_25"]=table["Pop_0_25"]-table["Pop_0_4"]-table["Pop_5_16"]
#print(table.dtypes)
mca_groupby=table.groupby("MCA").sum(numeric_only=True)
mca_groupby=mca_groupby.drop(columns=['LACode','Outcome_OFSTED'])
mca_groupby=mca_groupby.reset_index()
MCA_Unpivot=mca_groupby.melt(id_vars="MCA",var_name="Popoulation_Type",value_name="Value")
MCA_Unpivot=MCA_Unpivot.sort_values(["MCA"])
#print(MCA_Unpivot.columns)
#mca_groupby shows all population aggregated by MCA
region_groupby=table.groupby("Region").sum(numeric_only=True)
region_groupby=region_groupby.drop(columns=['LACode','Outcome_OFSTED'])
region_groupby=region_groupby.reset_index()
Region_Unpivot=region_groupby.melt(id_vars="Region",var_name="Popoulation_Type",value_name="Value")
Region_Unpivot=Region_Unpivot.sort_values(["Region"])
#print(Region_Unpivot)
#region_groupby shows all population aggregated by region
Rate_Calc = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Lookups Calculations.xlsx', sheet_name='Rate Pop')
statne_groupby=statne_groupby.reset_index()
Statne_Unpivot=statne_groupby.melt(id_vars="LANo",var_name="Popoulation_Type",value_name="Value")
Statne_Unpivot=Statne_Unpivot.sort_values(["LANo"])
#Statne_Unpivot shows you all population aggregated by stats neighbour for each LA No. 
Data_raw = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Master Data - Original.xlsx')
#Data_raw is the MASTER Table with all LAs data submissions - needs to be replaced each quarter.
Data=Data_raw.merge(Rate_Calc, on="Measure ID", how="left")
Data=Data.drop(columns=['Measure Name','Measure Quality'])
table_all=table.drop(columns=['LAName','Region','MCA','TypeLA','Outcome_OFSTED'])
table_all=table_all.reset_index()
table_all=table_all.melt(id_vars="LACode",var_name="Popoulation_Type",value_name="Value")
table_all=table_all.sort_values(["LACode"])
#table_all has all Pop Type with value for each LACode.
Data=Data.merge(table_all,left_on=["LA Code","Pop"],right_on=["LACode","Popoulation_Type"],how="left")
Data=Data.drop(columns=["LACode","LA Name","Popoulation_Type","Pop"])
Data["Measure Value"]=pd.to_numeric(Data["Measure Value"],errors="coerce")
Data["Rate10k"]=Data["Measure Value"]/Data["Value"]*10000
Data=Data.drop(columns=["Value"])
#Calculate Rate per 10k.
#Methodology: need to map Population type for correct LA and then value/population*10000
Perc_Calc = pd.read_excel('/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/Lookups Calculations.xlsx', sheet_name='Percentage')
Data=Data.merge(Perc_Calc,left_on="Measure ID",right_on="Numerator",how="left")
Denominator=Data.drop(columns=["Region","Rate10k","Numerator"])
Data=Data.merge(Denominator, left_on=["LA Code","Financial Year","Quarter","Denominator"],right_on=["LA Code","Financial Year","Quarter","Measure ID"],how="left")
Data=Data.drop(columns=["Denominator_y","Measure ID_y","Numerator","Denominator_x"])
Data=Data.rename(columns={"Measure ID_x":"Measure ID", "Measure Value_x": "Value","Measure Value_y":"Denominator"})
Data["Percentage"]=Data["Value"]/Data["Denominator"]*100
Data=Data.drop(columns=["Denominator"])
#Calculate Percentages
#Methodology: Percentages are calculate only for specific Measure IDs - map to correct format to identify denominator for correct LA, FY and Quarter

#Below are the steps to obtain Rate and Percentages but by Region breakdown against quarterly raw data. 
R_Data=Data_raw.drop(columns=["LA Name","Measure Name","Measure Quality"])
R_Data["Measure Value"]=pd.to_numeric(R_Data["Measure Value"],errors="coerce")
R_Data = R_Data.drop_duplicates(subset=["Region","LA Code", "Financial Year", "Quarter", "Measure ID"])
R_Data=(R_Data.groupby(["Region","Financial Year","Quarter","Measure ID"])["Measure Value"].sum().reset_index())
#Aggregate measures by region, FY, Quarter and Measure ID
R_Data=R_Data.merge(Rate_Calc, on="Measure ID", how="left")
R_Data = R_Data.drop_duplicates(subset=["Region","Financial Year", "Quarter", "Measure ID","Measure Value"])
#Region_Unpivot has all Pop Type with value for each Region
R_Data=R_Data.merge(Region_Unpivot,left_on=["Region","Pop"],right_on=["Region","Popoulation_Type"],how="left")
R_Data=R_Data.drop(columns=["Popoulation_Type","Pop"])
R_Data["Measure Value"]=pd.to_numeric(R_Data["Measure Value"],errors="coerce")
R_Data["Rate10k"]=R_Data["Measure Value"]/R_Data["Value"]*10000
R_Data=R_Data.drop(columns=["Value"])
#Calculate Rate per 10k.
#Methodology: need to map Population type for correct Region and then value/population*10000
R_Data=R_Data.merge(Perc_Calc,left_on="Measure ID",right_on="Numerator",how="left")
Denominator=R_Data.drop(columns=["Rate10k","Numerator"])
R_Data=R_Data.merge(Denominator, left_on=["Region","Financial Year","Quarter","Denominator"],right_on=["Region","Financial Year","Quarter","Measure ID"],how="left")
R_Data=R_Data.drop(columns=["Denominator_y","Measure ID_y","Numerator","Denominator_x"])
R_Data=R_Data.rename(columns={"Measure ID_x":"Measure ID", "Measure Value_x": "Value","Measure Value_y":"Denominator"})
R_Data["Percentage"]=R_Data["Value"]/R_Data["Denominator"]*100
R_Data=R_Data.drop(columns=["Denominator"])
#print(R_Data.sample(10))
#Calculate Percentages
#Methodology: Percentages are calculate only for specific Measure IDs - map to correct format to identify denominator for correct Region, FY and Quarter

#Below are the steps to obtain Rate and Percentages by Mayoral Combined Authority breakdown against quarterly raw data. 
table_mca=table[["LACode","MCA"]]
MCA_Data=Data_raw.merge(table_mca,left_on="LA Code",right_on="LACode",how="left")
MCA_Data=MCA_Data[["MCA","LA Code","Financial Year","Quarter","Measure ID","Measure Value"]]
MCA_Data["Measure Value"]=pd.to_numeric(MCA_Data["Measure Value"],errors="coerce")
MCA_Data=MCA_Data.sort_values(["Measure Value"],ascending=False)
MCA_Data=(MCA_Data.groupby(["MCA","Financial Year","Quarter","Measure ID"])["Measure Value"].sum().reset_index())
MCA_Data=MCA_Data.merge(Rate_Calc, on="Measure ID", how="left")
MCA_Data = MCA_Data.drop_duplicates(subset=["MCA","Financial Year", "Quarter", "Measure ID","Measure Value"])
#MCA_Unpivot has all Pop Type with value for each MCA
MCA_Data=MCA_Data.merge(MCA_Unpivot,left_on=["MCA","Pop"],right_on=["MCA","Popoulation_Type"],how="left")
MCA_Data=MCA_Data.drop(columns=["Popoulation_Type","Pop"])
MCA_Data["Measure Value"]=pd.to_numeric(MCA_Data["Measure Value"],errors="coerce")
MCA_Data["Rate10k"]=MCA_Data["Measure Value"]/MCA_Data["Value"]*10000
MCA_Data=MCA_Data.drop(columns=["Value"])
#Calculate Rate per 10k.
#Methodology: need to map Population type for correct MCA and then value/population*10000
MCA_Data=MCA_Data.merge(Perc_Calc,left_on="Measure ID",right_on="Numerator",how="left")
Denominator=MCA_Data.drop(columns=["Rate10k","Numerator"])
MCA_Data=MCA_Data.merge(Denominator, left_on=["MCA","Financial Year","Quarter","Denominator"],right_on=["MCA","Financial Year","Quarter","Measure ID"],how="left")
MCA_Data=MCA_Data.drop(columns=["Denominator_y","Measure ID_y","Numerator","Denominator_x"])
MCA_Data=MCA_Data.rename(columns={"Measure ID_x":"Measure ID", "Measure Value_x": "Value","Measure Value_y":"Denominator"})
MCA_Data["Percentage"]=MCA_Data["Value"]/MCA_Data["Denominator"]*100
MCA_Data=MCA_Data.drop(columns=["Denominator"])
#Calculate Percentages
#Methodology: Percentages are calculate only for specific Measure IDs - map to correct format to identify denominator for correct Region, FY and Quarter

with pd.ExcelWriter("/workspaces/D2I-Jupyter-Notebook-Tools/Vanessa_Trial/SEND RIIA Data Clean.xlsx") as writer: 
   Data.to_excel(writer, sheet_name="MainData",index=False)
   R_Data.to_excel(writer, sheet_name="RegionalData",index=False)
   MCA_Data.to_excel(writer, sheet_name="MCAData",index=False)