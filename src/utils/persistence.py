#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# File: persistence.py                                                         #
# Project: utils                                                               #
# Created: Monday, 6th January 2020 3:28:28 am                                 #
# Author: John James (jjames@decisionscients.com)                              #
# -----                                                                        #
# Last Modified: Monday, 6th January 2020 3:31:02 am                           #
# Modified By: John James (jjames@decisionscients.com>)                        #
# -----                                                                        #
# Copyright 2020 - 2020 DecisionScients                                        #
# ============================================================================ #

"""Class responsible for object persistence"""
import bz2
import pickle
# --------------------------------------------------------------------------- #
#                          PERSISTENCE CLASS                                  #
# --------------------------------------------------------------------------- #
class Persistence:

    def __init__(self):
        pass

    def serialize(self, instance, filename):
        sfile = bz2.BZ2File(filename, 'w')
        pickle.dump(instance, sfile)
        return self

    def deserialize(self, filename):
        infile = open(filename, 'rb')
        instance = pickle.load(infile, encoding='bytes') 
        return instance
