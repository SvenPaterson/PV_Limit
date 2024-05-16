import os
import pandas as pd

def correctCSV(file_path):
    with open(file_path, 'r') as f_in, open((file_path+'.csv'), 'w') as f_out:
        header = f_in.readlines(1)[0]
        f_out.write(header)
        for line in f_in.readlines():
            if line != header:
                f_out.write(line)

def XLStoDataframe(raw_data_path, file):
    df = pd.read_csv(os.path.join(raw_data_path, file), sep='\t',
                     parse_dates=[['Date', 'Time']],
                     usecols=['Date', 'Time', 'Value', 'Value.1', 'Value.2', 'Value.3'])
    # TSSvBABSL test 5-16-24
    df.rename(columns={'Value': 'T2', # Inlet
                       'Value.1': 'T1', # Inboard
                       'Value.2': 'T4', # Outboard
                       'Value.3': 'T3'}, # Outlet
              inplace=True)
    # OLD
    """ df.rename(columns={'Value': 'T1', # Inboard Seal
                       'Value.1': 'T2', # Inlet
                       'Value.2': 'T3', # Outlet 
                       'Value.3': 'T4'}, # Outboard Seal
              inplace=True) """
    return df


def get_Omega_data(raw_data_path):
    file_list = [f for f in os.listdir(raw_data_path) if f.endswith(".XLS")]
    if not len(file_list):
        raise ValueError("No temperature data files found")
    for file in file_list:
        correctCSV(os.path.join(raw_data_path,file))
    file_list =[]
    for f in os.listdir(raw_data_path):
        if f.endswith(".csv") and f != 'fail_list.csv':
            file_list.append(f)
    for i, file in enumerate(file_list):
        if 'df' not in locals():
            df = XLStoDataframe(raw_data_path, file)
        else:
            next_df = XLStoDataframe(raw_data_path, file)
            df = pd.concat([df, next_df], ignore_index=True)

    return df
