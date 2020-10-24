#!/usr/bin/env python3
# coding: utf-8
'''
TODO: functions for other rack information (what rack has the most paintings, what rack has the most space)
'''
import pandas as pd
import numpy as np
import re


class Lookup:
    '''
    Contains functions to read the cleaned data Nasher provided us by returning information about a
    specific painting (based on object number) or about a specific rack (based on rack number and letter)
    '''
    def __init__(self, dim_path, loc_path):
        '''
        Constructs a Lookup object.

        :param dim_path: the path of the dimensions CSV file
        :param loc_path: the path of the locations CSV file
        :return: returns nothing
        '''
        pd.set_option('display.max_colwidth', None)

        self.dimensions = pd.read_csv(dim_path)
        self.locations = pd.read_csv(loc_path)
        del self.dimensions['Unnamed: 0']
        del self.locations['Unnamed: 0']

    def get_rows(self, df, col, val):
        '''
        Returns the rows of a dataframe that have a certain value
        in a certain column
        
        :param df: the dataframe to search
        :param col: the column to search in the dataframe
        :param val: the value to check for in the column
        :return: a dataframe containing the rows that have the value in the column
        '''
        return df.loc[df[col] == val]

    def get_info(self, objectID):
        '''
        Given a painting's object number, returns a list of dictionaries containing
        information about the painting(s) with that object number
        TODO: handle .A, .B, etc. letters at end of objectID by deleting them?

        :param objectID: a string that represents a painting's object number
        :return: an array of dictionaries containing information about the painting(s) with that object number
        '''
        if len(objectID.split('.')) == 2:
            objectNumber = objectID + '.1'
        else:
            objectNumber = objectID
        
        dims = self.get_rows(self.dimensions, 'objectID', objectNumber)
        if len(dims) == 0:
            dims_ = 'Object Number not found'
        else:
            dims_ = [dims['width'].item(), dims['height'].item(), dims['depth'].item()]
        
        loc = self.get_rows(self.locations, 'objectID', objectNumber)
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

    def to_string(self, data):
        '''
        Given a dictionary containing information about a painting, returns a string with that information

        :param data: a dictionary containing information about a painting
        :return: a string in a readable format describing a painting
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

    def get_rack(self, rackID):
        '''
        Takes a rackID and returns a list of dictionaries describing
        the painting(s) on that rack

        :param rackID: a string representing the ID of a rack (i.e. 3A, 27, 30B)
        :return: an array of dictionaries describing the painting(s) on that rack
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
            
        loc_ = self.get_rows(self.locations, 'locationID', rackNumber)
        if type(rackLetter) == type('A'):
            loc__ = loc_.loc[loc_['locationLetter'] == rackLetter]
        else:
            loc__ = loc_.loc[loc_['locationLetter'] != 'A'].loc[loc_['locationLetter'] != 'B']
        
        items = []
        for painting in loc__['objectID']:
            for i in self.get_info(painting):
                items.append(i)
        
        return items


if __name__ == '__main__':
    lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')

    number = '2015.2'
    for i in lookup.get_info(number):
        print(lookup.to_string(i), '\n')

    print('\n')

    for i in lookup.get_rack('62J'):
        print(lookup.to_string(i), '\n')