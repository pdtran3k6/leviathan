import os
import numpy as np
import pickle
import heapq

def fetchNames(fp):
  names = []
  imagesEmployee = os.listdir(fp)
  heapq.heapify(imagesEmployee)
  for img in imagesEmployee:
    names.append(img.split(".")[0])
  return names

def fetchEncodings(empDir, names):
  encs = []
  for name in names:
    encs.append(np.loadtxt(f"{empDir}/{name}.enc", dtype=np.float64))
  return encs