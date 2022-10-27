import os, sys
import csv
from random import sample
import pandas as pd

from tqdm import tqdm
from datetime import timedelta
from tkinter import filedialog

def torque_file_to_df(file, sep):
    # read sample rate of data file
    with open(file) as f:
        reader = csv.reader(f)
        i = 0
        while i < 28:
            row = next(reader)
            i += 1
    
    df = pd.read_csv(file, sep=sep, header=25,
                     parse_dates=[['Date', 'Time']]
                     )
    df.drop(columns=df.columns[-1], axis=1, inplace=True)

    df.rename(columns={'Tracking Value': 'Torque, Nm'}, inplace=True)
    
    df_avg = df.groupby('Date_Time', as_index=False)['Torque, Nm'].mean()
    return df_avg
    # ensure sample rate is added to date_time column
    
    """ if header_row > 23:
        time_delta = df.iloc[1]['Date_Time'] - df.iloc[0]['Date_Time']
    else: time_delta = timedelta(milliseconds=1000/sample_rate) """

    """ if df.iloc[1]['Date_Time'] == df.iloc[0]['Date_Time']:
        sample_rate = 200 #200S/s for PV lim typical
    else:
        sample_rate = 1 # 1S/2 for 48 test typical
    time_delta = timedelta(milliseconds=1000/sample_rate)
    trigger_time = df.iloc[0]['Date_Time']
    total_time = [trigger_time+i*time_delta for i in range(0, df.shape[0])]
    print(total_time[-1])
    df['Date_Time'] = pd.Series(total_time)
    return df """

""" root_dir = os.path.join(sys.path[0], 'raw_data')
file_path = filedialog.askopenfilename(title="Select Project Folder",
                                        initialdir=root_dir)

torque_file_to_df(file_path, '\t') """

def get_torque_data(raw_data_path):
    all_files = os.listdir(raw_data_path)
    file_list = [f for f in all_files if f.endswith(('.txt'))]
    if not len(file_list):
        raise ValueError('\n\tThere is no torque data file available to process')
    for file_path in tqdm(file_list):
        file = os.path.join(raw_data_path, file_path)
        if file_path.endswith(".txt"):
            sep = '\t'
        if file_path.endswith(".csv"):
            sep = ','
        if not file_path.endswith(".csv") and not file_path.endswith('.txt'): 
            raise ValueError('\n\tIncorrect file type!')
        if 'df' not in locals():
            df = torque_file_to_df(file, sep)
        else:
            next_df = torque_file_to_df(file, sep)
            df = pd.concat([df, next_df], ignore_index=True)
    df.sort_values(by=['Date_Time'], ignore_index=True, inplace=True)

    # display positive torque
    if df['Torque, Nm'].mean() < 0:
        df['Torque, Nm'] = df['Torque, Nm'].multiply(other=-1)

    """ # offset torque data if transducer was not exactly tared to 0 for 48hr test
    if (df.Date_Time.iloc[-1] - df.Date_Time.iloc[0]) > timedelta(hours=12):
        start_torque = df['Torque, Nm'][df['Torque, Nm'] < 0.5].mean()
        df['Torque, Nm'] = df['Torque, Nm'].subtract(start_torque) """

    return df
