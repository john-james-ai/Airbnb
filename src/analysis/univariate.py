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
from scipy.stats import kurtosis, skew, shapiro, kurtosistest, skewtest

# ---------------------------------------------------------------------------- #
#                              DESCRIBE                                        #
# ---------------------------------------------------------------------------- #
class Describe(ABC):
    """Base class for all univariate subclasses."""

    @abstractmethod
    def describe(self, data):
        pass

# ---------------------------------------------------------------------------- #
#                             DESCRIBEQUANT                                    #
# ---------------------------------------------------------------------------- #
class DescribeQuant(Describe):
    """Computes descriptive statistics for a quantitative variable.

    """
    def __init__(self):
        super(DescribeQuant, self).__init__()
        self._description = {}
        
    def describe(self, data):
        """Computes descriptive statistics for a quantitative variable.
        
        Parameters
        ----------
        data : array-like
            The univariate data to be analyzed.

        Returns
        -------
        description : dict
            Descriptive statistics including counts, percentiles, and 
            measures of location and scale.

        """     
        # Ensure only numeric columns are evaluated.
        data = data.select_dtypes([np.number])
        if data.empty:
            description = pd.DataFrame()
        else:
            cols = np.array(data.columns)
            # Compute basic descriptive statistics and round to 2 sig digits.        
            description = data.describe(percentiles=[0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95], include=np.number)   
            description = description.round(2)
            description = description.T
            # Add missing counts 
            d_missing = data.isnull().sum()
            d_missing = d_missing.rename('# Missing')
            # Add missing percentages
            d_pct_missing = round(data.isnull().sum() / len(data) * 100, 2)
            d_pct_missing = d_pct_missing.rename('% Missing')
            # Add Kurtosis
            d_kurtosis = data.kurtosis()
            d_kurtosis = d_kurtosis.rename('Kurtosis')
            # Add Skew
            d_skew = data.skew()
            d_skew = d_skew.rename('skew')
            # Concatenate pandas objects into dataframe
            description = pd.concat([description, d_missing, d_pct_missing, d_kurtosis, d_skew], axis=1)
            # Add Kurtosis test
            _, d_kurtosis_test = kurtosistest(data)
            description['Kurtosis p-value'] = pd.DataFrame(data=[d_kurtosis_test], columns=cols).T
            # Add Skew test
            _, d_skew_test = skewtest(data)
            description['Skew p-value'] = pd.DataFrame(data=[d_skew_test], columns=cols).T
            # Add shapiro
            df = data.apply(lambda x: pd.Series(shapiro(x), index=['w', 'Shapiro p-value'])).T
            description = pd.concat([description, df['Shapiro p-value']], axis=1)
        return description


# ---------------------------------------------------------------------------- #
#                             DESCRIBEQUANT                                    #
# ---------------------------------------------------------------------------- #
class DescribeQual(Describe):
    """Computes descriptive statistics for a qualitative variable.

    """
    def __init__(self):
        super(DescribeQual, self).__init__()
        self._description = {}
        
    def describe(self, data):
        """Computes descriptive statistics for a qualitative variable.
        
        Parameters
        ----------
        data : array-like
            The univariate data to be analyzed.

        Returns
        -------
        description : dict
            Descriptive statistics including counts, missing and unique 
            values.

        """        
        d = data.select_dtypes(exclude=np.number)
        if d.empty:
            description = pd.DataFrame()
        else:
            description = d.describe().T
        return description
                



        


