#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : constants.py                                                      #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Friday, January 17th 2020, 5:57:33 pm                       #
# Last Modified : Friday, January 17th 2020, 5:57:33 pm                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Module containing global constants."""
# %%
import logging
import os
import site
from pathlib import Path

from collections import defaultdict
import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
site.addsitedir(PROJECT_DIR)


class Constants():

    USECOLS = ["id", "host_id",
               "host_response_rate",
               "host_total_listings_count",
               "host_response_time",
               "host_neighbourhood",
               "host_since",
               "host_is_superhost",
               "host_location",
               "city",
               "zipcode",
               "state",
               "market",
               "neighbourhood_cleansed",
               "accommodates",
               "bed_type",
               "square_feet",
               "beds",
               "room_type",
               "bedrooms",
               "bathrooms",
               "guests_included",
               "property_type",
               "amenities",
               "is_business_travel_ready",
               "maximum_nights",
               "availability_30",
               "minimum_nights",
               "experiences_offered",
               "cleaning_fee",
               "extra_people",
               "price",
               "security_deposit",
               "cancellation_policy",
               "review_scores_cleanliness",
               "review_scores_location",
               "review_scores_communication",
               "review_scores_accuracy",
               "review_scores_rating",
               "review_scores_checkin",
               "number_of_reviews_ltm",
               "reviews_per_month",
               "review_scores_value",
               "license",
               "host_verifications",
               "require_guest_phone_verification",
               "require_guest_profile_picture",
               "host_identity_verified",
               "instant_bookable",
               "requires_license",
               "host_has_profile_pic",
               "last_scraped",
               "calculated_host_listings_count_entire_homes",
               "calculated_host_listings_count_private_rooms",
               "calculated_host_listings_count_shared_rooms",
               "reviews_per_month"]


        DTYPES = ['BOOL': ["experiences_offered",
                        "host_has_profile_pic",
                        "host_identity_verified",
                        "host_in_town",
                        "instant_bookable",
                        "is_business_travel_ready",
                        "require_guest_profile_picture",
                        "requires_license"],
                'CATEGORY': ["bed_type",
                        "cancellation_policy",
                        "city",
                        "host_is_superhost",
                        "host_neighbourhood",
                        "host_verifications",
                        "license",
                        "market",
                        "neighbourhood_cleansed",
                        "property_type",
                        "require_guest_phone_verification",
                        "room_type",
                        "state"]
                'DATETIME': ["last_scraped",],
                'FLOAT': ["bathrooms",
                        "bedrooms",
                        "beds",
                        "cleaning_fee",
                        "extra_people",
                        "host_response_rate",
                        "host_total_listings_count",
                        "monthly_earnings",
                        "monthly_earnings_current",
                        "occupancy_rate",
                        "price",
                        "review_scores_accuracy",
                        "review_scores_checkin",
                        "review_scores_cleanliness",
                        "review_scores_communication",
                        "review_scores_location",
                        "review_scores_rating",
                        "review_scores_value",
                        "reviews_per_month",
                        "security_deposit",
                        "square_feet"],
                        "accommodates",
                'INT': ["availability_30",
                        "guests_included",
                        "host_id",
                        "host_since",
                        "id",
                        "maximum_nights",
                        "minimum_nights",
                        "month",
                        "number_of_reviews_ltm",
                        "year"],
                'OBJECT': ["amenities",
                        "host_location",
                        "host_response_time",
                        "zipcode"]}

    SFO = {'2016': os.path.join(PROJECT_DIR, "data/raw/san-francisco/2016/"),
           '2017': os.path.join(PROJECT_DIR, "data/raw/san-francisco/2017/"),
           '2018': os.path.join(PROJECT_DIR, "data/raw/san-francisco/2018/"),
           '2019': os.path.join(PROJECT_DIR, "data/raw/san-francisco/2019/")}

    DIRECTORY_STAGED = os.path.join(PROJECT_DIR, "data/staged/san-francisco/")
    DIRECTORY_INTERIM = os.path.join(
        PROJECT_DIR, "data/interim/san-francisco/")
    DIRECTORY_PROCESSED = os.path.join(
        PROJECT_DIR, "data/processed/san-francisco/")


