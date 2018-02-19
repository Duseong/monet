from __future__ import print_function
import os
import pandas as pd
import numpy as np
import datetime

def getdegrees(degrees, minutes, seconds):
        return degrees+ minutes/60.0 + seconds/3600.00


def lbs2kg(lbs):
    kg = 0.453592 * lbs
    return kg

class CEMSEmissions(object):
    """Class for data from continuous emission monitoring systems (CEMS).
       Data from power plants can be downloaded from ftp://newftp.epa.gov/DMDNLoad/emissions/"""

    def __init__(self):
      self.efile = None   
      self.url = "ftp://newftp.epa.gov/DmDnLoad/emissions/"
      self.lb2kg = 0.453592  #number of kilograms per pound.
      self.info = "Data from continuous emission monitoring systems (CEMS) \n"
      self.info += self.url + '\n'
      self.df = None

    def __str__(self):
        return self.info

    def get_data(self, rdate, states=['md']):
        """gets the ftp url from the retrieve method and then 
           loads the data from the ftp site using the load method.
           TO DO add loop for adding multiple months.
        """
        if isinstance(states, str):
           states = [states] 
        for st in states:
            url = self.retrieve(rdate, st, download=False)
            self.load(url)


    def get_var(self, varname, loc=None, daterange=None):
        """returns time series with variable indicated by varname.
           TO DO filter for specified dates.
           TO DO filter for specified location."""
        columns =  list(self.df.columns.values)
        #temp = self.df['OP_DATE', 'OP_HOUR', 'OP_TIME']
        #print(temp[0:10])
        for ccc in columns:
            print(ccc)
            #if varname.lower() is in ccc.lower():
        return ccc               

    def retrieve(self, rdate, state, download=True):
        """rdate - datetime object. Uses year and month. Day and hour are not used.
           state - state abbreviation to retrieve data for
           Files are by year month and state.
        """
        import wget
        efile = 'empty'
        ftpsite = self.url
        ftpsite += 'hourly/'
        ftpsite += 'monthly/'
        ftpsite +=  rdate.strftime("%Y") + '/'
        fname = rdate.strftime("%Y") + state + rdate.strftime("%m") + '.zip'
        if not download:
           return ftpsite + fname
        if not os.path.isfile(fname):
            print('retrieving ' + ftpsite + fname) 
            efile = wget.download(ftpsite + fname)
            print('retrieved ' + ftpsite + fname) 
        else:
            print('file exists ' + fname)
            efile = fname
        self.info += 'File retrieved :' +  efile + '\n'
        return efile

    def get_location(self, name):
        """Need to create a comprehensive dictionary for all locations in the US."""
        lhash = {}
        lhash[314] = (39.1785, -76.5269) #Herbert A Wagner
        lhash[110]   = (getdegrees(39,10,53), getdegrees(-76,32,16)) #brandon shores
        lhash[312]   = (getdegrees(39,19,25), getdegrees(-76,21,59)) #CP Crane
        lhash[322]   = (getdegrees(38,32,37), getdegrees(-76,41,19)) #chalk point
        lhash[323]   = (getdegrees(39,12,36), getdegrees(-77,27,54)) #dickerson
        lhash[324]   = (getdegrees(38,21,33), getdegrees(-76,58,36)) #morgantown
        lhash[1116]   = (getdegrees(39,35,46), getdegrees(-78,44,46)) #warrier run
        lhash[1229]   = (38.670, -76.865) #brandywine
        lhash[316]   = (29.238,-76.5119) #perryman

    def load(self, efile, verbose=True):
        """loads information found in efile into a pandas dataframe.
        """
        dftemp = pd.read_csv(efile)
        columns = list(dftemp.columns.values)
        ckeep=[]
        for ccc in columns:
            #print( dftemp[ccc].unique())
            if 'so2' in ccc.lower():
                ckeep.append(ccc) 
            elif 'time' in ccc.lower():
                ckeep.append(ccc) 
            elif 'date' in ccc.lower():
                ckeep.append(ccc) 
            elif 'hour' in ccc.lower():
                ckeep.append(ccc) 
            elif 'name' in ccc.lower():
                ckeep.append(ccc) 
            elif 'id' in ccc.lower():
                ckeep.append(ccc) 
            elif 'btu' in ccc.lower():
                ckeep.append(ccc) 
        dftemp = dftemp[ckeep]
        cnan = ['SO2_MASS (lbs)']
        ##drop rows with NaN in the cnan column.
        dftemp.dropna(axis=0,  inplace=True, subset=cnan)
        #print(dftemp['FACILITY_NAME'].unique())
        #print(dftemp['FAC_ID'].unique())
        pairs = zip(dftemp['FAC_ID'], dftemp['FACILITY_NAME'])
        pairs = list(set(pairs))
        #print(pairs)
        self.namehash = dict(pairs)  #key is facility id and value is name.

        ##create column with datetime information from column with month-day-year and column with hour.
        dftime = dftemp.apply(lambda x:pd.datetime.strptime("{0} {1}".format(x['OP_DATE'], x['OP_HOUR'])  , "%m-%d-%Y %H"), axis=1) 
        dftemp = pd.concat([dftime, dftemp], axis=1) 
        dftemp.rename(columns={0:'date'}, inplace=True)
        dftemp.drop(['OP_DATE', 'OP_HOUR'], axis=1, inplace=True)

        if self.df is None:
            self.df = dftemp
            if verbose: print('Initializing pandas dataframe. Loading ' + efile)
        else:
            self.df.append(dftemp)        
            if verbose: print('Appending to pandas dataframe. Loading ' + efile)
        return dftemp
        
