from attendance import AttendanceApp
from wage import WageCalculatorApp
from exportCSV import exportCSV
from encodeImages import encodeImages
from helper import fetchNames, fetchEncodings
from constants import EMPLOYEE_DIR, ENCODING_DIR


if __name__ == "__main__":
  # encode all employee images if necessary, then load encodings
  encodeImages(EMPLOYEE_DIR, ENCODING_DIR)
  names = fetchNames(EMPLOYEE_DIR)
  encs = fetchEncodings(ENCODING_DIR, names)

  aa = AttendanceApp(writeInterval=10, names=names, encodings=encs)
  aa.root.mainloop()

  wc = WageCalculatorApp(names=names)
  wc.root.mainloop()

  exportCSV()
