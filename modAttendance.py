from constants import ATTENDANCE_RAW, ATTENDANCE_CSV

import datetime as dt
import os
import pickle
import random

def modAttendance():
  attendance = None
  with open(ATTENDANCE_RAW, "rb") as f:
    attendance = pickle.load(f)

  # add test cases
  morning_start = dt.datetime.combine(date=dt.date(2021,9,29), time=dt.time(9,30,23))
  morning_end = dt.datetime.combine(date=dt.date(2021,9,29), time=dt.time(16,00,11))
  night_start = dt.datetime.combine(date=dt.date(2021,9,29), time=dt.time(17,2,43))
  night_end = dt.datetime.combine(date=dt.date(2021,9,29), time=dt.time(21,58,10))
  
  attendance["Phat"] = [morning_start, morning_end]
  attendance["Phat"].extend([night_start, night_end])
  attendance["Elon Musk"] = [morning_start + dt.timedelta(minutes=random.randint(-5,10)), morning_end + dt.timedelta(minutes=random.randint(-5,10))]
  attendance["Elon Musk"].extend([night_start + dt.timedelta(minutes=random.randint(-5,10)), night_end + dt.timedelta(minutes=random.randint(-5,10))])

  with open(ATTENDANCE_RAW, "wb") as f:
    pickle.dump(attendance, f, pickle.HIGHEST_PROTOCOL)

  print(attendance)

if __name__ == "__main__":
  modAttendance()