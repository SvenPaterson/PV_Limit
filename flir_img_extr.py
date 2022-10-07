from exiftool import ExifToolHelper

with ExifToolHelper() as et:
    for d in et.get_metadata("test_img.jpg"):
        for k, v in d.items():
            print(f"Dict: {k} = {v}")
    et.execute('-b', "test_img.jpg")