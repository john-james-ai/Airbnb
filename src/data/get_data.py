#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project: Airbnb                                                             #
# Version: 0.1.0                                                              #
# File: \get_data.py                                                          #
# Python Version: 3.8.0                                                       #
# ---------------                                                             #
# Author: John James                                                          #
# Company: Decision Scients                                                   #
# Email: jjames@decisionscients.com                                           #
# ---------------                                                             #
# Create Date: Saturday January 4th 2020, 7:13:14 pm                          #
# Last Modified: Sunday January 5th 2020, 3:52:44 pm                          #
# Modified By: John James (jjames@decisionscients.com)                        #
# ---------------                                                             #
# License: Modified BSD                                                       #
# Copyright (c) 2020 Decision Scients                                         #
# =========================================================================== #
#                               GET DATA                                      #
# =========================================================================== #
"""Downloads the Airbnb from the Inside Airbnb site 
(http://insideairbnb.com/get-the-data.html). Data has been made available
under the Creative Commons CC0 1.0 Universal (CC0 1.0) 
"Public Domain Dedication" license. 

This script downloads the web page into html, extracts the file names 
for the files containing listing information for the United States, then
downloads the files by filename."""

import os
import re
import requests

airbnb_listings = "../../airbnb.txt"
directory = "../../data/raw/" 
# def clean_directory():
#     filelist = [f for f in os.listdir(directory)]
#     for f in filelist:
#         os.remove(os.path.join(directory, f))
        
def get_listings():
    listings = []
    with open(airbnb_listings, encoding="utf8") as file:        
        for line in file:
            if "/data/listings.csv.gz" in line and 'states' in line:
                urls = re.search(r"(?P<url>https?://[^\s]+)", line).group("url")
                listings.append(urls)
    return listings

def download_listings(listings):
    for listing in listings:
        # Extract city and format filename
        city = listing.split("/")[5]
        date = listing.split("/")[6]
        filename = city + "_" + date + ".gz"        
        path = directory + filename
        # Create response object
        print("Downloading {filename}.".format(filename=filename))
        r = requests.get(listing, stream=True)
        if r.status_code == 200:
            # Start the download
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            print("Downloaded {filename}".format(filename=path))
        else:
            print(r.status_code)

    print("Downloads complete!")
    return 

if __name__ == "__main__":

    # Get a listings
    
    listings = get_listings()
    print(listings[0:10])
    download_listings(listings)

