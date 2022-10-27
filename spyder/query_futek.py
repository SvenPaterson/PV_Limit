# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 10:43:50 2022

@author: stephen
"""
import csv, sys, os
from datetime import datetime

from pathlib import Path

print(Path.cwd())

filename = 'test_file_1.txt'
filepath = os.path.join(Path.cwd(), filename)
    
def row_count(file):
    with open(file) as in_file:
        return sum(1 for _ in in_file)

num_rows = row_count(filepath)
print(f'num_rows: {num_rows}')
with open(filepath) as f:
    
    reader = csv.reader(f)
    row = next(reader)
    i = 0
    
    samples = {}
    while i < num_rows-2:
        row = next(reader)
        if row:
            row = row[0].split('\t')
        
        if i > 27:
            #print(row[0])
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
