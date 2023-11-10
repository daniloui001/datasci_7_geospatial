#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install geopandas


# In[ ]:


import requests
import pandas as pd
from geopy.geocoders import GoogleV3
import urllib.parse
import geopandas as gpd


# In[ ]:


csv_file = "https://raw.githubusercontent.com/hantswilliams/HHA_507_2023/3ccdc2b145a6cc291ca8f4cf45486575d3d97886/WK7/assignment7_slim_hospital_addresses.csv"
df = pd.read_csv(csv_file)

# In[ ]:


api_key = ''

# In[ ]:


google_response = []
geolocator = GoogleV3(api_key=api_key)

# In[ ]:


for index, row in df.iterrows():
    city = row['CITY']
    state = row['STATE']
    address = f"{city}, {state}"
    if index >= 100:
        break

    try:
        location = geolocator.geocode(address)
        if location:
            lat_response = location.latitude
            lng_response = location.longitude
            final = {'address': address, 'lat': lat_response, 'lon': lng_response}
            google_response.append(final)
            print(f'Geocoded {address}')
        else:
            print(f'Geocoding failed for {address}')
    except Exception as e:
        print(f'Error while geocoding {address}: {str(e)}')

# In[ ]:


df1 = pd.DataFrame(google_response)

# In[ ]:


reverse_geocoded_data = []

# In[ ]:


dflat = pd.read_csv("https://raw.githubusercontent.com/hantswilliams/HHA_507_2023/3ccdc2b145a6cc291ca8f4cf45486575d3d97886/WK7/assignment7_slim_hospital_coordinates.csv")

# In[ ]:


for index, row in dflat.iterrows():
    latitude = row['X']
    longitude = row['Y']
    if index >= 100:
        break

    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.address
            final = {'lat': latitude, 'lon': longitude, 'address': address}
            reverse_geocoded_data.append(final)
            print(f'Reverse geocoded: {address}')
        else:
            print(f'Reverse geocoding failed for coordinates ({latitude}, {longitude})')
    except Exception as e:
        print(f'Error while reverse geocoding coordinates ({latitude}, {longitude}): {str(e)}')

# In[ ]:


df2 = pd.DataFrame(reverse_geocoded_data)
