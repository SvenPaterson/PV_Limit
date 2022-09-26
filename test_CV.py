import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = cv2.imread("FLIR8001.jpg")
#img = img.crop((30, 5, 125, 24))
img = img[5:24, 30:125]
#[y:y+h, x:x+w]
cv2.dilate(img, (5, 5), img)
ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
cv2.imshow("Image", img)
text = pytesseract.image_to_string(img, config='--psm 7')
print(text)
cv2.waitKey(0)
cv2.destroyAllWindows()