import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk

from process_FLIR import get_FLIR_data
from process_futek import get_torque_data
from process_Omega import get_Omega_data
from tkinter import filedialog


def main():
    root = tk.Tk()
    root.withdraw()
    root_dir = os.path.join(sys.path[0], 'raw_data')
    data_path = filedialog.askdirectory(title="Select Project Folder",
                                            initialdir=root_dir)
    cropped_data_path = os.path.join(data_path, 'cropped_data')
    if not os.path.exists(cropped_data_path):
                os.makedirs(cropped_data_path)

    #  ---------------- IMPORT DATA ----------------  #
    try:
        torque_data = get_torque_data(data_path)
        print('Torque data import successful')
    except:
        raise ValueError('Torque data import unsuccessful')
    try:
        omega_data = get_Omega_data(data_path)
        print('Thermocouple data import successful')
    except:
        raise ValueError('Thermocouple data import unsuccessful')
    try:
        flir_data = get_FLIR_data(data_path, cropped_data_path)
        print('FLIR Camera image processing / import successful')
    except:
        raise ValueError('FLIR Camera image processing / import unsuccessful')

    #  ------------------ PLOT DATA ------------------  #
    # fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
    fig, ax1 = plt.subplots()
    l1 = ax1.plot(torque_data["Date_Time"],
                  torque_data["Torque, Nm"],
                  color='g',
                  label='Torque')

    ax1.set_xlabel('Timestamp')
    ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
    ax1.set_ylabel('Torque, Nm', color='g')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Temperature, degF')

    l2 = ax2.plot(flir_data["Date_Time"],
                  flir_data["Temperature, degF"],
                  color='r',
                  label='Thermal Img')

    l3 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T1'],
                  color='aqua',
                  label='Seal Temp')

    l4 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T2'],
                  color='lightskyblue',
                  label='Inlet Temp')

    l5 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T3'],
                  color='dodgerblue',
                  label='Outlet Temp')

    l6 = ax2.plot(omega_data['Date_Time'],
                  omega_data['T3']-omega_data['T2'],
                  color='black',
                  label='deltaTemp')

    # create legend for all traces
    lns = l1+l2+l3+l4+l5+l6
    labs = [line.get_label() for line in lns]
    ax1.legend(lns, labs, loc="best")

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
