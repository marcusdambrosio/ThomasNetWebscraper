import pandas as pd
import numpy as np
import sys
import time
import math

def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

def addressSplitting(file = None, data = None):
    if file != None:
        data = pd.read_csv(file)

    addresses = data['address'].tolist()
    cities = []
    states = []
    zips = []
    for add in addresses:
        try:
            end = add.split(', ')[1]
            states.append(end[:2])
            zips.append(end[3:8])
            cities.append(add.split(',')[0])
        except:
            states.append('Failed')
            zips.append('Failed')
            cities.append('Failed')

    addressDf = pd.DataFrame({'city' : cities,
                              'state' : states,
                              'zip' : zips})
    addressDf.fillna(value = 'Failed', inplace = True)
    return addressDf




def busDetailSplitting(file = None, data = None):
    if file != None:
        data = pd.read_csv(file)
    busDetailsDf = pd.DataFrame()

    for i ,dets in enumerate(data['bus_details']):
        busDetails = {}
        busDetails['companyName'] = data.loc[i, 'company_name']
        try:
            website = dets[list(find_all(dets,'href="'))[0] + 6: list(find_all(dets,'"'))[1]]
            busDetails['website'] = website
        except:
            busDetails['website'] = 'Failed'

        try:
            otherdetsStart = list(find_all(dets, "</a>',"))
            otherdets = dets[otherdetsStart[-1] + 8:].split("', '")
        except:
            try:
                otherdetsStart = list(find_all(dets, '</table>'))
                otherdets = dets[otherdetsStart[-1] + 8:].split("', '")
            except:
                try:
                    math.isnan(dets)
                    pass
                except:
                    otherdets = dets.split("', '")

        for det in otherdets:
            try:
                label, value = det.split("': '")
                busDetails[label] = value
            except:
                continue

        busDetailsDf = busDetailsDf.append(busDetails, ignore_index = True)
    busDetailsDf.fillna(value = 'Failed', inplace = True)
    # busDetailsDf.to_csv(file[:-4] + 'busDetails')
    return busDetailsDf

# data = pd.read_csv('irrigation_bus_details.csv')
# data.fillna(value = 'Failed', inplace = True)
# lowSales = data[data['Annual Sales'] == 'Under $1 Mil']
#
# sales = data['Annual Sales']
# lowSales = [c for c in sales if c[0] == 'U' or c[0] == 'N']


def getStateDf(state, file = None, data = None):
    if file != None:
        data = pd.read_csv(file)
    addressDf = addressSplitting(data = data)
    stateAddDf = addressDf[addressDf['state'] == state]
    stateDf = data.iloc[stateAddDf.index, :]
    return stateDf


def getSalesRange(salesRange, file = None, data = None):
    if file != None:
        data = pd.read_csv(file)
    print(data)
    sys.exit()
    busDetailDf = busDetailSplitting(data = data)
    print(busDetailDf)
    sys.exit()
    salesRangeDf = busDetailDf[busDetailDf['Annual Sales'] == salesRange]
    salesDf = data.iloc[salesRangeDf.index, :]
    return salesDf


def caLowSales(file):
    # stateDf = addressSplitting(file = file)
    # busDetailDf = busDetailSplitting(file = file)
    # stateFilter = stateDf[stateDf['state'] == 'CA'].index

    data = pd.read_csv(file)

    salesFilter1 = data[data['det_Annual Sales'] == 'Not Available'].index.tolist()
    salesFilter2 = data[data['det_Annual Sales'] == 'Under $1 Mil'].index.tolist()
    salesFilter3 = data[data['det_Annual Sales'] == '$1 - 4.9 Mil'].index.tolist()
    stateFilter = data[data['state'] == 'CA'].index.tolist()

    bothFilters = [c for c in stateFilter if c in pd.Series(salesFilter1+salesFilter2+salesFilter3).unique()]
    finalDf = pd.read_csv(file).iloc[bothFilters, :]
    return finalDf

df = pd.read_csv('agriculture_data/CALowSales.csv')



def addBusDetails(category:str, file: str) -> pd.DataFrame:
    filepath = f'{category}_data/{file}.csv'
    data = pd.read_csv(filepath)
    busDetailDf = busDetailSplitting(file = filepath)
    addressDf = addressSplitting(filepath)
    for col in busDetailDf.columns:
        data['det_'+col] = busDetailDf[col]
    for col in addressDf.columns:
        data[col] = addressDf[col]
    data.drop('bus_details', axis = 1, inplace = True)
    data.to_csv(f'{category}_data/{file}full.csv', index = False)

