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
from scipy.stats import kurtosis, skew
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
        
    def _describe_quant(self, x):
        """Computes descriptive statistics for numeric attributes."""        
        d = {}
        a = x.describe()
        d['count'] = a[0]
        d['na'] = x.isna().sum()
        d['min'] = a[3]
        d['5%'] = x.quantile(q=0.05)
        d['10%'] = x.quantile(q=0.1)
        d['25%'] = a[4]
        d['50%'] = a[5]
        d['mean'] = a[1]
        d['mode'] = x.mode()
        d['75%'] = a[6]
        d['90%'] = x.quantile(q=0.9)
        d['95%'] = x.quantile(q=0.95)
        d['max'] = a[7]
        d['std'] = a[2]
        d['kurtosis'] = kurtosis(x)
        d['skew'] = skew(x)
        return d

    def _describe_qual(self, x):
        """Computes descriptive statistics for qualitative variables."""
        d = {}
        a = x.describe()    
        d['count'] = a[0]
        d['na'] = pd.isnull(x)
        d['unique'] = a[1]
        d['top'] = a[2]
        d['freq'] = a[3]
        return d

    def fit(self):
        """Fits the analysis to the data."""        
        self._reset()

        self._analysis['name'] = self._dataset.name

        df = self._dataset.get_data()        
        
        # Analyze numerics
        df_quant = df.select_dtypes(include=self._NUMERICS)
        for col in df_quant.columns:
            self._analysis_quant[col] = self._describe_quant(df_quant[col])
        self._analysis['quant'] = self._analysis_quant

        # Analyze categoricals
        df_qual =  df.select_dtypes(exclude=self._NUMERICS)
        for col in df_qual.columns:
            self._analysis_qual[col] = self._describe_qual(df_qual[col])
        self._analysis['qual'] = self._analysis_qual

        self._fit = True

        return self

    def get_analysis(self, attribute=None):
        """Returns the complete analysis or that of a specific attribute."""
        if not self._fit:
            raise Exception("The analysis has not been fit to the DataSet object.")
        if attribute:
            if attribute == 'quant':
                return self._analysis_quant
            elif attribute== 'qual':
                return self._analysis_qual
            else:
                analysis = self._analysis_quant.get(attribute) or \
                    self._analysis_qual.get(attribute)
                if analysis:
                    return analysis
                else:
                    raise AttributeError("{attr} is not a valid attribute for\
                        the DataSet object.".format(attr=attribute))            
        else:
            return self._analysis

      


                



        


