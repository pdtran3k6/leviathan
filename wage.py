from helper import fetchNames
from constants import ATTENDANCE_RAW, EMPLOYEE_DIR
from datetime import datetime
import pickle
import wage
import json
from tkinter import Tk, Button, Label, Text, Frame, Entry, Checkbutton, IntVar, messagebox


class WageCalculatorApp:
  def __init__(self, writeInterval=3600, names=None):
    self.root = Tk()
    self.root.wm_title("Wage Calculator")
    self.root.wm_protocol("WM_DELETE_WINDOW", self.root.destroy)
    self.tipFrame = Frame(self.root, height=20)
    self.tipFrame.pack()
    self.empFrame = Frame(self.root)
    self.empFrame.pack()

    self.empPaycheck = dict()
    self.empTip = {n: 0 for n in names} # TODO: catch error if not names
    self.empTipShift = {n: [] for n in names}
    self.empTime = {n: 0 for n in names} 

    # load hours worked
    with open(ATTENDANCE_RAW, "rb") as f:
      attendance = pickle.load(f)
      i = 0
      for employeeName, timeLst in attendance.items():
        if len(timeLst) & 1: # odd number of entries
          print(f"ERROR: Missing time for employee {employeeName}")
          continue
        
        print(f"processing employee {employeeName} with times [{timeLst}]")
        empName = Label(self.empFrame, text=employeeName)
        empName.grid(row=i, column=0, pady=10, sticky="w")
        
        for k in range(0,len(timeLst)-1,2):
          time1, time2 = timeLst[k], timeLst[k+1]
          hoursWorked = (time2-time1).seconds//3600 # TODO: round up or down?
          self.empTime[employeeName] += hoursWorked 
          shift = IntVar()
          hours = Checkbutton(self.empFrame, text=f"{time1.strftime('%H:%M')} - {time2.strftime('%H:%M')}", variable=shift)
          hours.grid(row=i, column=1+k, padx=10, pady=10)
          self.empTipShift[employeeName].append(shift)

        paycheck = Label(self.empFrame, text="")
        paycheck.grid(row=i+1, column=1)
        self.empPaycheck[employeeName] = paycheck

        i += 2

    # tip input / button
    self.tipAmtInput = Entry(self.tipFrame)
    self.tipAmtInput.grid(row=0, column=0, padx=10, pady=10)
    distributeTipBtn = Button(self.tipFrame, text="Distrib. Tip", command=self.distributeTip)
    distributeTipBtn.grid(row=0, column=1, padx=10, pady=10)

    calcBtn = Button(self.root, text="Calculate", command=self.calculate)
    calcBtn.pack(padx=10, pady=10)


  def calculate(self):
    # add all the tips + compute wage for each employee
    # update paycheck
    with open('wage.json') as f:
      data = json.load(f)
    for e, p in self.empPaycheck.items():
      totalWage = data[e] * self.empTime[e] + self.empTip[e]
      p.config(text=f"{data[e]}$/h * {self.empTime[e]}h + {self.empTip[e]}$ = {totalWage:.2f}$")
  
  def distributeTip(self):
    # TODO: allocate tips to each shift
    # spread tips evenly accross employees' shifts
    totalTip = float(self.tipAmtInput.get()) if self.tipAmtInput.get() != "" else 0
    
    totalShiftCnt = 0
    for e, shiftLst in self.empTipShift.items():
      cnt = sum([s.get() for s in shiftLst])
      self.empTip[e] = cnt
      totalShiftCnt += cnt
    
    if totalShiftCnt == 0:
      messagebox.showerror(message=f"Please select at least one shift")  
      return
    tipPerShift = totalTip / totalShiftCnt # float
    for empName, shiftLst in self.empTipShift.items():
      self.empTip[empName] *= tipPerShift

    messagebox.showinfo(title="Tip Distribution", 
    message=f"""{totalTip}$ tip distributed across {totalShiftCnt} shifts.\n
                Each shift will get {tipPerShift:.2f}$!""")

if __name__ == "__main__":
  wc = WageCalculatorApp(names=fetchNames(EMPLOYEE_DIR))
  wc.root.mainloop()