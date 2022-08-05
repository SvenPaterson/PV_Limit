import os
import csv
import pandas as pd

from PIL import Image, ImageOps
from pytesseract import pytesseract

# point to local pytesseract installation
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_FLIR_data(raw_data_path, crop_data_path, output=''):
    file_list = [f for f in os.listdir(raw_data_path) if f.endswith(".jpg")]
    results = {"timestamp": [], "temp": []}
    fail_list = []
    for i, file in enumerate(file_list):
        print('\n', file)
        img = Image.open(os.path.join(raw_data_path, file))

        # get exif date_time string from jpeg file, produced by FLIR camera
        img_exif = img.getexif()
        for key, val in img_exif.items():
            if key == 306:  # exif {key: '306', val: 'datetime'}
                date_time = val

        # crop, resize, resample, convert to greyscale, invert image
        img = img.crop((30, 5, 125, 24))
        w, h = img.size
        scale = 10
        new_size = w*scale, h*scale
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        img = img.convert('L')
        img = ImageOps.invert(img)
        img = img.point(lambda x: 0 if x < 155 else 255, '1')

        # save cropped greyscale image
        file_name = f"{file.split('.')[0]}_cropped.jpg"
        crop_path = os.path.join(crop_data_path, file_name)
        img.save(crop_path)

        # perform OCR on cropped image
        string = pytesseract.image_to_string(img, config='--psm 6')

        # interpet OCR output and save data
        if string[2] == '.':
            try:
                t = float(string[:4])
                results['temp'].append(t)
                results["timestamp"].append(date_time)
                print('temp read as: ', string[:4], 'degF')
            except ValueError:
                fail_list.append(file)
                print(string[:4], 'failed')
        else:
            try:
                t = float(string[:3])
                results['temp'].append(t)
                results['timestamp'].append(date_time)
                print('temp read as: ', string[:3], 'degF')
            except ValueError:
                fail_list.append(file)
                print(string[:3], 'failed')

    if fail_list:
        print('\nOCR failed on the following files:\n', fail_list)

    if output == 'csv':
        with open('results.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(results.keys())

            timestamp, temp = tuple(results.values())
            for i, ts in enumerate(timestamp):
                w.writerow([ts, temp[i]])
    else:
        df = pd.DataFrame(results)
        df.timestamp = pd.to_datetime(df.timestamp,
                                      format='%Y:%m:%d %H:%M:%S')
        df.rename(columns={"timestamp": "Date_Time",
                           "temp": "Temperature, degF"},
                  inplace=True)
        return df
