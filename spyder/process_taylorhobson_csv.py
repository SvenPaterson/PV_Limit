# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:09:36 2022

@author: stephen
"""
import os

from pathlib import Path
from typing import List, TypedDict


def processTHcsv():
    pass


def findTHcsv(folder: str | Path) -> (str, List[str | Path]):
# =============================================================================
#     Parameter is root folder and func returns a list of file paths of all CSV 
#     files produced by running "Apply a template..." command in Mountains
#     software
#
#     assumes root folder structure thusly:
#       
#       root:   --->   subdir: sample_one   ---> file.csv
#               --->   subdir: sample_two   ---> file.csv
#               .
#               .
#               --->   subdir: sample_N     ---> file.csv
#
#    no more than one csv per subdir can be processed
#   
# =============================================================================

    res = []
    check = set()
    for sd in os.listdir(folder):
        d = os.path.join(folder, sd)
        if os.path.isdir(d):
            for i, file in enumerate(os.listdir(d)):
                if file.endswith('.csv'):
                    res.append((sd, os.path.join(folder, sd, file)))
                    if sd not in check:
                        check.add(sd)
                    else:
                        raise ValueError('Error. There should not be more ' +
                                         'than one csv file per sample folder')
    return res

class ParamInfo(TypedDict):
    param: float
    
    
def importTHcsv(file: Path | str) -> ParamInfo:
    param = 'Ra'
    value = int(2)
    return {param: value}
        
if __name__ == '__main__':

        
    res = importTHcsv(r'D:\20053 PV Limit\wear sleeve surface finish')
    print(type(res['Ra']))