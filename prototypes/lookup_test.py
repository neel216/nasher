#!/usr/bin/env python3
# coding: utf-8
'''
This file contains functions to read the cleaned data Nasher provided us by returning information about a
specific painting (based on object number) or about a specific rack (based on rack number and letter)

TODO: functions for other rack information (what rack has the most paintings, what rack has the most space)
'''

import pandas as pd
import numpy as np
import re
pd.set_option('display.max_colwidth', None)

dimensions = pd.read_csv('data/dimensionsCleaned.csv')
del dimensions['Unnamed: 0']
locations = pd.read_csv('data/locationsCleaned.csv')
del locations['Unnamed: 0']

def get_rows(df, col, val):
    '''
    Returns the rows of a dataframe (df) that have a certain value (val)
    in the cell of a certain column (col)
    '''
    return df.loc[df[col] == val]

def get_info(objectID):
    '''
    Takes a string parameter (objectID) and returns a list of dictionaries
    containing information about the painting(s) with that object number

    TODO: handle .A, .B, etc. letters at end of objectID by deleting them?
    '''
    if len(objectID.split('.')) == 2:
        objectNumber = objectID + '.1'
    else:
        objectNumber = objectID
    
    dims = get_rows(dimensions, 'objectID', objectNumber)
    if len(dims) == 0:
        dims_ = 'Object Number not found'
    else:
        dims_ = [dims['width'].item(), dims['height'].item(), dims['depth'].item()]
    
    loc = get_rows(locations, 'objectID', objectNumber)
    items = []
    for i in loc.iterrows():
        room = i[1]['room']
        locationType = i[1]['locationType']
        locationLetter = i[1]['locationLetter'] if type(i[1]['locationLetter']) != type(np.nan) else ''
        try:
            location = f'{int(i[1]["locationID"])}{locationLetter}'
        except ValueError:
            location = 'unknown'
        artist = i[1]['artist']
        otherInfo = i[1]['info']

        info = {
            'objectID': objectNumber,
            'artist': artist,
            'room': room,
            'locationType': locationType,
            'location': location,
            'dimensions': dims_,
            'otherInfo': otherInfo
        }
        items.append(info)
    return items

def to_string(data):
    '''
    Takes a dictionary containing information about a painting and returns it in a readable
    string format
    '''
    if data['dimensions'] == 'Object Number not found':
        dimensions_ = 'unknown'
    else:
        dimensions = data['dimensions']
        dimensions_ = ' x '.join(str(d) for d in dimensions)
    objectID = data['objectID']
    artist = data['artist']
    room = data['room']
    locationType = data['locationType']
    location = data['location']
    other = data['otherInfo']

    ret = f'Object {objectID} by {artist} is stored in {room} on {locationType} {location}.\nTitle/Info: {other}\nDimensions (cm): {dimensions_}'
    return ret

def get_rack(rackID):
    '''
    Takes a string parameter (rackID) and returns a list of dictionaries describing
    the painting(s) on that rack
    '''
    if len(rackID) == 3:
        rackNumber = int(rackID[:-1])
        rackLetter = rackID[-1]
    elif len(rackID) == 2 and len(''.join(re.findall('[a-zA-Z]+', rackID))) == 1:
        rackNumber = int(rackID[0])
        rackLetter = rackID[-1]
    else:
        rackNumber = int(rackID)
        rackLetter = np.nan
        
    loc_ = get_rows(locations, 'locationID', rackNumber)
    loc__ = loc_.loc[loc_['locationLetter'] == rackLetter] if type(rackLetter) == type('A') else loc_.loc[loc_['locationLetter'] != 'A'].loc[loc_['locationLetter'] != 'B']
    
    items = []
    for painting in loc__['objectID']:
        for i in get_info(painting):
            items.append(i)
    
    return items
    
    
if __name__ == '__main__':
    number = '2015.2'
    for i in get_info(number):
        print(to_string(i), '\n')

    print('\n')

    for i in get_rack('62J'):
        print(to_string(i), '\n')