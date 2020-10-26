from lookup import Lookup
from sheets import Sheet


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

def add_painting():
    pass


lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')
sheet = Sheet('1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I', 'TMS Changes!A1:C1000')


# Menu to allow user to choose what to do
choice = input("a. Change a painting's location\nb. Lookup a painting\nc. Lookup a rack\nd. Scan a rack\ne. Add a painting\n")

if choice == 'a':
    change_location()
elif choice == 'b':
    lookup_painting()
elif choice == 'c':
    lookup_rack()
elif choice == 'd':
    pass # image recognition stuff would get called here
elif choice == 'e':
    add_painting()

