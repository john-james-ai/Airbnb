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
    def __init__(self, dataset):
        self._dataset = dataset
        self._analysis = {}
        self._fit = False

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
    """Computes descriptive statistics for a DataSet object.

    Parameters
    ----------
    dataset : DataSet
              The DataSet object being analyzed.

    """
    def __init__(self, dataset):
        super(Describe, self).__init__(dataset=dataset)
        self._analysis_quant = {}
        self._analysis_qual = {}

    def _reset(self):
        self._analysis = {}
        self._analysis_quant = {}
        self._analysis_qual = {}
        self._fit = False
        
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

    def fit(self):
        """Fits the analysis to the data."""        
        self._reset()

        self._analysis['name'] = self._dataset.name

        df = self._dataset.get_data()        
        
        # Analyze numerics   
        self._analysis['quant'] = self._describe_quant(df)

        # Analyze categoricals
        self._analysis['qual'] = self._describe_qual(df)

        self._fit = True

        return self
    
    def get_analysis(self, attribute=None):
        """Returns the complete analysis or that of a specific attribute."""
        if not self._fit:
            raise Exception("The analysis has not been fit to the DataSet object.")
        if attribute:
            if attribute == 'quant':
                return self._analysis['quant']
            elif attribute== 'qual':
                return self._analysis['qual']
            else:
                analysis = \
                    self._analysis['quant'].get(key=attribute, default=None) or \
                    self._analysis['qual'].get(key=attribute, default=None)
                if analysis:
                    return analysis
                else:
                    raise AttributeError("{attr} is not a valid attribute for\
                        the DataSet object.".format(attr=attribute))            
        else:
            return self._analysis

      


                



        


