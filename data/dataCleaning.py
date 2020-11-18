#!/usr/bin/env python
# coding: utf-8
'''
Given CSV files for location and dimensions data from the Nasher Museum of Art's TMS Database,
this file cleans the data and downloads it as cleaned CSV files
'''
import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', None)


dimensions = pd.read_csv('dimensions.csv', header=None) # Read in dirty dimensions data
del dimensions[0] # delete the index column

# Determine if all values in the second column are the same
for i in dimensions[1]:
    if i != 'Public-Facing Dimension Label Text':
        print('all values are not the same')
# All values in this column are the same, therefore we can delete it
del dimensions[1]

# Rename columns and create new columns with NaN values
dimensions.columns = ['objectID', 'dimensions']
dimensions['width'] = np.nan
dimensions['height'] = np.nan
dimensions['depth'] = np.nan

# Clean dimensions data
for i in dimensions['dimensions']:
    dims = []
    print('----', i, '-----')
    if type(i) == type(4.0):
        dims = 'is a NaN'
        dimensions['dimensions'] = dimensions['dimensions'].replace(i, np.nan)
        continue
    elif i[-1] != ')':
        if len(i.split('(')) == 2:
            dims = i.split('(')[-1][:i.split('(')[-1].find(')')]
            dims = dims.split(' ')
            dims = [float(dims[0]), float(dims[2])]
        else:
            if i == 'dimensions variable':
                dimensions['dimensions'] = dimensions['dimensions'].replace(i, np.nan)
                dims = 'Getting rid of "dimensions variable"'
                continue
            elif len(i.split()) == 6:
                dims = i.split()
                if dims[1] == '¾':
                    dims[1] = 0.75
                if dims[4] == '¼':
                    dims[4] = 0.25
                if dims[1] == '5/8':
                    dims[1] = 0.625
                if dims[4] == '5/8':
                    dims[4] = 0.625
                dims = [round((int(dims[0]) + dims[1]) * 2.54, 1), round((int(dims[3]) + dims[4]) * 2.54, 1)]
            elif len(i.split()) == 5:
                dims = i.split()
                if dims[3] == '¼':
                    dims[3] = 0.25
                dims = [round(int(dims[0]) * 2.54, 1), round((int(dims[2]) + dims[3]) * 2.54, 1)]
            else:
                dims = i[i.index('(') + 1:i.index(')')].split()
                if len(dims) == 4:
                    dims = [float(dims[0]), float(dims[2])]
                else:
                    dims = [float(dims[0]), float(dims[2]), float(dims[4])]
    elif 'frame' in i.lower():
        dims = i[i.lower().index('frame'):]
        dims = dims[dims.index('(') + 1:dims.index(')')].split()
        if len(dims) == 4:
            dims = [float(dims[0]), float(dims[2])]
        elif len(dims) == 6:
            dims = [float(dims[0]), float(dims[2]), float(dims[4])]
    else:
        dims = i[i.index('(') + 1: i.index(')')].split()
        if len(dims) == 4:
            dims = [float(dims[0]), float(dims[2])]
        elif len(dims) == 6:
            dims = [float(dims[0]), float(dims[2]), float(dims[4])]
    try:
        if dims != 'is a NaN' and dims != 'Getting rid of "dimensions variable"' and type(dims[0]) != type(4.0):
            if len(dims) == 2 and dims[1] == 'cm':
                dims = [float(dims[0]), np.nan]
            if len(dims) == 2 and dims[1] == 'frame':
                dims = i[i.index('Frame (Each frame):') + len('Frame (Each frame):'):]
                dims = dims[dims.index('(') + 1:-1]
                dims = dims.split()
                dims = [float(dims[0]), float(dims[2])]
            if dims[0] == 'Individual' or dims[0] == 'diameter':
                dims = i[i.index('inches'):]
                dims = dims[dims.index('(') + 1:dims.index(')')]
                dims = dims.split()
                if len(dims) == 2:
                    dims = [float(dims[0]), np.nan]
                if len(dims) == 4:
                    dims = [float(dims[0]), float(dims[2])]
                if len(dims) == 6:
                    dims = [float(dims[0]), float(dims[2]), float(dims[4])]
            if dims[0] == '.A':
                dims = [81.3, 76.2, 35.6]
            if dims[0] == 'closed':
                dims = [33.0, 50.8]
            if len(dims) == 8:
                dims = [float(dims[0]), float(dims[2]), float(dims[4])]
    except IndexError:
        dims = i[i.index('inches'):]
        dims = dims[dims.index('(') + 1:dims.index(')')]
        dims = dims.split()
        dims = [float(dims[0]), float(dims[2]), float(dims[4])]
    if len(dims) == 2:
        dims = [dims[0], dims[1], np.nan]
    print(dims)
    dimensions['width'][dimensions.index[dimensions['dimensions'] == i].tolist()[0]] = dims[0]
    dimensions['height'][dimensions.index[dimensions['dimensions'] == i].tolist()[0]] = dims[1]
    dimensions['depth'][dimensions.index[dimensions['dimensions'] == i].tolist()[0]] = dims[2]
    print(dimensions.index[dimensions['dimensions'] == i].tolist()[0])
    dimensions['dimensions'][dimensions.index[dimensions['dimensions'] == i].tolist()[0]] = ' x '.join(map(str, dims)) + ' cm'

# Look at summary of information in dimensions dataframe
dimensions.info()

# Download dimensions dataframe to CSV
#dimensions.to_csv('dimensionsCleaned.csv')




locations = pd.read_csv('locations.csv', header=None) # Read in dirty locations data

# Insert new column with NaN values and delete unnecessary columns
locations.insert(1, 'room', np.nan)
del locations[1]
del locations[4]

# Insert new columns with NaN values
locations.insert(3, 'locationID', np.nan)
locations.insert(4, 'locationLetter', np.nan)

# Rename column names
locations.columns = ['objectID', 'room', 'locationType', 'locationID', 'locationLetter', 'artist', 'info']


index = 0
# Clean locations data
for i in locations['locationType']:
    if pd.notnull(i):
        loc = i.split(', ')
        if len(loc) == 4:
            rackID = np.nan
            rackLetter = np.nan
            if len(loc[3]) == 3:
                rackID = int(loc[3][:-1])
                rackLetter = loc[3][-1]
            elif len(loc[3]) == 2:
                rackID = int(loc[3])
            loc = [loc[1], loc[2], rackID, rackLetter]
        elif len(loc) == 5:
            rackID = np.nan
            rackLetter = np.nan
            if len(loc[3]) == 3:
                rackID = int(loc[3][:-1])
                rackLetter = loc[3][-1]
            elif len(loc[3]) == 2:
                rackID = int(loc[3])
            loc = [loc[1], loc[2], rackID, rackLetter]
        elif len(loc) == 2:
            loc = [loc[1], np.nan, np.nan, np.nan]
        elif len(loc) == 3:
            loc = [loc[1], loc[2], np.nan, np.nan]
    else:
        loc = [np.nan, np.nan, np.nan, np.nan]
    print(i)
    locations['room'][index] = loc[0]
    locations['locationType'][index] = loc[1]
    locations['locationLetter'][index] = loc[3]
    locations['locationID'][index] = loc[2]
    index += 1

# Look at summary of information in locations dataframe
locations.info()

# Download locations data to CSV
#locations.to_csv('locationsCleaned.csv')



