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
        # Read in dataframes from the given paths
        self.dim_path = dim_path
        self.dimensions = pd.read_csv(dim_path)
        self.loc_path = loc_path
        self.locations = pd.read_csv(loc_path)

        # Removes the index column from each dataframe
        del self.dimensions['Unnamed: 0']
        del self.locations['Unnamed: 0']

    def get_rows_contains(self, df, col, val, _decimals=True):
        '''
        Returns the rows of a dataframe that contain a value
        in a certain column
        
        :param df: the dataframe to search
        :param col: the column to search in the dataframe
        :param val: the value to check for in the column
        :return: a dataframe containing the rows that have the value in the column
        '''
        # If we want to compare numbers and their decimal points
        if _decimals:
            return df[df[col].str.contains(val)]
        # If we want to compare numbers without decimal points
        return df[df[col].str.replace('.', '').str.contains(val)]
    
    def get_rows_exact(self, df, col, val):
        '''
        Returns the rows of a dataframe that have an exact value
        in a certain column
        
        :param df: the dataframe to search
        :param col: the column to search in the dataframe
        :param val: the value to check for in the column
        :return: a dataframe containing the rows that have the value in the column
        '''
        return df.loc[df[col] == val]
    
    def get_info(self, objectID, decimals=True):
        '''
        Given a painting's object number, returns a list of dictionaries containing
        information about the painting(s) with that object number

        :param objectID: string that represents a painting's object number
        :return: an array of dictionaries containing information about the painting(s) with that object number
        '''
        objectNumber = objectID
        
        # Get rows in dimensions dataframe that contain the object id
        dims = self.get_rows_contains(self.dimensions, 'objectID', objectNumber, _decimals=decimals)
        _dims = {}
        if len(dims) == 0:
            # The dimensions dataframe doesn't have the object id
            dims_ = 'Object Number not found'
        else:
            # Create a list with the basic dimensions info for each painting we found from the dimensions dataframe
            for i in dims.iterrows():
                _dims[i[1]['objectID']] = [i[1]['width'], i[1]['height'], i[1]['depth']]

        # Get rows in locations dataframe that contain the object id
        loc = self.get_rows_contains(self.locations, 'objectID', objectNumber, _decimals=decimals)
        items = []

        # Create a list with the basic information from each painting we found in the locations dataframe
        for i in loc.iterrows():
            index = i[0] # Gets the index of the row in the dataframe for later reference
            room = i[1]['room'] # Get the "room" location of the painting
            locationType = i[1]['locationType'] # Get the location "type": Screen or Wall Screen
            # Determine if the screen has an A or B at the end of it
            locationLetter = i[1]['locationLetter'] if type(i[1]['locationLetter']) != type(np.nan) else ''
            # Determine if we actually know the location or not
            try:
                location = f'{int(i[1]["locationID"])}{locationLetter}'
            except ValueError:
                location = 'unknown'
            # Determine if we know the dimensions or not
            try:
                dims_ = _dims[i[1]['objectID']]
            except KeyError:
                dims_ = 'Object Number not found'
            artist = i[1]['artist'] # Get the artist's information
            otherInfo = i[1]['info'] # Get any other infromation about the painting

            # Put all of the information into a dictionary
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
            items.append(info) # Add the dictionary to the list of paintings that match the object ID
        return items

    def to_string(self, data):
        '''
        Given a dictionary containing information about a painting, returns a readable string with that information

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
        # Process rack ID string
        if len(rackID) == 3:
            # If the rack is formatted with a 2 digit number and a letter
            rackNumber = int(rackID[:-1])
            rackLetter = rackID[-1]
        elif len(rackID) == 2 and len(''.join(re.findall('[a-zA-Z]+', rackID))) == 1:
            # If the rack is formatted with a 1 digit number and a letter
            rackNumber = int(rackID[0])
            rackLetter = rackID[-1]
        else:
            # If the rack is formatted with a 2 digit number and no letter
            rackNumber = int(rackID)
            rackLetter = np.nan
        
        # Get the location of all paintings that are on the given rack
        loc_ = self.get_rows_exact(self.locations, 'locationID', rackNumber)
        if type(rackLetter) == type('A'):
            # If the given rack has a rack letter
            loc__ = loc_.loc[loc_['locationLetter'] == rackLetter]
        else:
            # If the given rack has no rack letter
            loc__ = loc_.loc[loc_['locationLetter'] != 'A'].loc[loc_['locationLetter'] != 'B']
        
        items = []
        # Put all of the paintings we found into a list of dictionaries describing each painting
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
        # Process rack ID string
        if len(rackID) == 3:
            # If the rack is formatted with a 2 digit number and a letter
            rackNumber = int(rackID[:-1])
            rackLetter = rackID[-1]
        elif len(rackID) == 2 and len(''.join(re.findall('[a-zA-Z]+', rackID))) == 1:
            # If the rack is formatted with a 1 digit number and a letter
            rackNumber = int(rackID[0])
            rackLetter = rackID[-1]
        else:
            # If the rack is formatted with a 2 digit number and no letter
            rackNumber = int(rackID)
            rackLetter = np.nan

        # Edit the value of the room
        self.locations.iloc[index, self.locations.columns.get_loc('room')] = new_room
        # Edit the value of the rack number
        self.locations.iloc[index, self.locations.columns.get_loc('locationID')] = rackNumber
        # Edit the value of the rack letter
        self.locations.iloc[index, self.locations.columns.get_loc('locationLetter')] = rackLetter

        self.refresh_csv() # Download the CSV so we save the data locally
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
        # Process rack ID string
        if len(rackID) == 3:
            # If the rack is formatted with a 2 digit number and a letter
            rackNumber = int(rackID[:-1])
            rackLetter = rackID[-1]
        elif len(rackID) == 2 and len(''.join(re.findall('[a-zA-Z]+', rackID))) == 1:
            # If the rack is formatted with a 1 digit number and a letter
            rackNumber = int(rackID[0])
            rackLetter = rackID[-1]
        else:
            # If the rack is formatted with a 2 digit number and no letter
            rackNumber = int(rackID)
            rackLetter = np.nan
        
        # Get dimensions into a readable string (_ x _ x _ cm)
        dims_ = ' x '.join(str(d) for d in dims) + ' cm'
        width = dims[0]
        height = dims[1]
        depth = dims[2]

        # Add the new painting to the locations dataframe
        self.locations.loc[len(self.locations.index)] = [objectID, room, locationType, rackNumber, rackLetter, artist, title_and_year]
        # Add the new painting to the dimensions dataframe
        self.dimensions.loc[len(self.dimensions.index)] = [objectID, dims_, width, height, depth]
        self.refresh_csv() # Download the CSV so we save the data locally
        return True

    def refresh_csv(self):
        '''
        Overrides the existing CSVs to ensure data is saved if program is stopped

        :return: returns nothing useful
        '''
        self.locations.to_csv(self.loc_path) # Override the locations CSV with the data from the location dataframe
        self.dimensions.to_csv(self.dim_path) # Override the dimensions CSV with the data from the dimensions dataframe
        return True
    
    def object_exists(self, objectID, decimals=True):
        '''
        Checks to see if a given object ID number exists in the locations database

        :param objectID: string that describes an object number
        :param decimals: whether to search the database with decimals in the object IDs or not
        :return: returns a boolean describing whether or not the given object ID is in the location database
        '''
        locationList = self.locations['objectID'].tolist() # Creates a list from the object ID column of the locations dataframe
        # Iterate over each painting in the list and check its object ID to see if it contains the given object ID
        for i in locationList:
            if decimals:
                if objectID in i:
                    # Return true if we found the painting
                    return True
            else:
                if objectID in i.replace('.', ''):
                    # Return true if we found the painting
                    return True
        return False # We didn't find the painting

if __name__ == '__main__':
    # Create a Lookup object
    lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')

    number = '2006711'
    # Print each painting found for the given number (searching without decimals)
    for i in lookup.get_info(number, decimals=False):
        print(lookup.to_string(i), '\n')

    print('\n')

    # Print each painting found for the given rack
    for i in lookup.get_rack('46B'):
        print(lookup.to_string(i), '\n')