from lookup import Lookup
from sheets import Sheet
import camera_integrate1
from os import execv


def change_location():
    # Would get objectID from OCR here
    objectID = '2014.15.2' # would normally get this from OCR




    # Check if number is correct and manual entry if it isn't correct
    choice = input(f'Is {objectID} correct? [y/n] ')
    print('\n')
    if choice == 'n':
        objectID = input('Enter the correct object number: ')
        print('\n')

    # Allow user to select painting from lookup results
    c = 1
    paintings = lookup.get_info(objectID)
    for i in paintings:
        print(str(c) + '.', lookup.to_string(i), '\n')
        c += 1
    choice = input('Select a painting. ')
    print('\n')
    painting = paintings[int(choice) - 1]

    # Enter new location for painting
    print(f"Old Location: {painting['room']}, {painting['location']}")
    new_room = input('Enter new room (i.e. Nasher Painting Storage Room, Off-site) (enter "same" if the room is not changing): ')
    if new_room.lower() == 'same':
        new_room = painting['room']
    new_loc = ''
    if new_room.lower() != 'off-site':
        new_loc = input('Enter new location (i.e. 48A, 27, 3B): ')
    print(f"New location: {new_room}, {new_loc}")

    # update google sheets
    sheet.add_rows([[painting['objectID'], painting['artist'], painting['otherInfo'], painting['room'] + ', ' + painting['location'], new_room + ', ' + new_loc]])

    # update local data
    lookup.edit_location(painting['index'], new_room, new_loc)

def lookup_painting():
    objectID = input('Enter an object number: ')
    print('\n')

    c = 1
    paintings = lookup.get_info(objectID)
    for i in paintings:
        print(str(c) + '.', lookup.to_string(i), '\n')
        c += 1

def lookup_rack():
    rack = input('Enter a rack number/ID (i.e. 48A, 27): ')
    print('\n')

    c = 1
    for i in lookup.get_rack(rack):
        print(str(c) + '.', lookup.to_string(i), '\n')
        c += 1

def scan_rack():
    # execv("camera_transform.py", [])
    # camera_transform.run()
    camera_integrate1.run()
    #print("test")
    # fork("camera_transform.py")
    # print("test")

def add_painting():
    objectID = input('What is the object number of the new painting? ')
    room = input('What room will the painting be stored in? ')
    locationType = input('What kind of rack will the painting be stored on (i.e. Screen, Wall Screen)? ')
    rackID = input('What rack will the painting be stored on (i.e. 48A, 27)? ')
    author = input('Who is the author of the painting? ')
    title_and_year = input('What is the title and the year of the painting (separate with a comma and space)? ')
    width = float(input('What is the width of the painting (in cm)? '))
    height = float(input('What is the height of the painting (in cm)? '))
    depth = float(input('What is the depth of the painting (in cm)? '))
    dims = [width, height, depth]

    sheet.add_rows([[objectID, author, title_and_year + '\nDimensions: ' + ' x '.join(str(d) for d in dims) + ' cm', '', room + ', ' + locationType + ' ' + rackID]])
    lookup.add_painting(objectID, room, locationType, rackID, author, title_and_year, dims)
    print('Painting added to database.')


lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')
sheet = Sheet('1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I', 'TMS Changes!A1:C')


# Menu to allow user to choose what to do
choice = input("a. Change a painting's location\nb. Lookup a painting\nc. Lookup a rack\nd. Scan a rack\ne. Add a painting\n")

if choice == 'a':
    change_location()
elif choice == 'b':
    lookup_painting()
elif choice == 'c':
    lookup_rack()
elif choice == 'd':
    scan_rack()
elif choice == 'e':
    add_painting()

