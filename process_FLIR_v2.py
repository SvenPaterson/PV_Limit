import os
import pandas as pd
import pickle
import numpy as np
import cv2

from tqdm import tqdm
from PIL import Image
from pytesseract import pytesseract

# point to local pytesseract installation
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# DO THIS https://www.analyticsvidhya.com/blog/2021/06/optical-character-recognitionocr-with-tesseract-opencv-and-python/

def listToString(s):
    str1 = ""
    return str1.join(s)

def get_FLIR_data(raw_data_path, crop_data_path):
    file_list = [f for f in os.listdir(raw_data_path) if f.endswith('.jpg')]
    prev_data_file = [f for f in os.listdir(raw_data_path) if f.endswith('.pickle')]

    if len(prev_data_file) == 0 and len(file_list) == 0:
        error_msg = "\n\tThere is no previously processed data nor\n" \
                    "\tare there any FLIR imgs available to process"
        raise ValueError(error_msg)

    if len(prev_data_file) > 0:
        prev_data_path = os.path.join(raw_data_path, prev_data_file[0])
        df = pickle.load(open(prev_data_path, 'rb'))
    
    else:
        print("Initial image processing required, please wait...")        
        results = {'timestamp': [], 'temp': [], 'filename': []}
        fail_list = [("file, datetime, full string, float conversion attempt")]

        for file in tqdm(file_list):
            img = Image.open(os.path.join(raw_data_path, file))

            # get exif date_time string from jpeg file, produced by FLIR camera
            img_exif = img.getexif()
            for key, val in img_exif.items():
                if key == 306:  # exif {key: '306', val: 'datetime'}
                    date_time = val

            # crop, resize, resample, convert to greyscale, invert image
            img = cv2.imread(os.path.join(raw_data_path, file))
            img = img[5:24, 30:90]
            cv2.dilate(img, (5, 5), img)
            ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
            img = cv2.bitwise_not(img)
            img = cv2.copyMakeBorder(img, 
                                        10, 10, 10, 10,
                                        cv2.BORDER_CONSTANT, 
                                        value= (255,255,255)
                                    )
            img = cv2.inRange(img, (0,0,0), (10, 10, 10))
            img = cv2.bitwise_not(img)
            # save cropped greyscale image
            file_name = f'{file.split(".")[0]}_cropped.jpg'
            crop_path = os.path.join(crop_data_path, file_name)
            cv2.imwrite(crop_path, img)

            # perform OCR on cropped image
            string = pytesseract.image_to_string(img, config='--psm 7')

            # interpet OCR output and save data
            # this is super brute force and may still produce some errors
            
            
            # TODO refine below filter
            num = [c for c in string if c.isdigit() or c == '.' or not 'F']

            try:
                t = float(listToString(num[:3]))
                results['temp'].append(t)
                results['timestamp'].append(date_time)
                results['filename'].append(file)
            except:
                fail_list.append((f'{file}, {date_time}, {string}, {num}'))
        
        df = pd.DataFrame(results)
        df.timestamp = pd.to_datetime(df.timestamp,
                                    format='%Y:%m:%d %H:%M:%S')
        df.rename(columns={'timestamp': 'Date_Time',
                        'temp': 'Temperature, degF'},
                        inplace=True)
        df.sort_values(by=['Date_Time'], inplace=True, ignore_index=True)
        df.to_pickle(os.path.join(raw_data_path, 'FLIR_data.pickle'))

        if len(fail_list) > 1:
            print(f"\n[FAIL_LIST] OCR failed on: {len(fail_list)-1} out of", end=' ')
            print(f"{len(results['temp'])} processed files\n")
            with open("fail_list.csv", 'w') as f_out:
                for line in fail_list:
                    f_out.write(line)
        else:
            success_msg = '[FAIL_LIST] all files converted without error'
            print(success_msg)
            with open(os.path.join(raw_data_path, "fail_list.csv"), 'w') as f_out:
                f_out.write(success_msg)
        
        print("\n[Processing Complete]\n")
    
    print(df)
    return df
