# Fraud Detection Data Preprocessing
This repository contains a script to preprocess and analyze fraud detection data. The preprocessing steps include handling missing values, cleaning data, exploratory data analysis (EDA), merging datasets for geolocation analysis, feature engineering, normalization and scaling, and encoding categorical features.

## Files
eda.py: The main script containing all the preprocessing functions.
Fraud_Data.csv: The dataset containing fraud detection data.
IpAddress_to_Country.csv: The dataset containing IP address ranges and corresponding countries.

## Preprocessing Steps
1. Handling Missing Values
The handle_missing_values function imputes missing values for numerical columns with the mean and drops rows with missing values for categorical columns.

2. Data Cleaning
The clean_data function removes duplicates, corrects data types, and converts the ip_address column to the appropriate format.

3. Exploratory Data Analysis (EDA)
The univariate_analysis and bivariate_analysis functions perform univariate and bivariate analysis on relevant columns.

4. Merge Datasets for Geolocation Analysis
The merge_datasets function converts IP addresses to integer format and merges Fraud_Data.csv with IpAddress_to_Country.csv based on IP address ranges.

5. Feature Engineering
The feature_engineering function creates new features such as transaction frequency, velocity, and time-based features (hour_of_day, day_of_week).

6. Normalization and Scaling
The normalize_and_scale function normalizes and scales numerical features to ensure consistency.

7. Encode Categorical Features
The encode_categorical_features function performs one-hot encoding for categorical features (source, browser, sex).

## Usage
Import the Modules:

python
from data_processing import (handle_missing_values, clean_data, univariate_analysis, 
                             bivariate_analysis, merge_datasets, feature_engineering, 
                             normalize_and_scale, encode_categorical_features)
import pandas as pd
Load the Data:

python
fraud_df = pd.read_csv('Fraud_Data.csv')
ip_df = pd.read_csv('IpAddress_to_Country.csv')
Preprocessing Steps:

python
fraud_df = handle_missing_values(fraud_df)
fraud_df = clean_data(fraud_df)
univariate_analysis(fraud_df)
merged_data = merge_datasets(fraud_df, ip_df)
merged_data = feature_engineering(merged_data)
bivariate_analysis(merged_data)
merged_data = encode_categorical_features(merged_data)
merged_data = normalize_and_scale(merged_data)
View Processed Data:

python
print(merged_data.head())

## Conclusion
This script performs comprehensive data preprocessing for fraud detection analysis, making the data suitable for machine learning algorithms.