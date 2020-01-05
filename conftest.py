#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project: Visualence                                                         #
# Version: 0.1.0                                                              #
# File: \conftest.py                                                          #
# Python Version: 3.8.0                                                       #
# ---------------                                                             #
# Author: John James                                                          #
# Company: Decision Scients                                                   #
# Email: jjames@decisionscients.com                                           #
# ---------------                                                             #
# Create Date: Tuesday December 31st 2019, 7:10:48 pm                         #
# Last Modified: Wednesday January 1st 2020, 10:31:40 am                      #
# Modified By: John James (jjames@decisionscients.com)                        #
# ---------------                                                             #
# License: Modified BSD                                                       #
# Copyright (c) 2019 Decision Scients                                         #
# =========================================================================== #
# %%
import numpy as np
from pytest import fixture
import warnings
warnings.filterwarnings('ignore')
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

from visualence.canvas.base import Canvas 
from visualence.canvas.title import CanvasTitle
@fixture(scope="session")
def create_canvas():
    canvas = Canvas()
    return canvas

@fixture(scope='session')
def create_canvas_component():
    component = CanvasTitle()
    return component
    