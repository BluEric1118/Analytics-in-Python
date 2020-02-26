#Demonstration the following scenarios:
#   1) Simple bar/hist/scatter plot
#   2) Group by variables when creating plot
#   3) Add title and change plot size

import numpy as np

# <start> import data
def read_311_data(datafile):
    import pandas as pd
    import numpy as np
    
    #Add the fix_zip function
    def fix_zip(input_zip):
        try:
            input_zip = int(float(input_zip))
        except:
            try:
                input_zip = int(input_zip.split('-')[0])
            except:
                return np.NaN
        if input_zip < 10000 or input_zip > 19999:
            return np.NaN
        return str(input_zip)
    
    #Read the file
    df = pd.read_csv(datafile,index_col='Unique Key')
    
    #fix the zip
    df['Incident Zip'] = df['Incident Zip'].apply(fix_zip)
    
    #drop all rows that have any nans in them (note the easier syntax!)
    
    df = df.dropna(how='any')
    
    #get rid of unspecified boroughs
    df = df[df['Borough'] != 'Unspecified']
    
    #Convert times to datetime and create a processing time column
    
    import datetime
    df['Created Date'] = df['Created Date'].apply(lambda x:datetime.datetime.strptime(x,'%m/%d/%Y %I:%M:%S %p'))
    df['Closed Date'] = df['Closed Date'].apply(lambda x:datetime.datetime.strptime(x,'%m/%d/%Y %I:%M:%S %p'))
    df['processing_time'] =  df['Closed Date'] - df['Created Date']
    
    #Finally, get rid of negative processing times and return the final data frame
    
    df = df[df['processing_time']>=datetime.timedelta(0,0,0)]
    
    return df

datafile = "nyc_311_data_subset-2.csv"
data = read_311_data(datafile)

# <end> import data

#Group data by borough and plot a bar chart of the incident count (one variable)
borough_group = data.groupby('Borough')
#kind can be 'hist', 'scatter'
borough_group.size().plot(kind='bar')

#Group data by borough and plot a bar chart of the incident count (two variables)
agency_borough = data.groupby(['Agency','Borough'])
# using unstack() to categorized, increase the size of the image and add a title
agency_borough.size().unstack().plot(kind='bar',title="Incidents in each Agency by Borough",figsize=(15,12))

#convert the timedelta processing_time into floats for calculation purposes
data['float_time'] =data['processing_time'].apply(lambda x:x/np.timedelta64(1, 'D'))

grouped = data[['float_time','Agency']].groupby('Agency')
grouped.mean().sort_values('float_time',ascending=False)

data['float_time'].hist(bins=50)