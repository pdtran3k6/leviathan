from constants import ATTENDANCE_RAW, ATTENDANCE_CSV

import csv
import os
import pickle

def exportCSV():
  with open(ATTENDANCE_RAW, "rb") as f:
    attendance = pickle.load(f)
    # print(attendance) # for debugging purpose
    # newline="" to avoid empty lines in output on Windows
    with open(ATTENDANCE_CSV, "w", newline="") as fcsv:
      writer = csv.writer(fcsv)
      for employeeName, timeLst in attendance.items():
        writer.writerows([[time.strftime('%m-%d-%Y'), time.strftime('%H:%M'), employeeName] for time in timeLst])

if __name__ == "__main__":
  exportCSV()