#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : make_dataset.py                                                   #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Wednesday, January 8th 2020, 12:49:32 pm                    #
# Last Modified : Thursday, January 16th 2020, 6:32:35 am                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #

"""Downloads the Airbnb from the Inside Airbnb site 
(http://insideairbnb.com/get-the-data.html). Data has been made available
under the Creative Commons CC0 1.0 Universal (CC0 1.0) 
"Public Domain Dedication" license. 
"""
import click
import logging
import os
from pathlib import Path
import re
import requests

from bs4 import BeautifulSoup

def get_data(project_dir,year, market):
    """Downloads data into raw data directory."""
    
    logger = logging.getLogger(__name__)
    logger.info('downloading data into raw data directory')

    # point to output directory
    url = "http://insideairbnb.com/get-the-data.html"
    mbyte=1024*1024

    print('Reading: ', url)
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    print('Processing: ', url)
    for name in soup.findAll('a', href=True):
        zipurl = name['href']
        directory = ""
        raw_data_dir = os.path.join(project_dir, "data/raw/")
        if( zipurl.endswith('listings.csv.gz') and market in zipurl and year in zipurl):     
            city =  zipurl.split("/")[5]          
            parts = zipurl.split("/")[4:9]   
            filename = '_'.join(parts) 
            directory = os.path.join(raw_data_dir, city).replace("\\", "/")
            os.makedirs(directory, exist_ok=True)
            filepath = os.path.join(directory, filename).replace("\\", "/")        
            if os.path.exists(filepath):
                print("%s already downloaded" % filepath)
            else:
                r = requests.get(zipurl, stream=True)
                if( r.status_code == requests.codes.ok ) :
                    fsize = int(r.headers['content-length'])
                    print('Downloading %s (%sMb)' % ( filepath, fsize/mbyte ))
                    with open(filepath, 'wb') as fd:
                        for chunk in r.iter_content(chunk_size=1024): # chuck size can be larger
                            if chunk: # ignore keep-alive requests
                                fd.write(chunk)
                        fd.close()
@click.command()
@click.argument('market')
@click.argument('year')
def main(market, year):
    # Obtains the root directory for the project.
    project_dir = Path(__file__).resolve().parents[2]
    get_data(project_dir, year, market)    

if __name__ == "__main__":

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()