from constants import EMPLOYEE_DIR, ENCODING_DIR

import cv2
import numpy as np
import face_recognition
import os

def encodeImages(empDir, encDir):
  employeeImages = os.listdir(empDir)
  for ei in employeeImages:
    nameEmployee = ei.split(".")[0]
    encFilename = f"{encDir}/{nameEmployee}.enc"
    if os.path.isfile(encFilename):
      print(f"{encFilename} already exists!")
      continue
    imgEmployee = face_recognition.load_image_file(f"{empDir}/{ei}")
    imgEmployee = cv2.cvtColor(imgEmployee, cv2.COLOR_BGR2RGB)
    encEmployee = face_recognition.face_encodings(imgEmployee)[0]
    np.savetxt(f"{encFilename}", encEmployee)
  print("Encoding complete!")

if __name__ == "__main__":
  encodeImages(EMPLOYEE_DIR, ENCODING_DIR)