from lookup import Lookup
from sheets import Sheet

lookup = Lookup('data/dimensionsCleaned.csv', 'data/locationsCleaned.csv')
sheet = Sheet('1cU243sy8jJz91GATvx_TfjWqdklvTCkbnQKEqDF3T8I', 'TMS Changes!A1:C1000')




# Menu to allow use to choose what to do
choice = input("a. Change a painting's location\nb. Lookup a painting\nc. Lookup a rack\nd. Scan a rack\ne. Add a painting\n")




# Would get objectID from OCR here
objectID = '2014.15.2' # would normally get this from OCR





# Check if number is correct and manual override if it isn't correct
choice = input(f'Is {objectID} correct? [y/n] ')
print('\n')
if choice == 'n':
    objectID = input('Enter the correct objectID. ')
    print('\n')





# Check if lookup result is correct
c = 1
paintings = lookup.get_info(objectID)
for i in paintings:
    print(str(c) + '.', lookup.to_string(i), '\n')

choice = input('Select a painting. ')
print('\n')
painting = paintings[int(choice) - 1]



# Enter new location
print(f"Old Location: {painting['room']}, {painting['location']}")
new_room = input('Enter new room (i.e. Nasher Painting Storage Room, Off-site) (enter "same" if the room is not changing): ')
if new_room.lower() == 'same':
    new_room = painting['room']
new_loc = ''
if new_room.lower() != 'off-site':
    new_loc = input('Enter new location (i.e. 48A, 27, 3B): ')

print(f"New location: {new_room}, {new_loc}")
sheet.add_rows([[painting['objectID'], painting['artist'], painting['otherInfo'], painting['room'] + ', ' + painting['location'], new_room + ', ' + new_loc]])
# update local data


# get number from ocr
# check if the number is correct & manual override
# check if the lookup result is correct
# enter new location
# update google sheet
# update local data