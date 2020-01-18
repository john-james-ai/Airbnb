#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : stage_dataset.py                                                  #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Friday, January 17th 2020, 6:59:57 am                       #
# Last Modified : Friday, January 17th 2020, 7:00:42 am                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Preliminary cleaning and formatting prior to exploratory analysis."""
#%%
import logging
import os
import site
import sys
from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parents[2]
site.addsitedir(PROJECT_DIR)

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from src.data.data_classes import DataSet, DataCollection
from src.data.constants import Constants
from src.data.data_studio import TypeStudio

# --------------------------------------------------------------------------- #
#                               CLEAN MONEY                                   #
# --------------------------------------------------------------------------- #
def number_(dataset):

    """Ensures financial variables are typed float without special characters."""
    vars = [price,weekly_price, monthly_price,	security_deposit, 
            cleaning_fee,	extra_people]
    df = dataset.get_data()
    for var in vars:
        df[var] = df[var].str.replace(',', '')
        df[var] = df[var].str.replace('$', '')
        df[var] = df[var].str.replace('%', '')
    
    dataset.add(df)

    return dataset

# --------------------------------------------------------------------------- #
#                               ATTENDANT                                     #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
#                               DATA SERVER                                   #
# --------------------------------------------------------------------------- #
def serve_data():
    """Serves the data forward during the preliminary inspection."""
    
    for year, directory in Constants.SFO.items():
        
        for filename in os.listdir(directory):           
            
            name = "_".join(filename.split("_")[1:4])
            dataset = DataSet(name=name)
            dataset.import_data(os.path.join(directory, filename))
            dataset = number_rince(dataset)
            dataset = text_rince(dataset)
            dataset = type_cast(dataset)
            dataset = format_data(dataset)
            dataset = select_data(dataset)
            dataset = check_data(dataset)



# --------------------------------------------------------------------------- #
#                                 MAIN                                        #
# --------------------------------------------------------------------------- #
def main(input_filepath, output_filepath):
    """ Serves the raw data forward for pre-analysis inspection and formatting."""
    logger = logging.getLogger(__name__)
    logger.info('Preliminary pre-analysis data inspection and formatting.')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
