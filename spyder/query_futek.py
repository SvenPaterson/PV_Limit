# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:43:50 2022

@author: stephen
"""
import csv, os
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from pathlib import Path

root = tk.Tk()

filename = 'test_file_1.txt'
filepath = os.path.join(Path.cwd(), filename)

file_path = filedialog.askopenfilename(title="Select Torque File",
                                       initialdir=Path.cwd())
print(file_path)
def row_count(file):
    with open(file) as in_file:
        return sum(1 for _ in in_file)

num_rows = row_count(filepath)
print(f'num_rows: {num_rows}')
with open(filepath) as f:
    
    reader = csv.reader(f)
    row = next(reader)
    i = 0
    header_row = False
    sample_rate = False
    blank_rows = 0
    samples = {}
    
    while i < 30:#num_rows-2:
        row = next(reader)
        
        if not row:
            blank_rows += 1
        if row:
            row = row[0].split('\t')
            print(row)
            if not header_row and row[0] == 'Sample Number':
                header_row = i
                print(f'header_row found and is: {header_row}')
            if row[0] == 'Sampling Rate':
                sample_rate = i+2
            if sample_rate and i == sample_rate:
                sample_rate = int(row[1].split('"')[1])
                
        if i > 27:
            sample_num = int(row[0])
            torque = float(row[1].split('"')[1])
            date_time = datetime.strptime(row[2].strip('"'), "%m/%d/%Y %H:%M:%S %p" )
            
            if date_time not in samples:
                samples[date_time] = [sample_num]
                
            else:
                samples[date_time].append(sample_num)
            
        i += 1
#%%
count = 0
hist = []
for key in samples.keys():
    for value in samples[key]:
        count +=1
    hist.append(count)
    count = 0

root.destroy()