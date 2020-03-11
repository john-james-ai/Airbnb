#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : format.py                                                         #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 14th 2020, 4:28:43 am                      #
# Last Modified : Friday, February 14th 2020, 4:28:43 am                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Functions used to format data."""
import re
import random
import string
import textwrap

def proper(s):
    """Strips then capitalizes each word in a string.""" 
    s = s.replace("-", " ").title()
    s = s.replace("_", " ").title()
    return s    

def snake(s):
    """Converts string to snake case suitable for filenames."""
    s = re.sub(r"[^a-zA-Z0-9._// ]+", '', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    s = s.replace(" ", "_")
    pattern = '_' + '{2,}'
    s = re.sub(pattern, '_', s)
    return s

def format_text(x):
    x = " ".join(x.split())
    formatted = textwrap.fill(textwrap.dedent(x))
    return formatted        

def scale_number(num, suffix="B"):
    """
    Scale a number such as bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if num < factor:
            return f"{num:.2f}{unit}{suffix}"
        num /= factor