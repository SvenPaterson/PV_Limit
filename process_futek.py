import os
import csv
import pandas as pd

from datetime import timedelta


def torque_file_to_df(file, sep):
    # read sample rate of data file
    with open(file) as f:
        reader = csv.reader(f)
        for i in range(21):
            next(reader)
        row = next(reader)
        if sep == ',':
            sample_rate = int(row[1])
        if sep == '\t':
            sample_rate = int(row[0].split('"')[1])
        
    df = pd.read_csv(file, sep=sep, header=23,
                     index_col='Sample Number',
                     parse_dates=[['Date', 'Time']])
    df.drop(columns=df.columns[-1], axis=1, inplace=True)
    df.rename(columns={'Tracking Value': 'Torque, Nm'}, inplace=True)

    # ensure sample rate is added to date_time column
    trigger_time = df.iloc[0]['Date_Time']
    time_delta = timedelta(milliseconds=1000/sample_rate)
    total_time = [trigger_time+i*time_delta for i in range(0, df.shape[0])]
    df['Date_Time'] = pd.Series(total_time)
    
    return df


def get_torque_data(raw_data_path):
    all_files = os.listdir(raw_data_path)
    file_list = [f for f in all_files if f.endswith(('.txt', '.csv'))]
    if not len(file_list):
        raise ValueError('There is no torque data file available to process')
    for file_path in file_list:
        file = os.path.join(raw_data_path, file_path)
        if file_path.endswith(".txt"):
            sep = '\t'
        if file_path.endswith(".csv"):
            sep = ','
        if not file_path.endswith(".csv") and not file_path.endswith('.txt'): 
            raise ValueError('Incorrect file type!')
        if 'df' not in locals():
            df = torque_file_to_df(file, sep)
        else:
            next_df = torque_file_to_df(file, sep)
            df= pd.concat([df, next_df], ignore_index=True)
    df.sort_values(by=['Date_Time'], ignore_index=True, inplace=True)
    # display positive torque
    df['Torque, Nm'] = df['Torque, Nm'].multiply(other=-1)
    return df
