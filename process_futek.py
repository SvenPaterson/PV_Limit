import os
import csv
import pandas as pd

from datetime import timedelta


def get_torque_data(raw_data_path):
    file_list = [f for f in os.listdir(raw_data_path) if f.endswith(".txt")]
    if len(file_list) > 1:
        raise ValueError("This script cannot process more than one torque data"
                         " file at a time")
    else:
        file = os.path.join(raw_data_path, file_list[0])

        # read sample rate of data file
        with open(file) as f:
            reader = csv.reader(f)
            for i in range(21):
                next(reader)
            sample_rate = int(next(reader)[0].split('"')[1])

        # import data file
        df = pd.read_csv(file, sep='\t',
                         header=23,
                         index_col='Sample Number',
                         parse_dates=[['Date', 'Time']])
        df.drop(columns=df.columns[-1], axis=1, inplace=True)
        df.rename(columns={"Tracking Value": "Torque, Nm"}, inplace=True)

        # ensure sample rate is added to date_time column
        trigger_time = df.iloc[0]['Date_Time']
        time_delta = timedelta(milliseconds=1000/sample_rate)
        total_time = [trigger_time+i*time_delta for i in range(0, df.shape[0])]
        df['Date_Time'] = pd.Series(total_time)
    return df
