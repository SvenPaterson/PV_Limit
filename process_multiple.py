from process_datapoint import process_data

import sys
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# get list of subdirs in a directory and ask user to confirm what subdirs to process
def get_subdirs(path):
    subdirs = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    print('Found the following subdirectories:')
    for i, subdir in enumerate(subdirs):
        print(f'\t{i}: {subdir}')
    print('Which subdirectories would you like to process?')
    print('Enter a comma-separated list of numbers, or enter "all" to process all subdirectories.')
    print('Enter "none" to exit.')
    while True:
        response = input('Enter your response: ')
        if response == 'all':
            return subdirs
        elif response == 'none':
            sys.exit()
        else:
            try:
                indices = [int(i) for i in response.split(',')]
                if all([i in range(len(subdirs)) for i in indices]):
                    return [subdirs[i] for i in indices]
                else:
                    print('Invalid response. Please try again.')
            except:
                print('Invalid response. Please try again.')

#process each folder
raw_data = os.path.join(sys.path[0], 'raw_data', 'batch_process')
for folder in get_subdirs(raw_data):
    process_data(folder)
    plot_name = os.path.split(folder)[-1]
    processed_folder = os.path.join(sys.path[0], 'processed_plots')
    plt.tight_layout()
    plt.savefig(os.path.join(processed_folder, f'{plot_name}.png'))