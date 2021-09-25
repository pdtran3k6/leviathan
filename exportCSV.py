import os
from constants import ATTENDANCE_RAW, ATTENDANCE_CSV, MIN_DURATION
import pickle
import csv

with open(ATTENDANCE_RAW, "rb") as f:
  attendance = pickle.load(f)
  # print(attendance) # for debugging purpose
  with open(ATTENDANCE_CSV, "w") as fcsv:
    writer = csv.writer(fcsv)
    for employeeName, timeLst in attendance.items():
      for time in timeLst:
        writer.writerow([time.strftime('%m-%d-%Y'), time.strftime('%H:%M'), employeeName])
