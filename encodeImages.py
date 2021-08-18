import cv2
import numpy as np
import face_recognition
import os
import constants

employeeImages = os.listdir(constants.EMPLOYEE_DIR)
for ei in employeeImages:
  nameEmployee = ei.split(".")[0]
  imgEmployee = face_recognition.load_image_file(f"{constants.EMPLOYEE_DIR}/{ei}")
  imgEmployee = cv2.cvtColor(imgEmployee, cv2.COLOR_BGR2RGB)
  encEmployee = face_recognition.face_encodings(imgEmployee)[0]
  np.savetxt(f"{constants.ENCODING_DIR}/{nameEmployee}.enc", encEmployee)

print("Encoding complete!")