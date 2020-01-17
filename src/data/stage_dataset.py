#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Airbnb                                                            #
# Version : 0.1.0                                                             #
# File    : stage_dataset.py                                                  #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# --------------------------------------------------------------------------- #
# Created       : Friday, January 17th 2020, 6:59:57 am                       #
# Last Modified : Friday, January 17th 2020, 7:00:42 am                       #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Preliminary cleaning and formatting prior to exploratory analysis."""
import click
import logging
import os
import site
import sys
from pathlib import Path
PROJECT_DIR = Path(__file__).resolve().parents[2]
site.addsitedir(PROJECT_DIR)
import pandas as pd
pd.set_option('display.max_rows', None)
from src.data.data_classes import DataSet

USECOLS = ["id",
            "last_scraped",
            "experiences_offered",
            "host_id",
            "host_since",
            "host_location",
            "host_response_time",
            "host_response_rate",
            "host_is_superhost",
            "host_neighbourhood",
            "host_total_listings_count",
            "host_verifications",
            "host_has_profile_pic",
            "host_identity_verified",
            "neighbourhood_cleansed",
            "city",
            "state",
            "zipcode",
            "market",
            "property_type",
            "room_type",
            "accommodates",
            "bathrooms",
            "bedrooms",
            "beds",
            "bed_type",
            "amenities",
            "square_feet",
            "price",
            "security_deposit",
            "cleaning_fee",
            "guests_included",
            "extra_people",
            "minimum_nights",
            "maximum_nights",
            "availability_30",
            "review_scores_rating",
            "review_scores_accuracy",
            "review_scores_cleanliness",
            "review_scores_checkin",
            "review_scores_communication",
            "review_scores_location",
            "review_scores_value",
            "requires_license",
            "license",
            "instant_bookable",
            "cancellation_policy",
            "require_guest_profile_picture",
            "require_guest_phone_verification",
            "reviews_per_month"]

DTYPES = {"id" : "int64",
            "host_id" : "int64",
            "host_response_rate" : "float64",
            "host_total_listings_count" : "float64",
            "host_response_time" : "category",
            "host_neighbourhood" : "category",
            "host_since" : "int64",
            "host_is_superhost" : "category",
            "host_location" : "object",
            "city" : "category",
            "zipcode" : "object",
            "state" : "category",
            "market" : "category",
            "neighbourhood_cleansed" : "category",
            "accommodates" : "int64",
            "bed_type" : "category",
            "square_feet" : "float64",
            "beds" : "float64",
            "room_type" : "category",
            "bedrooms" : "float64",
            "bathrooms" : "float64",
            "guests_included" : "int64",
            "property_type" : "category",
            "amenities" : "object",
            "maximum_nights" : "int64",
            "availability_30" : "int64",
            "minimum_nights" : "int64",
            "experiences_offered" : "category",
            "cleaning_fee" : "float64",
            "extra_people" : "float64",
            "price" : "float64",
            "security_deposit" : "category",
            "cancellation_policy" : "category",
            "review_scores_cleanliness" : "float64",
            "review_scores_location" : "float64",
            "review_scores_communication" : "float64",
            "review_scores_accuracy" : "float64",
            "review_scores_rating" : "float64",
            "review_scores_checkin" : "float64",
            "reviews_per_month" : "float64",
            "review_scores_value" : "float64",
            "license" : "category",
            "host_verifications" : "object",
            "require_guest_phone_verification" : "category",
            "require_guest_profile_picture" : "category",
            "host_identity_verified" : "category",
            "instant_bookable" : "category",
            "requires_license" : "category",
            "host_has_profile_pic" : "category",
            "last_scraped" : "object"}




def create_training_set(inpath, outpath):
    """Creates training set comprised of 2016-2018 data."""

    train_years = ["2016", "2017", "2018"]
    dataset = DataSet(name='training')
    
    for year in train_years:
        directory = os.path.join(inpath, year)
        filenames = os.listdir(directory)
        for filename in filenames:
            filepath = os.path.join(inpath, year, filename).replace("\\", "/")
            dataset.import_data(filename=filepath, columns=USECOLS)
            dataset.cast_types(DTYPES)
    print(dataset.get_metadata)
    outfile = os.path.join(outpath,'train.csv')
    dataset.export_data(filename=outfile)

def build_dataset(inpath, months, dataset):
    """Builds DataSet object for designated months from inpath."""
    
    for filename in os.listdir(inpath):
        month = filename.split("_")[2].split("-")[1]
        if month in months:
            filepath = os.path.join(inpath, filename).replace("\\", "/")
            dataset.import_data(filename=filepath, columns=USECOLS)
            dataset.cast_types(DTYPES)
    print(dataset.get_metadata)
    return dataset

def create_validation_set(inpath, outpath):
    """Creates validation set comprised of first-half of 2019 data."""

    months = ["01", "02", "03", "04", "05", "06"]    
    directory = os.path.join(inpath, "2019")
    dataset = DataSet(name='validation')
    dataset = build_dataset(directory, months, dataset)
    filename = os.path.join(outpath, 'validation.csv')
    dataset.export_data(filename=filename)

def create_test_set(inpath, outpath):
    """Creates validation set comprised of second-half of 2019 data."""

    months = ["07", "08", "09", "10", "11", "12"]    
    directory = os.path.join(inpath, "2019")
    dataset = DataSet(name='test')
    dataset = 
    dataset = build_dataset(directory, months, dataset)
    filename = os.path.join(outpath, 'test.csv')
    dataset.export_data(filename=filename)

def create_interim_datasets(project_dir, market):
    """Creates training set comprised of 2016 thru 2018 data inclusive."""
    inpath = os.path.join(project_dir, "data/raw/", market).replace("\\", "/")
    outpath = os.path.join(project_dir, "data/interim/", market).replace("\\", "/")

    logger = logging.getLogger(__name__)
    logger.info('\nCreating interim training set for %s market.' %market)    
    create_training_set(inpath, outpath)
    
    logger.info('\nCreating interim validation set for %s market.' %market)        
    create_validation_set(inpath, outpath)
    
    logger.info('\nCreating interim test set for %s market.' %market)        
    create_test_set(inpath, outpath)

    

@click.command()
@click.argument('market')
def main(market):
    # Creates interim training, validation and test sets.    
    create_interim_datasets(PROJECT_DIR, market)

if __name__ == "__main__":

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()