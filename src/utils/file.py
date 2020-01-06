#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : file.py                                                            #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Monday, 6th January 2020 12:05:12 am                          #
# Last Modified: Monday, 6th January 2020 4:53:11 pm                           #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""Classes for reading and writing to files."""
from abc import ABC, abstractmethod
import os
import pandas as pd

class BaseFile(ABC):
    """Abstract base class for performing file i/o."""

    def __init__(self):
        pass

    @abstractmethod
    def read(self, filename):
        pass

    @abstractmethod
    def write(self, filename):
        pass
# ---------------------------------------------------------------------------- #
#                               FileGZ                                         #  
# ---------------------------------------------------------------------------- #
class FileGZ(BaseFile):
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
        df.to_csv(filename, compression='gzip')
        return self
        
# ---------------------------------------------------------------------------- #
#                               FileCSV                                        #  
# ---------------------------------------------------------------------------- #
class FileCSV(BaseFile):
    """Read and write CSV files and returning DataFrames."""

    def __init__(self):
        pass

    def read(self, filename):
        """Reads a .csv file, designated by 'filename' into a DataFrame.
        
        Parameters
        ----------
        filename : str
            The relative or fully qualified file path

        Returns
        -------
        DataFrame : The file contents in DataFrame format.
        
        """

        self._filename = filename
        df = pd.read_csv(filename)
        return df

    def write(self, filename, df):
        """Accepts a filename and a DataFrame and writes it to a .csv file.
        
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
        df.to_csv(filename)
        return self
        
# ---------------------------------------------------------------------------- #
#                                FILE                                          #   
# ---------------------------------------------------------------------------- #
class File:
    """Wrapper for File* objects."""
    _FILE_HANDLERS = {'gz': FileGZ(), 'csv': FileCSV()}

    def __init__(self):
        pass
        
    def _get_file_handler(self, filename):
        file_ext = filename.split(".")[-1]
        file_handler = self._FILE_HANDLERS.get(file_ext)
        if file_handler is None:
            raise Exception("{ext} files are not supported.".format(ext=file_ext))        
        else:
            return file_handler

    def read(self, filename):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(filename)
        return file_handler.read(filename)

    def write(self, filename, df):
        """Obtains a file handler based upon the file extension, then reads.""" 
        file_handler = self._get_file_handler(filename)
        return file_handler.write(filename, df)