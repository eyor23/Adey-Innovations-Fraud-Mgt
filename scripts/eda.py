import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def handle_missing_values(df):
    # Impute missing values with mean for numerical columns
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].mean())

    # Drop rows with missing values for categorical columns
    df = df.dropna(subset=df.select_dtypes(exclude=[np.number]).columns)
    return df


def clean_data(df):
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    # Correct data types
    df['signup_time'] = pd.to_datetime(df['signup_time'])
    df['purchase_time'] = pd.to_datetime(df['purchase_time'])
    df['age'] = df['age'].astype(int)
    df['ip_address'] = df['ip_address'].astype(float)
    return df

def univariate_analysis(df):
    columns = ['purchase_value', 'browser', 'age', 'ip_address']
    for col in columns:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f'Univariate Analysis of {col}')
        plt.show()

def bivariate_analysis(df):
    df['transaction_count'] = df.groupby('user_id')['purchase_time'].transform('count')
    df['hour_of_day'] = df['purchase_time'].dt.hour
    relevant_pairs = [
        ('purchase_value', 'age'),
        ('purchase_value', 'transaction_count'),
        ('purchase_time', 'source'),
        ('purchase_value', 'hour_of_day')
    ]
    for x, y in relevant_pairs:
        plt.figure()
        sns.scatterplot(data=df, x=x, y=y)
        plt.title(f'Bivariate Analysis of {x} vs {y}')
        plt.show()

import struct

#def float_to_ip(f):
 #   packed = struct.pack('!f', f)
  #  ip = struct.unpack('!I', packed)[0]
   # return ip

def convert_ip_to_integer(ip):
    return int(ip)


#def merge_datasets(fraud_df, ip_df):
    #ip_df['lower_bound_ip_address'] = ip_df['lower_bound_ip_address'].apply(convert_ip_to_integer)
    #ip_df['upper_bound_ip_address'] = ip_df['upper_bound_ip_address'].apply(convert_ip_to_integer)
    #fraud_df['ip_address'] = fraud_df['ip_address'].apply(convert_ip_to_integer)

    #merged_df = pd.merge(fraud_df, ip_df, how='left', left_on='ip_address', right_on='lower_bound_ip_address')
    #return merged_df

def merge_datasets(fraud_df, ip_df):
    ip_df['lower_bound_ip_address'] = ip_df['lower_bound_ip_address'].astype(float).astype(int)
    ip_df['upper_bound_ip_address'] = ip_df['upper_bound_ip_address'].astype(float).astype(int)
    fraud_df['ip_address'] = fraud_df['ip_address'].apply(convert_ip_to_integer)

    # Merge fraud data with ip address data based on ip address ranges
    merged_df = pd.merge(
        fraud_df,
        ip_df,
        how='left',
        left_on='ip_address',
        right_on='lower_bound_ip_address'
    )
    return merged_df

def feature_engineering(df):
    # Transaction frequency and velocity
    df['transaction_count'] = df.groupby('user_id')['purchase_time'].transform('count')
    df['transaction_amount_sum'] = df.groupby('user_id')['purchase_value'].transform('sum')
    # Time-Based features
    df['hour_of_day'] = df['purchase_time'].dt.hour
    df['day_of_week'] = df['purchase_time'].dt.dayofweek
    return df

def normalize_and_scale(df):
    scaler = StandardScaler()
    df[df.select_dtypes(include=[np.number]).columns] = scaler.fit_transform(df.select_dtypes(include=[np.number]))
    return df

def encode_categorical_features(df):
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(df[['source', 'browser', 'sex']])
    encoded_df = pd.DataFrame(encoded_features.toarray(), columns=encoder.get_feature_names_out(['source', 'browser', 'sex']))
    df = df.drop(columns=['source', 'browser', 'sex'])
    df = pd.concat([df, encoded_df], axis=1)
    return df

def main():
    fraud_df = pd.read_csv(r'C:\Users\user\Desktop\Kifiya\Adey-Innovations-Fraud-Mgt\data\Fraud_Data.csv')
    ip_df = pd.read_csv(r'C:\Users\user\Desktop\Kifiya\Adey-Innovations-Fraud-Mgt\data\IpAddress_to_Country.csv')
    fraud_df = handle_missing_values(fraud_df)
    fraud_df = clean_data(fraud_df)
    univariate_analysis(fraud_df)
    bivariate_analysis(fraud_df)
    merged_df = merge_datasets(fraud_df, ip_df)
    merged_df = feature_engineering(merged_df)
    merged_df = normalize_and_scale(merged_df)
    merged_df = encode_categorical_features(merged_df)
    return merged_df

if __name__ == "__main__":
    processed_df = main()
    print(processed_df.head())
