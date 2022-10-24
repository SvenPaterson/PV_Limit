import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk

from process_FLIR_v2 import get_FLIR_data
from process_futek import get_torque_data
from process_Omega import get_Omega_data
from tkinter import filedialog
from datetime import datetime, timedelta

from torque_PSD import SAMPLE_RATE


def main():
    #  --------------- SETUP PROJECT ---------------  #
    root = tk.Tk()
    root.withdraw()
    root_dir = os.path.join(sys.path[0], 'raw_data')
    data_path = filedialog.askdirectory(title="Select Project Folder",
                                        initialdir=root_dir)
    cropped_data_path = os.path.join(data_path, 'cropped_data')
    if not os.path.exists(cropped_data_path):
        os.makedirs(cropped_data_path)
    print("\nImporting of Data has begun, please wait...\n")
    
    #  ---------------- IMPORT DATA ----------------  #
    try:
        print('\tImporting Thermocouple data...')
        omega_data = get_Omega_data(data_path)
        print('\t  Thermocouple data import successful\n')
    except:
        raise ValueError('\n\tThermocouple data import unsuccessful\n')
    
    try:
        print('\tImporting FLIR Camera data...')
        flir_data = get_FLIR_data(data_path, cropped_data_path)
        print('\t  FLIR Camera image processing/import successful\n')
    except:
        raise ValueError('\n\tFLIR Camera image processing/import unsuccessful\n')
    
    try:
        print('\tImporting Torque data...')
        torque_data = get_torque_data(data_path)
        print('\t  Torque data import successful\n')
    except:
        raise ValueError('\n\tTorque data import unsuccessful\n')


    #  ------------------ PLOT DATA ------------------  #
    # fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
    fig, ax1 = plt.subplots()
    l1 = ax1.plot(torque_data["Date_Time"],
                  torque_data["Torque, Nm"],
                  color='green',
                  label='Torque')

    ax1.set_xlabel('Timestamp')
    ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    ax1.set_ylabel('Torque, Nm', color='g')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Temperature, degF')
    #ax2.set_ylim(0, 400)

    l2 = ax2.plot(flir_data["Date_Time"],
                  flir_data["Temperature, degF"],
                  color='r',
                  label='Thermal Img')

    l3 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T1'],
                  color='aqua',
                  label='Inboard Seal Temp')

    l4 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T4'],
                  color='darkcyan',
                  label='Outboard Seal Temp')


    l5 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T2'],
                  color='lightskyblue',
                  label='Inlet Temp')

    l6 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T3'],
                  color='dodgerblue',
                  label='Outlet Temp')

    l7 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T3']-omega_data['T2'],
                  color='black',
                  label='deltaTemp')
    
    SMA = 20 # simple moving average window
    l8 = ax1.plot(torque_data["Date_Time"],
                  torque_data["Torque, Nm"].rolling(window=SMA).mean(),
                  color='lime',
                  label=f'SMA{SMA} - Torque')

    ax2.set_ylim(0,400)
    ax1.set_ylim(0,2)

    test_start_time = torque_data["Date_Time"][0]
    test_duration = timedelta(hours=48)
    time_padding = timedelta(hours=2)
    ax1.set_xlim(test_start_time-time_padding,
                 test_start_time + test_duration + time_padding)

    # create legend for all traces
    lns = l1+l8+l2+l3+l4+l5+l6+l7
    labs = [line.get_label() for line in lns]
    ax1.legend(lns, labs, loc="best")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
