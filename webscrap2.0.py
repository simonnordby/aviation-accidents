#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:28:31 2023

@author: simonnordby
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 06:56:52 2023

@author: simonnordby
"""

import urllib
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "utf-8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0"
} 

data = []

# Function to get keys from the infobox. Used later.
def get_infobox_value(soup, name):
    for key in soup.find_all("th", {"class":"infobox-label"}):
        if name.lower() in key.text.lower():
            data = key.find_next_sibling("td")
            return data
    return None


for i in range(2022,2024):
    url = 'https://en.wikipedia.org/wiki/Category:Aviation_accidents_and_incidents_in_'+str(i)
    try:
        request = urllib.request.Request(url,None,headers)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response.read().decode('utf-8'),"html.parser")
        print('Working through '+str(i))
        
        category_links = soup.find("div", {"id":"mw-pages"}) #narrows down the area in the html file.
        crash_in_year = category_links.find_all("a",) #finds all links(a) in the area.
        crash_links = [ #list comprehention
            link.get("href")
            for link in crash_in_year
                ]
        for link in crash_links: #loops through every link.
            url = "https://en.wikipedia.org" + link #over writes old url   
            request = urllib.request.Request(url,None,headers)
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response.read().decode('utf-8'),"html.parser")
            infobox = soup.find("table", {"class":"infobox"}) 
            if infobox: #if there is an infobox in the link. 
                try: # Extracting data from infobox
                    date = get_infobox_value(infobox, "Date").text
                    
                    summary = get_infobox_value(infobox, "Summary")
                    
                    site = get_infobox_value(infobox, "Site")
                    location = site.find(string=True, recursive=False)#returns the first part of site                
                    latitude = site.find("span", {"class":"latitude"}).text
                    longitude = site.find("span", {"class":"longitude"}).text                
                    aircraft_type = get_infobox_value(infobox, "Aircraft type")
                    operator = get_infobox_value(infobox, "Operator").text
                    passengers = get_infobox_value(infobox, "Passengers").text
                    crew = get_infobox_value(infobox, "Crew").text
                    fatalities = get_infobox_value(infobox, "Fatalities").text
                    injuries = get_infobox_value(infobox, "Injuries").text
                    survivers = get_infobox_value(infobox, "Survivers").text
                    on_board = (survivers,crew, fatalities, injuries, survivers)
                    
                    data.append([date,summary,location,latitude,longitude,aircraft_type,operator,on_board])

                except AttributeError as e:
                    print(f'AttributeError: {e}')
    except urllib.error.HTTPError as e:
        print(f"Page from year {i} not found: {e}")
    except Exception as e:
        print(f'Error: {e}')
df = pd.DataFrame(data,columns = ['date', 'summary', 'location', 'latitude', 'longitude', 'aircraft-type', 'operator', 'on_board'])
df.to_csv('aviation_accidents.csv', index=False, encoding='utf-8')