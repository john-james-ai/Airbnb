#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : print.py                                                          #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/airbnb                         #
# --------------------------------------------------------------------------- #
# Created       : Monday, March 9th 2020, 5:38:55 am                          #
# Last Modified : Monday, March 9th 2020, 5:39:07 am                          #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Print utilities."""
import math
import statistics
from tabulate import tabulate
# --------------------------------------------------------------------------- #
#                                Print                                        #
# --------------------------------------------------------------------------- #
class Printer:
    """ Formats and prints simple dataframes and dictionaries."""

    def __init__(self, line_length = 80, title_separator='='):
        self._line_length = min(line_length,80)
        self._default_anchor_pos = int(math.floor(self._line_length / 2))
        self._default_anchor_style = ":"
        self._default_anchor_lhs_pad = 1
        self._default_anchor_rhs_pad = 1     
        self._title_separator = title_separator   

    def _compute_budgets(self, anchor):
        """Computes available space on left and right sides."""
        anchor['lhs_budget'] = anchor['pos'] - anchor['lhs_pad'] 
        anchor['rhs_budget'] = self._line_length - anchor['rhs_pad'] -\
             anchor['pos'] 
        return anchor
    
    def _set_anchor(self, content):
        """Sets vertical anchor point for text alignment."""

        # Initialize anchor, padding and budget with default values
        anchor = {}
        anchor['style'] = self._default_anchor_style
        anchor['pos'] = self._default_anchor_pos
        anchor['lhs_pad'] = self._default_anchor_lhs_pad
        anchor['rhs_pad'] = self._default_anchor_rhs_pad  
        # Compute budgets given default anchor position
        anchor = self._compute_budgets(anchor)    

        # Get line lengths from content
        lhs_lens = [len(str(k)) for k in content.keys()]
        rhs_lens = [len(str(v)) for v in content.values()]    

        # If all lengths are within budget return self._anchor_pos
        if max(lhs_lens) <= anchor['lhs_budget'] and \
           max(rhs_lens) <= anchor['rhs_budget']:
           return anchor

        # Otherwise adjust anchor by 1/2 (avg_rhs - avg_lhs)
        lhs_avg_len = statistics.mean(lhs_lens)
        rhs_avg_len = statistics.mean(rhs_lens)
        anchor['pos'] -= math.floor(1/2 * (rhs_avg_len - lhs_avg_len))
        # Adjust the budgets for lhs and rhs accordingly
        anchor = self._compute_budgets(anchor)

        return anchor    


    def _print_title(self, title):
        """Prints title and title separator"""
        if not isinstance(self._line_length, (int, float)):
            raise TypeError("Invalid line length. Must be an integer or float.")
        title_separator = self._title_separator * len(title)
        print("\n")
        print(title.center(self._line_length))
        print(title_separator.center(self._line_length))

    def _print_line(self, anchor, k, v):
        lhs_pad = ' ' * (anchor['pos'] - anchor['lhs_pad'] - len(str(k)))
        line = lhs_pad + str(k) + ' '*anchor['lhs_pad'] + anchor['style'] + \
            ' '*anchor['rhs_pad'] + str(v)
        print(line)


    def print_dictionary(self, content, title=None):
        """Pretty prints a title and dictionary or table."""
        anchor = self._set_anchor(content) 
        if title:
            self._print_title(title)
        for k, v in content.items():
            self._print_line(anchor, k,v)

    def print_table(self, content, title=None):
        """Prints a table with a heading.

        Note: To use the tabulate package, content must be a dictionary and 
        each key must be an iterable.

        Parameters
        ----------
        title : str
            The title to be printed above the table
        content : dict of lists
            Dictionary in which the values are iterables.
        """
        if title:
            self._print_title(title)
        print(tabulate(content, headers='keys'))

        
