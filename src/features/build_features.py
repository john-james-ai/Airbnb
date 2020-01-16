#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : build_features.py                                                 #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Saturday, January 4th 2020, 6:56:37 pm                      #
# Last Modified : Thursday, January 16th 2020, 6:38:01 am                     #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #


OMIT_COLUMNS = ["listing_url",
                "scrape_id",
                "name",
                "summary",
                "space",
                "description",
                "amenities",
                "neighborhood_overview",
                "notes",
                "transit",
                "access",
                "interaction",
                "house_rules",
                "thumbnail_url",
                "medium_url",
                "picture_url",
                "xl_picture_url",
                "host_url",
                "host_name",
                "host_about",
                "availability_60",
                "availability_90",
                "availability_365",
                "host_acceptance_rate",
                "host_picture_url",
                "neighbourhood",
                "neighbourhood_group_cleansed",
                "smart_location",
                "country_code",
                "country",
                "latitude",
                "longitude",
                "minimum_minimum_nights",
                "maximum_minimum_nights",
                "minimum_maximum_nights",
                "maximum_maximum_nights",
                "minimum_nights_avg_ntm",
                "maximum_nights_avg_ntm",
                "has_availability",
                "calendar_last_scraped",
                "first_review",
                "last_review",
                "license",
                "jurisdiction_names"]

def select_features():
    """Selects features for quantitative analysis."""

def transform_categorical_features():
    """Converts categorical features to binary features."""