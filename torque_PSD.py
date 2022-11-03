import os, sys
import matplotlib.pyplot as plt
import tkinter as tk

from tkinter import filedialog
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from process_futek import get_torque_data

SAMPLE_RATE = 300
STEP_LENGTH = 7200 # in seconds


def slice_data(df, interval_in_secs, sample_rate):
    sliced_data = {}
    print(f"Total Samples: {df.index[-1]}")
    chunk_test = df.index[-1] // interval_in_secs
    print(f'chunk test is: {chunk_test}')
    chunk = interval_in_secs * sample_rate
    print(f'chunk is {chunk}')

    for i in range(0, df.index[-1]-chunk, chunk):
        start = i
        stop = i + chunk
        hour = i / chunk
        #print(start, stop, hour)
        test_step = df.iloc[start:stop]
        sliced_data[f"test_step_{int(hour)}"] = test_step
    return sliced_data


def main():
    #  --------------- SETUP PROJECT ---------------  #
    root = tk.Tk()
    root.withdraw()
    root_dir = os.path.join(sys.path[0], 'raw_data')
    data_path = filedialog.askdirectory(title="Select Project Folder",
                                        initialdir=root_dir)
    df = get_torque_data(data_path)
    #print(df.head())

    animate_bool = False 
    if animate_bool:
        window = 60
        sliced_data = slice_data(df, window, SAMPLE_RATE)
        fig, ax = plt.subplots()
        frames = int(df.index[-1] / (window * SAMPLE_RATE) - 1)
        #L = plt.legend(loc=1)
        def animate(i):
            ax.clear()
            ax.psd(sliced_data[f'test_step_{i}']["Torque, Nm"],
                   Fs=SAMPLE_RATE,
                   label=f"Window: {window} secs at Time: {round(i*60/3600, 1)} hrs")
            ax.set_ylim(bottom=-80, top=10)
            ax.yaxis.set_major_locator(MultipleLocator(10))
            #fig.set_label()
            plt.legend(loc=1)
            plt.tight_layout()
            return ax

        ani = FuncAnimation(fig, animate, frames=frames, interval=100, repeat=True)
        #interval, delay between frames in milliseconds
    else:
        fig, ax = plt.subplots()
        
        sliced_data = slice_data(df, STEP_LENGTH, SAMPLE_RATE)
        #print(sliced_data)
        for i in range(0, len(sliced_data)):
            ax.psd(sliced_data[f'test_step_{i}']["Torque, Nm"],
                Fs=SAMPLE_RATE,
                label= f"Test Step #{i}")
        ax.set_ylim(bottom=-80, top=10)
    
    
    plt.show()






if __name__ == '__main__':
    main()