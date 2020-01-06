#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#==============================================================================#
# File: file.py                                                                #
# Project: data                                                                #
# Created: Monday, 6th January 2020 12:05:12 am                                #
# Author: John James (jjames@decisionscients.com)                              #
# -----                                                                        #
# Last Modified: Monday, 6th January 2020 12:28:27 am                          #
# Modified By: John James (jjames@decisionscients.com>)                        #
# -----                                                                        #
# Copyright 2020 - 2020 DecisionScients                                        #
#==============================================================================#
"""Classes for reading and writing to files."""
from abc import ABC, abstractmethod
import os
import pandas as pd

class File(ABC):
    """Abstract base class for performing file i/o."""

    def __init__(self):
        pass

    @abstractmethod
    def read(self, filename):
        pass

    @abstractmethod
    def write(self, filename):
        pass

class FileGZDF(File):
    """Read and write compressed GZ files and returning DataFrames."""

    def __init__(self):
        pass

    def read(self, filename):
        """Reads a .gz file, designated by 'filename' into a DataFrame.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path

        Returns
        -------
        DataFrame : The file contents in DataFrame format.
        
        """

        self._filename = filename
        df = pd.read_csv(filename, compression='gzip', error_bad_lines=False,
                        low_memory=False)
        return df

    def write(self, filename, df):
        """Accepts a filename and a DataFrame and writes it to a .gz file.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path
        df : DataFrame
            The DataFrame object to be written to file.

        Returns
        -------
        self
        
        """

        self._filename = filename
        self._df = df
        df.to_csv(filename, compression='gzip', error_bad_lines=False,
                        low_memory=False)
        return self
        
    def remove(self, filename):
        """Removes a file.

        Parameters
        ----------
        filename : str
            The relative or fully qualified file path.
        """
        os.remove(filename)
        return self
