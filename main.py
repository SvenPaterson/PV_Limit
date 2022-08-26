import sys
import os
import matplotlib
import matplotlib.pyplot as plt

from process_FLIR import get_FLIR_data
from process_futek import get_torque_data
from process_Omega import get_Omega_data


def main():
    root = sys.path[0]
    raw_data_path = os.path.join(root, 'raw_data')
    cropped_data_path = os.path.join(root, 'cropped_data')

    torque_data = get_torque_data(raw_data_path)
    print(torque_data, torque_data.info())
    omega_data = get_Omega_data(raw_data_path)
    print(omega_data, omega_data.info())
    flir_data = get_FLIR_data(raw_data_path, cropped_data_path)
    print(flir_data, flir_data.info())

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
