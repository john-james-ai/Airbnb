#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : test_file.py                                                       #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Monday, 6th January 2020 4:37:31 pm                           #
# Last Modified: Monday, 6th January 2020 4:37:31 pm                           #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""Tests the file class."""
import os

import pytest
from pytest import mark

from src.data.data_classes import File

class FileTests:

    @mark.file
    @mark.file_validation
    def test_file_validation(self):        
        filename = "tests/data/san_francisco.csv.xlsx"
        f = File()
        with pytest.raises(Exception):
            _ = f.read(filename)

    @mark.file
    @mark.file_gz
    def test_file_gz(self):
        # Test read
        filename = "./tests/data/san_francisco.csv.gz"
        f = File()
        df = f.read(filename)
        assert len(df) > 0, "gz read failed"
        # Test write
        filename = "./tests/data/san_francisco2.csv.gz"
        f.write(filename, df)
        assert os.path.exists(filename), "gz write failed"

    @mark.file
    @mark.file_csv
    def test_file_csv(self):
        # Get dataframe data
        filename = "./tests/data/san_francisco.csv.gz"
        f = File()
        df = f.read(filename)        
        # Test write
        filename = "./tests/data/san_francisco.csv"
        f = File()
        df = f.write(filename, df)
        assert os.path.exists(filename), "csv write failed"
        # Test read
        filename = "./tests/data/san_francisco.csv"
        df = f.read(filename)
        assert len(df) > 0, "csv read failed."
