# Manasi Pemmareddy
# Homework P3
#Help On Assignment: Bryan and Edward

import pandas as pd
import numpy as np

def chemprofile(filename, datasheet='dataset', sheetname='bosheet', filters=None):
    """This program is about being able to manipulate set of excel data sheet
    identify certain sets of data in the excel sheet and find certain statistic on them.
    The input consists of the file location of the of the Hansen Chemical data Sheet, 
    what you want to name the first sheet of excel workbook, the name of the second sheet
    and the filters to help select certain portions of the excel data to do the stats on"""

    df=pd.read_excel(filename, index_col='CAS_ID')
    dfc=df #creates a copy of the orginal data, so that the orginal can be manipulated
  
    if filters != None: #"!=" means not equal to
        for k in filters: #scrolls to each tag in dict (filter inputs are going to be read as dict)
            if k in df.columns.tolist() and k not in ['SMILES','CAS_ID']:
                if filters[k][0] != None: #sees whether or not k is equal to None, if it isn't do the following below
                    df=df[df.loc[:,k] >= filters[k][0]]
                    
                if filters[k][1] != None:
                    df=df[df.loc[:,k] <= filters[k][1]]    
    
    BF=df.describe() #gives a table (called BF) with the following stats: mean, std, min, max, median, 25%,75% quantiles
    BF.loc['Kurtosis',:]=df.kurtosis(axis=0) #adding the kurtosis data into the BF table
    BF.loc['Skewness',:]=df.skew(axis=0) 
    BF.loc['5%',:]=df.quantile(q=0.05, axis=0, numeric_only=True) #adding the percentile data into the BF table
    BF.loc['10%',:]=df.quantile(q=0.1, axis=0, numeric_only=True)
    BF.loc['90%',:]=df.quantile(q=0.9, axis=0, numeric_only=True)
    BF.loc['95%',:]=df.quantile(q=0.95, axis=0, numeric_only=True)
    BF.index = ['N', 'mean', 'std dev', 'min', 'max','median', 'skewness', 'kurtosis', '5%','10%','25%','75%','90%','95%'] #Restructure BF table
    writer = pd.ExcelWriter(filename) #creates excel fil
    dfc.to_excel(writer, sheet_name = datasheet) #in the excel sheet, we arent removing any data, we still want the excel sheet to have the original data on the first sheet
    BF.to_excel(writer, sheet_name = sheetname) #the second sheet has the stats of the FILTERED data
    writer.save()
    writer.close()   

    return 

#df=chemprofile('C:/Users/Manasi/Desktop/College/Senior Yr (2017-2018)/Fall 2018/Model and Simulation/Homework/Hansen chemical dataset.xlsx',filters= {'MW': (50, 400), 'LogP': (-2.0, 6.5)})
