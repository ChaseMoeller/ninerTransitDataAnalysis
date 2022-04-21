#reads an excel sheet and puts it into a pandas data frame
#sorts columns by selection values
#Author: Jonathan Martinez

import pandas as pd
import numpy as np
from geopy import distance

#test variables
route1='Green'
route2='Silver'
route3='Gold'

#idk if these are the stop/cycle time labels
timeLabel1 = "on"
timeLabel2 = "off"

#some columns must be sorted together by request of transit services
choice1='Date&Time'
choice2='Lat/long&stopName'
choice3=route3
stopTimeLabel=timeLabel2
choice4='dont use'

#params for sorts, change to test sorts
param1=choice2
param2=True


#function parameters @selection takes a String column name, @ascending takes a Boolean
#TODO: finish working out the logic when the visuals are up
def sortColumns(selection, ascends):
    df = pd.read_excel('2018-2019 Stop Data PART 1.xlsx', engine='openpyxl')
    print("original df")
    print(df)
    #df

    #they might want time threshold... like view from a specific date to another date
    #TODO: fix if thats the case
    if selection == choice1:
        df = df.sort_values(["Date","Time"], ascending=(ascends, ascends))
        print("sorted by date and time data frame")
        print(df)
        #df

    #4m30s
    #TODO: implement sort by stop name selection, should significantly improve runtime.
    elif selection == choice2:
        #df = df.loc[(df['Stop'] == 'Martin Hall')]
        latLongSum = 0
        latLongMax = None
        #sets the max lat/long pair
        latLong = df[['Latitude', 'Longitude']].to_numpy()
        for i, elem in enumerate(latLong):
            prev = latLong[i-1][0] + latLong[i-1][1]
            latLongSum = latLong[i][0] + latLong[i][1]
            if latLongSum > prev:
                latLongMax = elem

        latLongDists = []
        #calculates lat/long distances
        #if nulls are found in data sets, then the distance is set null
        for i, elem in enumerate(latLong):
            if np.isnan(latLong[i][0]) or np.isnan(latLong[i][1]):
                latLongDists = np.append(latLongDists, [float("nan")])
            else:
                latLongDists = np.append(latLongDists, distance.distance(latLong[i], latLongMax).miles)

        #sorts Stop & lat/long columns in ascending orders
        df['Dists'] = latLongDists.tolist()
        df = df.sort_values(['Stop', 'Dists'], ascending=(ascends,ascends))

        #comment out line to view distances "df = df.drop(['Dists'], axis=1)"
        df = df.drop(['Dists'], axis=1)
        print("sorted by lat/long & stop name data frame")
        print(df)
        #df

    #30s
    #not sure what stoptimelabels are. 
    #sorts by route and "stopTimeLabel"
    #TODO: fix if needed, shouldn't have to, I really think the on/off is the stop time
    elif selection == choice3:
        print("sorted by route selection ?and stoptimeLabel? data frame")
        df = df.loc[(df['Route'] == choice3) & (df['On off'] == stopTimeLabel)]
        print(df)
        #df

    #Not sure what cycle time is
    #should sort similarly to stoptime and route
    #TODO: implement this
    elif selection == choice4:
        print("sorted by route selection ?and cycletimeLabel? data frame")
        df = df.loc[(df['Route'] == choice3) & (df['On off'] == 'on')]
        print(df)

sortColumns(param1, param2)

