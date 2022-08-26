import os
import pandas as pd


def get_Omega_data(raw_data_path):
    file_list = [f for f in os.listdir(raw_data_path) if f.endswith(".XLS")]
    if not len(file_list):
        raise ValueError("There is/are no temperature data file(s) available to process")
    df = pd.read_csv(os.path.join(raw_data_path, file_list[0]), sep='\t',
                     parse_dates=[['Date', 'Time']],
                     usecols=['Date', 'Time', 'Value', 'Value.1', 'Value.2'])
    df.rename(columns={'Value': 'T1',
                       'Value.1': 'T2',
                       'Value.2': 'T3'},
              inplace=True)
    return df
