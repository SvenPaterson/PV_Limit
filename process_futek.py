import os
import csv
from random import sample
import pandas as pd

from tqdm import tqdm
from datetime import timedelta


def torque_file_to_df(file, sep):
    ### Find header row and sample rate of data ###
    with open(file) as f:
        reader = csv.reader(f)
        row = next(reader)
        
        header_row = False
        sample_rate = False
        blank_rows = 0

        i = 1 # pd.read_csv counts the 0th row as 1
        while i < 30:
            row = next(reader)
            if not row:
                blank_rows += 1
            if row:
                row = row[0].split('\t')
                
                if not header_row and row[0] == 'Sample Number':
                    header_row = i
                if row[0] == 'Sampling Rate':
                    sample_rate = i+2
                if sample_rate and i == sample_rate:
                    sample_rate = int(row[1].split('"')[1])
            i += 1
        header_row -= blank_rows

    df = pd.read_csv(file, sep=sep, header=header_row,
                     index_col='Sample Number', 
                     parse_dates=[['Date', 'Time']])
    df.drop(columns=df.columns[-1:], axis=1, inplace=True)
    df.rename(columns={'Tracking Value': 'Torque, Nm'}, inplace=True)
    
        
    if  'C3_S5' in file:
        """ 
        # Super dirty hack for weird variable sample_rate thanks to USB bandwidth
        # limitations when setting high sample rate on Sensit live logging view
        """
        df_avg = df.groupby('Date_Time', as_index=False)['Torque, Nm'].mean()
        return df_avg
    else:
        if df.iloc[1]['Date_Time'] != df.iloc[0]['Date_Time']:
            """ 
            # if running in live view on Sensit software the sample_rate of
            # sensor will not match the sample interval on the data file. So
            # you will need to manually select the sample rate here
            """
            sample_rate = 1

        time_delta = timedelta(milliseconds=1000/sample_rate)
        trigger_time = df.iloc[0]['Date_Time']
        total_time = [trigger_time+i*time_delta for i in range(0, df.shape[0])]
        df['Date_Time'] = pd.Series(total_time)
        return df
    


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

    return df
