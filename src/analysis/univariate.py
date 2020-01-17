#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : Airbnb                                                             #
# Version : 0.1.0                                                              #
# File    : univariate.py                                                      #
# Python  : 3.8.0                                                              #
# ---------------------------------------------------------------------------- #
# Author : John James                                                          #
# Company: DecisionScients                                                     #
# Email  : jjames@decisionscients.com                                          #
# ---------------------------------------------------------------------------- #
# Created      : Sunday, 5th January 2020 5:35:06 pm                           #
# Last Modified: Monday, 6th January 2020 12:51:41 pm                          #
# Modified By  : John James (jjames@decisionscients.com>)                      #
# ---------------------------------------------------------------------------- #
# License: BSD                                                                 #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""This module contains the classes that perform univariate analyses."""
from abc import ABC, abstractmethod
from pathlib import Path
import site
PROJECT_DIR = Path(__file__).resolve().parents[1]
site.addsitedir(PROJECT_DIR)

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew, shapiro

# ---------------------------------------------------------------------------- #
#                             UNIVARIATE                                       #
# ---------------------------------------------------------------------------- #
class Univariate(ABC):
    """Base class for all univariate subclasses.
    
    Parameters
    ----------
    dataset : DataSet
              The DataSet object being analyzed
    
    """
    _NUMERICS = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']    
    def __init__(self):
        self._analysis = {}

    def reset(self):
        self._analysis = {}

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def get_analysis(self, attribute=None):
        pass

# ---------------------------------------------------------------------------- #
#                             DESCRIBE                                         #
# ---------------------------------------------------------------------------- #
class Describe(Univariate):
    """Computes descriptive statistics for a DataSet or DataCollection object.

    """
    def __init__(self):
        super(Describe, self).__init__()
        self._analysis = {}
        
    def _describe_quant(self, df):
        """Computes descriptive statistics for numeric attributes."""        
        
        a = df.describe(percentiles=[.05,.1,.25,.5,.75,.9,.95],
                        include=np.number)
        a = a.T
        a['na'] = df.isna().sum()
        a['kurtosis'] = df.kurtosis(axis=0)
        a['skew'] = df.skew(axis=0)
        
        a = a[['count', 'na', 'min', '5%', '10%', '25%', '50%', 'mean', 
               '75%', '90%', '95%', 'max', 'std', 'kurtosis', 'skew']]
        
        return a

    def _describe_qual(self, df):
        """Computes descriptive statistics for qualitative variables."""
        
        a = df.describe(include=np.object)
        a = a.T
        a['na'] = df.isnull().sum().T
        a = a[['count', 'na', 'unique', 'top', 'freq']]
        return a

    def fit(self, data):
        """Fits the analysis to the DataFrame or DataSet object."""            
        
        # Obtain the data from the DataSet or DataCollection
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = data.get_data()
        
        # Analyze numerics   
        quant_analysis = self._describe_quant(df)

        # Analyze categoricals
        qual_analysis = self._describe_qual(df)

        # Package results
        self._analysis['quant'] = quant_analysis
        self._analysis['qual'] = qual_analysis

        return self
    
    def get_analysis(self):
        """Returns the analysis from the fit method."""
        return self._analysis

      


                



        


