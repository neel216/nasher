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

        self.dim_path = dim_path
        self.dimensions = pd.read_csv(dim_path)
        self.loc_path = loc_path
        self.locations = pd.read_csv(loc_path)
        del self.dimensions['Unnamed: 0']
        del self.locations['Unnamed: 0']

    def get_rows_contains(self, df, col, val):
        '''
        Returns the rows of a dataframe that have contain a value
        in a certain column
        
        :param df: the dataframe to search
        :param col: the column to search in the dataframe
        :param val: the value to check for in the column
        :return: a dataframe containing the rows that have the value in the column
        '''
        return df[df[col].str.contains(val)]
    
    def get_rows_exact(self, df, col, val):
        '''
        Returns the rows of a dataframe that have have a value
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

        :param objectID: string that represents a painting's object number
        :return: an array of dictionaries containing information about the painting(s) with that object number
        '''
        if len(objectID.split('.')) == 2:
            objectNumber = objectID + '.1'
        else:
            objectNumber = objectID
        
        dims = self.get_rows_contains(self.dimensions, 'objectID', objectNumber)
        _dims = {}
        if len(dims) == 0:
            dims_ = 'Object Number not found'
        else:
            for i in dims.iterrows():
                _dims[i[1]['objectID']] = [i[1]['width'], i[1]['height'], i[1]['depth']]

        loc = self.get_rows_contains(self.locations, 'objectID', objectNumber)
        items = []
        for i in loc.iterrows():
            index = i[0]
            room = i[1]['room']
            locationType = i[1]['locationType']
            locationLetter = i[1]['locationLetter'] if type(i[1]['locationLetter']) != type(np.nan) else ''
            try:
                location = f'{int(i[1]["locationID"])}{locationLetter}'
            except ValueError:
                location = 'unknown'
            try:
                dims_ = _dims[i[1]['objectID']]
            except KeyError:
                dims_ = 'Object Number not found'
            artist = i[1]['artist']
            otherInfo = i[1]['info']

            info = {
                'index': index,
                'objectID': i[1]['objectID'],
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

        :param data: dictionary containing information about a painting
        :return: string in a readable format describing a painting
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

        :param rackID: string representing the ID of a rack (i.e. 3A, 27, 30B)
        :return: array of dictionaries describing the painting(s) on that rack
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
            
        loc_ = self.get_rows_exact(self.locations, 'locationID', rackNumber)
        if type(rackLetter) == type('A'):
            loc__ = loc_.loc[loc_['locationLetter'] == rackLetter]
        else:
            loc__ = loc_.loc[loc_['locationLetter'] != 'A'].loc[loc_['locationLetter'] != 'B']
        
        items = []
        for painting in loc__['objectID']:
            for i in self.get_info(painting):
                items.append(i)
        
        return items

    def edit_location(self, index, new_room, rackID):
        '''
        Given the index of a row in the locations dataframe, changes the room
        and locationID and locationLetter to the locations given

        :param index: integer to index the dataframe
        :param new_room: string to replace the old room value
        :param rackID: string to replace the locationID and locationLetter
        :return: returns nothing useful
        '''
        if len(rackID) == 3:
            rackNumber = float(rackID[:-1])
            rackLetter = rackID[-1]
        elif len(rackID) == 2 and len(''.join(re.findall('[a-zA-Z]+', rackID))) == 1:
            rackNumber = float(rackID[0])
            rackLetter = rackID[-1]
        else:
            rackNumber = float(rackID)
            rackLetter = np.nan

        self.locations.iloc[index, self.locations.columns.get_loc('room')] = new_room
        self.locations.iloc[index, self.locations.columns.get_loc('locationID')] = rackNumber
        self.locations.iloc[index, self.locations.columns.get_loc('locationLetter')] = rackLetter

        self.refresh_csv()
        return True
    
    def add_painting(self, objectID, room, locationType, rackID, artist, title_and_year, dims):
        '''
        Adds a painting with the given information to the database

        :param objectID: the object number of the new painting (string)
        :param room: the room the new painting is being stored in (string)
        :param locationType: the type of screen the painting is being stored on
        :param rackID: the rack number and rack letter the painting is being stored on
        :param artist: the author of the painting
        :param title_and_year: the title of the painting, and the year the painting was made (separated by a comma and space)
        :param dimensions: an array with 3 float numbers describing the width, height, and depth of the painting in centimeters
        :return: returns nothing useful
        '''
        if len(rackID) == 3:
            rackNumber = float(rackID[:-1])
            rackLetter = rackID[-1]
        elif len(rackID) == 2 and len(''.join(re.findall('[a-zA-Z]+', rackID))) == 1:
            rackNumber = float(rackID[0])
            rackLetter = rackID[-1]
        else:
            rackNumber = float(rackID)
            rackLetter = np.nan
        
        dims_ = ' x '.join(str(d) for d in dims) + ' cm'
        width = dims[0]
        height = dims[1]
        depth = dims[2]

        self.locations.loc[len(self.locations.index)] = [objectID, room, locationType, rackNumber, rackLetter, artist, title_and_year]
        self.dimensions.loc[len(self.dimensions.index)] = [objectID, dims_, width, height, depth]
        self.refresh_csv()
        return True

    def refresh_csv(self):
        '''
        Overrides the existing CSVs to ensure data is saved if program is stopped

        :return: returns nothing useful
        '''
        self.locations.to_csv(self.loc_path)
        self.dimensions.to_csv(self.dim_path)
        return True

if __name__ == '__main__':
    lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')

    number = '2003.4.3'
    for i in lookup.get_info(number):
        print(lookup.to_string(i), '\n')

    print('\n')

    for i in lookup.get_rack('46B'):
        print(lookup.to_string(i), '\n')