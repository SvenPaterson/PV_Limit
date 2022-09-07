import os
import pandas as pd


def XLStoDataframe(raw_data_path, file):
    """ print(raw_data_path)
    print("\n")
    print(file)
    print(os.path.join(raw_data_path, file)) """
    df = pd.read_csv(os.path.join(raw_data_path, file), sep='\t',
                     parse_dates=[['Date', 'Time']],
                     usecols=['Date', 'Time', 'Value', 'Value.1', 'Value.2'])
    df.rename(columns={'Value': 'T1',
                       'Value.1': 'T2',
                       'Value.2': 'T3'},
              inplace=True)
    return df


def get_Omega_data(raw_data_path):
    file_list = [f for f in os.listdir(raw_data_path) if f.endswith(".XLS")]
    if not len(file_list):
        raise ValueError("No temperature data files found")
    for file in file_list:
        if 'df' not in locals():
            df = XLStoDataframe(raw_data_path, file)
        else:
            next_df = XLStoDataframe(raw_data_path, file)
            df = pd.concat([df, next_df], ignore_index=True)
    return df
