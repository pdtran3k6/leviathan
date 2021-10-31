from attendance import AttendanceApp
from constants import EMPLOYEE_DIR, ENCODING_DIR
from encodeImages import encodeImages
from exportCSV import exportCSV
from helper import fetchNames, fetchEncodings
from wage import WageCalculatorApp

if __name__ == "__main__":
  # encode all employee images if necessary, then load encodings
  encodeImages(EMPLOYEE_DIR, ENCODING_DIR)
  names = fetchNames(EMPLOYEE_DIR)
  encs = fetchEncodings(ENCODING_DIR, names)

  aa = AttendanceApp(writeInterval=10, names=names, encodings=encs)
  aa.root.mainloop()

  # No longer needed, do in Excel
  # wc = WageCalculatorApp(names=names)
  # wc.root.mainloop()

  exportCSV()
