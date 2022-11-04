import os
from pathlib import Path
from process_futek import get_torque_data

def get_futek_files(root_dir):
    dirs = []
    """ for d, _, f in os.walk(root_dir):
        for file in f:
            if file.endswith('.txt'):
                path = os.path.join(d, file)
                files.append(path) """
    for d, sd, f in os.walk(root_dir):
        if not sd:
            files = os.listdir(d)
            for file in files:
                if file.endswith('.txt'):
                    #print(d)
                    dirs.append(d)
    return dirs

if __name__ == '__main__':
    root_dir = Path.cwd() / 'raw_data'
    dirs = get_futek_files(root_dir)
    for d in dirs:
        print(f'processing: {d}')
        get_torque_data(d)