import os
from constants import ATTENDANCE_FILE, MIN_DURATION
from datetime import datetime
import pickle

with open(ATTENDANCE_FILE, "rb") as f:
  attendance = pickle.load(f)
  print(attendance)
  for employee, timeObj in attendance.items():
    start, end = timeObj['start'], timeObj['end']
    print(f"Employee {employee}\n\tchecks in at {start.strftime('%H:%M:%S %D')}\n\tchecks out at {end.strftime('%H:%M:%S %D')}")