from constants import ATTENDANCE_RAW, MIN_DURATION, EMPLOYEE_DIR, ENCODING_DIR
from helper import fetchNames, fetchEncodings

import cv2
from datetime import datetime
import face_recognition
import numpy as np
import pickle
from PIL import Image, ImageTk
from tkinter import Tk, Button, Label, Text, messagebox
import threading
import time

class AttendanceApp:
  # default to write every hour
  def __init__(self, writeInterval=3600, names=None, encodings=None):
    self.vs = cv2.VideoCapture(0)
    self.root = Tk()
    self.root.wm_title("Employee Attendance")
    self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
    self.panel = Label(self.root)  # initialize image panel
    self.panel.pack(padx=10, pady=10)
    btn = Button(self.root, text="Confirm", command=self.confirm)
    btn.pack(fill="both", expand=True, padx=10, pady=10)

    self.writer = threading.Thread(target=self.writeData, args=[writeInterval])
    self.stopCondition = threading.Condition()
    self.stopWriterThread = False
    self.writer.start()

    self.attendance = dict()
    self.curEmployee = None
    self.encs = encodings
    self.names = names

    self.videoLoopId = None
    self.videoLoop()

  def videoLoop(self):
    ok, img = self.vs.read()
    if ok:
      width = int(img.shape[1] * SCALE_PCNT / 100)
      height = int(img.shape[0] * SCALE_PCNT / 100)
      smImg = cv2.resize(img, (width, height))
      smImg = cv2.cvtColor(smImg, cv2.COLOR_BGR2RGB)
      smImg = cv2.flip(smImg,1)

      # insert image into tk
      imgtk = Image.fromarray(smImg)
      imgtk = ImageTk.PhotoImage(imgtk)
      self.panel.imgtk = imgtk
      self.panel.configure(image=imgtk)

      faceLocs = face_recognition.face_locations(smImg)
      encodedFaces = face_recognition.face_encodings(smImg, faceLocs)

      for faceLoc, encodedFace in zip(faceLocs, encodedFaces):
        matches = face_recognition.compare_faces(self.encs, encodedFace)
        faceDis = face_recognition.face_distance(self.encs, encodedFace)
        mIdx = np.argmin(faceDis)
        if matches[mIdx]: # should only be one
          self.curEmployee = self.names[mIdx]
          y1, x2, y2, x1 = faceLoc
          cv2.rectangle(smImg, (x1, y1), (x2, y2), NEON_GREEN, 2)
          cv2.rectangle(smImg, (x1, y2), (x2, y2+35), NEON_GREEN, cv2.FILLED)
          cv2.putText(smImg, self.curEmployee, (x1+15, y2+30), cv2.FONT_HERSHEY_COMPLEX, 1, WHITE, 2)

          imgtk = Image.fromarray(smImg)
          imgtk = ImageTk.PhotoImage(imgtk)
          self.panel.imgtk = imgtk
          self.panel.configure(image=imgtk)

    self.videoLoopId = self.root.after(20, self.videoLoop)

  def writeData(self, timeInterval):
    # TODO: #OPTIMIZATION avoid rewriting the whole object
    # Write only the deltas from previous state
    self.stopCondition.acquire()
    while not self.stopWriterThread:
      print("writing data...")
      with open(ATTENDANCE_RAW, "wb") as f:
        pickle.dump(self.attendance, f, pickle.HIGHEST_PROTOCOL)
      self.stopCondition.wait(timeout=timeInterval)
    self.stopCondition.release()

  def confirm(self):
    # Employee confirm their entrance/exit time
    curTime = datetime.now()
    if messagebox.askyesno(title="Confirmation", message=f"Employee: {self.curEmployee}. Time: {curTime.strftime('%H:%M:%S')}"):
      if self.curEmployee not in self.attendance:
        self.attendance[self.curEmployee] = [curTime]
      else:  
        if (curTime - self.attendance[self.curEmployee][-1]).total_seconds() > MIN_DURATION:
          self.attendance[self.curEmployee].append(curTime)
      # Force update
      self.stopCondition.acquire()
      print("updating data...")
      with open(ATTENDANCE_RAW, "wb") as f:
        pickle.dump(self.attendance, f, pickle.HIGHEST_PROTOCOL)
      self.stopCondition.release()
    
  def onClose(self):
    self.vs.release()
    self.root.after_cancel(self.videoLoopId)
    self.root.destroy()
    self.stopWriterThread = True
    self.stopCondition.acquire()
    self.stopCondition.notifyAll()
    self.stopCondition.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  names = fetchNames(EMPLOYEE_DIR)
  aa = AttendanceApp(writeInterval=10, names=names, encodings=fetchEncodings(ENCODING_DIR, names))
  aa.root.mainloop()
