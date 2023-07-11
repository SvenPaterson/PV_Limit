# PV_Limit

## Setting up environment 
use miniconda to manage environment. create new environment using environment.yml to include all the necessary libraries.

See 'importing environments' from conda cheatsheet page 2

    https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf

e.g. cun command in anaconda terminal:

    'conda env create -n PV_LIMIT --file environment.yml'

---

## Pre-reqs

You will need to also download and install Google's Tesseract OCR so that the wrapper library pytesseract can fuction:

tesseract 5 - windows installer:

    https://github.com/UB-Mannheim/tesseract/wiki
    

also you will need to update following line in process_FLIR.py to point to your own installation:

    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

---

## Overview

Code base for analyzing data from PV Limit testing

- FUTEK USB Torque Signal Conditioning Unit
- FLIR thermal imaging camera
- Omega temperature recorder with type T thermocouples

Code will accept multiple files from FUTEK torque sensor in either .txt (tab delim) or .cvs format. Place all files (.jpgs, .txt, .csv) from all capture devices in the root of a project folder and place that project folder in 
'/raw_data/batch_process' folder. Then run process_multiple.py script and choose which folders to process. 

you can also run process_datapoint.py to run a single test and open the plot.

Tho futek script anticipates imported data sample rate of 1 sample / sec. Might see weird behaviour or require debugging if different rate is used.

---

