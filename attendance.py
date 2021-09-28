import cv2
import numpy as np
import face_recognition
import os
from constants import *
import heapq
from datetime import datetime
import pickle
from PIL import Image, ImageTk
import threading
import time
from tkinter import Tk, Button, Label, Text, messagebox


names = []
imagesEmployee = os.listdir(EMPLOYEE_DIR)
heapq.heapify(imagesEmployee)
for img in imagesEmployee:
  names.append(img.split(".")[0])

# load encodings:
encs = []
for name in names:
  encs.append(np.loadtxt(f"{ENCODING_DIR}/{name}.enc", dtype=np.float64))

class AttendanceApp:
  # default to write every hour
  def __init__(self, writeInterval=3600):
    self.vs = cv2.VideoCapture(0)
    self.root = Tk()
    self.root.wm_title("Employee Attendance")
    self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    self.panel = Label(self.root)  # initialize image panel
    self.panel.pack(padx=10, pady=10)
    btn = Button(self.root, text="Confirm", command=self.confirm)
    btn.pack(fill="both", expand=True, padx=10, pady=10)

    self.writer = threading.Thread(target=self.writeData, args=[writeInterval])
    self.writer.daemon = True # auto-cleanup after program is shut down
    self.writer.start()

    self.attendance = dict()
    self.curEmployee = None

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
            matches = face_recognition.compare_faces(encs, encodedFace)
            faceDis = face_recognition.face_distance(encs, encodedFace)
            mIdx = np.argmin(faceDis)
            if matches[mIdx]: # should only be one
              self.curEmployee = name = names[mIdx]
              y1, x2, y2, x1 = faceLoc
              cv2.rectangle(smImg, (x1, y1), (x2, y2), NEON_GREEN, 2)
              cv2.rectangle(smImg, (x1, y2), (x2, y2+35), NEON_GREEN, cv2.FILLED)
              cv2.putText(smImg, name, (x1+15, y2+30), cv2.FONT_HERSHEY_COMPLEX, 1, WHITE, 2)

              imgtk = Image.fromarray(smImg)
              imgtk = ImageTk.PhotoImage(imgtk)
              self.panel.imgtk = imgtk
              self.panel.configure(image=imgtk)

        self.root.after(20, self.videoLoop)

  def writeData(self, timeInterval):
    # TODO: avoid rewriting the whole object
    # Write only the deltas from previous state
    while True:
      print("writing data...")
      with open(ATTENDANCE_RAW, "wb") as f:
        pickle.dump(self.attendance, f, pickle.HIGHEST_PROTOCOL)
      time.sleep(timeInterval)

  def confirm(self):
    # Employee confirm their entrance/exit time
    curTime = datetime.now()
    def postConfirm():
      # set start/end time
      if name not in self.attendance:
        self.attendance[name] = [curTime]
      else: 
        if (curTime - self.attendance[name][-1]).total_seconds() > MIN_DURATION:
          self.attendance[name].append(curTime)
      self.popup.destroy()

    self.popup = Tk()
    self.popup.wm_title("Confirmation")
    empTimeTxt = Label(self.popup, text=f"Employee: {self.curEmployee}. Time: {curTime.strftime('%H:%M:%d')}")
    empTimeTxt.pack(fill="both", padx=10, pady=10)
    okBtn = Button(self.popup, text="Ok", width=20, command=postConfirm)
    okBtn.pack(padx=10, pady=10)
    
  def onClose(self):
    if messagebox.askyesnocancel("Quit", "Do you want to quit?"):
      self.vs.release()
      try:
        self.popup.destroy()
      except:
        pass
      self.root.destroy()
      cv2.destroyAllWindows()


aa = AttendanceApp(5) # set writeInterval in seconds
aa.root.mainloop()
