#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : conftest.py                                                        #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Sunday, 5th January 2020 4:20:48 am                           #
# Last Modified: Monday, 6th January 2020 4:15:48 pm                           #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
# %%
import os
from pathlib import Path
import site
PROJECT_DIR = Path(__file__).resolve().parents[0]
site.addsitedir(PROJECT_DIR)
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

import numpy as np
from pytest import fixture

from src.data.data_classes import DataCollection, DataSet

@fixture(scope="function")
def get_dataset():
    ds = DataSet(name='test_dataset')
    filename = "./tests/data/san_francisco.csv"
    ds.import_data(filename)
    return ds



    