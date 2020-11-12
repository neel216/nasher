#!/usr/bin/env python
# coding: utf-8

# In[131]:


import pandas as pd
import numpy as np
pd.set_option('display.max_colwidth', None)


# In[132]:


dimensions = pd.read_csv('dimensions.csv', header=None)
dimensions


# In[134]:


del dimensions[0]
dimensions


# In[135]:


for i in dimensions[1]:
    if i != 'Public-Facing Dimension Label Text':
        print('all values are not the same')
# All values in this column are the same, therefore we can delete it


# In[136]:


del dimensions[1]
dimensions


# In[137]:


dimensions.columns = ['objectID', 'dimensions']
dimensions['width'] = np.nan
dimensions['height'] = np.nan
dimensions['depth'] = np.nan
dimensions


# In[138]:


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


# In[139]:


dimensions


# In[140]:


dimensions.info()


# In[141]:


#dimensions.to_csv('dimensionsCleaned.csv')


# In[199]:


locations = pd.read_csv('locations.csv', header=None)
locations


# In[200]:


locations.info()


# In[201]:


locations.insert(1, 'room', np.nan)
del locations[1]
del locations[4]
locations


# In[202]:


locations.insert(3, 'locationID', np.nan)
locations.insert(4, 'locationLetter', np.nan)
locations


# In[203]:


locations.columns = ['objectID', 'room', 'locationType', 'locationID', 'locationLetter', 'artist', 'info']
locations


# In[204]:


index = 0
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


# In[205]:


locations


# In[206]:


#locations.to_csv('locationsCleaned.csv')


# In[207]:


locations.info()


# In[ ]:




