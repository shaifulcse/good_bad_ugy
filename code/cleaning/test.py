import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from  scipy import stats
from matplotlib.patches import Rectangle

fig = plt.figure()
ax = fig.add_subplot(111)



SRC_PATH="../../data/cleaned/"


def check():
  fr = open(SRC_PATH + "ant.txt")
  lines = fr.readlines()
  
  for line in lines:
    print (line) 

if __name__ == "__main__":
      
  check()
