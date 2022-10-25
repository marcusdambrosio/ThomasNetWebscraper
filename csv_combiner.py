import pandas as pd
import os

def combine_csvs(fileDir):
    master = pd.concat([pd.read_csv(fileDir+'/'+csvFile) for csvFile in os.listdir(fileDir)])
    master.reset_index(drop = True, inplace = True)
    uniqueCompanies = []
    for ind, row in master.iterrows():
        if row['company_name'] in uniqueCompanies:
            master.drop(ind, axis = 0, inplace = True)
        else:
            uniqueCompanies.append(row['company_name'])
   
    master.to_csv(f'{fileDir}/MASTER.csv')
