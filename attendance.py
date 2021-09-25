import cv2
import numpy as np
import face_recognition
import os
from constants import *
import heapq
from datetime import datetime
import pickle

names = []
imagesEmployee = os.listdir(EMPLOYEE_DIR)
heapq.heapify(imagesEmployee)
for img in imagesEmployee:
  names.append(img.split(".")[0])

# load encodings:
encs = []
for name in names:
  encs.append(np.loadtxt(f"{ENCODING_DIR}/{name}.enc", dtype=np.float64))

attendance = dict()

cap = cv2.VideoCapture(0)
while True:
  success, img = cap.read()
  width = int(img.shape[1] * SCALE_PCNT / 100)
  height = int(img.shape[0] * SCALE_PCNT / 100)
  smImg = cv2.resize(img, (width, height))
  smImg = cv2.cvtColor(smImg, cv2.COLOR_BGR2RGB)
  
  faceLocs = face_recognition.face_locations(smImg)
  encodedFaces = face_recognition.face_encodings(smImg, faceLocs)
  smImg = cv2.cvtColor(smImg, cv2.COLOR_RGB2BGR)

  with open(ATTENDANCE_RAW, "wb") as f:
    for faceLoc, encodedFace in zip(faceLocs, encodedFaces):
      matches = face_recognition.compare_faces(encs, encodedFace)
      faceDis = face_recognition.face_distance(encs, encodedFace)
      mIdx = np.argmin(faceDis)
      if matches[mIdx]:
        name = names[mIdx]
        y1, x2, y2, x1 = faceLoc
        cv2.rectangle(smImg, (x1, y1), (x2, y2), NEON_GREEN, 2)
        cv2.rectangle(smImg, (x1, y2), (x2, y2+35), NEON_GREEN, cv2.FILLED)
        cv2.putText(smImg, name, (x1+15, y2+30), cv2.FONT_HERSHEY_COMPLEX, 1, WHITE, 2)
        # set start/end time
        if name not in attendance:
          attendance[name] = [datetime.now()]
          continue
        if (datetime.now() - attendance[name][-1]).total_seconds() > MIN_DURATION:
          attendance[name].append(datetime.now())
    pickle.dump(attendance, f, pickle.HIGHEST_PROTOCOL)

  cv2.imshow("Webcam", smImg)
  cv2.waitKey(1)