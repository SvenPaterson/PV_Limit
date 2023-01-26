import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk

from process_FLIR import get_FLIR_data
from process_futek import get_torque_data
from process_Omega import get_Omega_data
from tkinter import filedialog
from datetime import timedelta


def process_data(data_path, plot=False):
    print(f'Processing data from: {data_path}')
    
    if '48hr' in data_path:
        # duration in hrs, padding in mins
        TEST_DURATION = 48
        PADDING = 30

    elif '240hr' in data_path:
        TEST_DURATION = 240
        PADDING = 120
        
    else: 
        TEST_DURATION = 2
        PADDING = 10

    OPACITY = 0.75 # transparency of plotted data
    
    #  ---------------- IMPORT DATA ----------------  #
    print("\nImporting of Data has begun, please wait...\n")
    try:
        print('\tImporting Thermocouple data...')
        omega_data = get_Omega_data(data_path)
        print('\t  Thermocouple data import successful\n')
    except:
        raise ValueError('\n\tThermocouple data import unsuccessful\n')
    
    try:
        print('\tImporting FLIR Camera data...')
        flir_data = get_FLIR_data(data_path)
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
    # fig, [axs[0], axs[1]] = plt.subplots(nrows=2, ncols=1)
    
    fig, axs = plt.subplots(3, 1, figsize=(11, 8.5))
    fig.suptitle(os.path.split(data_path)[1])
    axs[0].set_ylabel('Torque, Nm')
    axs[1].set_ylabel('Temperature, degF')
    axs[2].set_ylabel('Temperature, degF')

    axs[0].set_ylim(0, 1.5)
    axs[1].set_ylim(120, 250)
    axs[2].set_ylim(-20, 20)


    l1 = axs[0].plot(torque_data["Date_Time"],
                  torque_data["Torque, Nm"],
                  color='green',
                  label='Torque')

    SMA = 1000 # simple moving average window
    l2 = axs[0].plot(torque_data["Date_Time"],
                     torque_data["Torque, Nm"].rolling(window=SMA).mean(),
                     color='lime',
                     label=f'SMA{SMA}')

    l3 = axs[1].plot(flir_data["Date_Time"],
                     flir_data["Temperature, degF"],
                     color='r',
                     label='Thermal Img')

    l4 = axs[1].plot(omega_data['Date_Time'],
                     omega_data['T1'],
                     color='aqua',
                     label='Inboard Seal Temp')

    if TEST_DURATION >= 48:
        l5 = axs[1].plot(omega_data['Date_Time'],
                         omega_data['T4'],
                         color='darkcyan',
                         label='Outboard Seal Temp')

    l6 = axs[1].plot(omega_data['Date_Time'],
                     omega_data['T2'],
                     color='yellow',
                     label='Inlet Temp')

    l7 = axs[1].plot(omega_data['Date_Time'],
                     omega_data['T3'],
                     color='orange',
                     label='Outlet Temp')

    l8 = axs[2].plot(omega_data['Date_Time'],
                     omega_data['T3']-omega_data['T2'],
                     color='black',
                     label='deltaT: Outlet-Inlet')
    
    for ax in axs:
        for line in ax.lines:
            line.set_alpha(OPACITY)

    test_start_time = torque_data["Date_Time"][0]

    #change depending on which type of test you're running
    if TEST_DURATION == 48:
        maj_formatter = matplotlib.dates.AutoDateFormatter(24)
        min_locator = matplotlib.ticker.AutoMinorLocator()
        x_label = 'Time (Hr:Min)\nDate (MM/DD)'
    if TEST_DURATION > 48:
        maj_formatter = matplotlib.dates.DateFormatter('%m/%d')
        min_locator = matplotlib.ticker.AutoMinorLocator(12)
        x_label = 'Date (MM/DD)'
    else:
        maj_formatter = matplotlib.dates.DateFormatter('%H:%M')
        min_locator = matplotlib.ticker.AutoMinorLocator(2)
        x_label = 'Time (Hr:Min)'

    test_duration = timedelta(hours=TEST_DURATION)
    time_padding = timedelta(minutes=PADDING)
    axs[2].set_xlabel(x_label)
    
    for ax in axs:
        ax.minorticks_on()
        ax.xaxis.set_major_formatter(maj_formatter)
        ax.xaxis.set_minor_locator(min_locator)
        ax.set_xlim(test_start_time - time_padding,
                    test_start_time + test_duration + time_padding)
        ax.grid(color='darkgrey', linestyle='-', 
                linewidth=0.25, alpha=1.00,
                which='Major')
        ax.grid(color='silver', linestyle='--',
                linewidth=0.25, alpha=0.75,
                which='Minor')
        ax.set_facecolor('white')

    # create legend for all traces
    lns1 = l1+l2
    labs1 = [line.get_label() for line in lns1]
    if TEST_DURATION >= 48:
        lns2 = l3+l4+l5+l6+l7
    else:
        lns2 = l3+l4+l6+l7
    labs2 = [line.get_label() for line in lns2]
    lns3 = l8
    labs3 = [line.get_label() for line in lns3]
    lns = [lns1, lns2, lns3]
    labs = [labs1, labs2, labs3]
    for i, ax in enumerate(axs):
        ax.legend(lns[i], labs[i], loc="upper right",
                  ncol=len(labs2), fontsize=8)

    plt.subplots_adjust(top=0.950,
                        bottom=0.08,
                        left=0.05,
                        right=0.99,
                        hspace=0.225,
                        wspace=0.2)


    
def main():
    #  --------------- SETUP PROJECT ---------------  #
    root = tk.Tk()
    root.withdraw()
    root_dir = os.path.join(sys.path[0])
    data_path = filedialog.askdirectory(title="Select Project Folder",
                                        initialdir=root_dir)
    
    process_data(data_path, Plot=True)
    plt.show()

if __name__ == '__main__':
    main()
