import os
import fnmatch
from pathlib import Path

def getFileList( path, pattern ):
    fileList = []
    for root, dirs, files in os.walk( path ):
        for file in files:
            if fnmatch.fnmatch( file, pattern ):
                fileList.append( os.path.join( root, file ) )
    return fileList


def main():
    root = Path.cwd() / 'raw_data'
    fileList = dict.fromkeys( getFileList( root, 'FUTEK_data.pickle' ) )
    test_PVLIM_runs = {}
    test_48hr_runs = {}
    test_240hr_runs = {}
    folders_files = []
    for file in fileList:
        folders_files.append( file )
        split_path = file.split( '\\' )
        print( file )
        if 'psi' in split_path[5]:
            if split_path[5] not in test_PVLIM_runs:
                test_PVLIM_runs[ split_path[5] ] = ( [(split_path[6], file)] )
            else: test_PVLIM_runs[ split_path[5] ].append( (split_path[6], file) )
        if '48hr' in split_path[5]:
            test_48hr_runs[ split_path[5] ] = ( [(split_path[6], file)] )
            

    for key in test_48hr_runs:
        print( f'{key}: {test_48hr_runs[key]}' )

    


if __name__ == '__main__':
    main()
    