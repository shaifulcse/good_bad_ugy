import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from  scipy import stats
from matplotlib.patches import Rectangle

fig = plt.figure()
ax = fig.add_subplot(111)



SRC_PATH="../../../mydata/data/cleaned/"


dic = {}

def check():
  order_problem = 0
  for file in os.listdir(SRC_PATH):
    #print file
     
    fr = open(SRC_PATH+file,"r")
    line = fr.readline()
    line = line.strip() 

    ln = fieldCheck(line) 

    if ln != 52:
      print (file, "problem with number of fileds")

    hd = HeaderCheck(line)  

    date_index = find_index("ChangeAtMethodAge", "checkstyle")
    lines = fr.readlines()
    for line in lines:
      line = line.strip()
      
      neg = negative(line, date_index)
      if neg == 1:
        print (file, line)
        order_problem += 1
 
      ln = all_field_check(line)
      if ln != 52:
        print ("problem")
    fr.close()
  
  if len(dic) != 1:
    print ("all headers did not match")
  print ("order issues:",order_problem)

def all_field_check(line):
  data =  line.split('\t')
  return len(data)
  
def negative(line, date_index):
  data =  line.split('\t')
  dates =  data[date_index]
  dates =  dates.split(',')
  prev = 0 
  for i in range(len(dates)):
    date = int(dates[i]) 
    if date<0:
      return 1
    if prev > date:
      return 1
    prev = date
  return 0  
      
def HeaderCheck(line):
  if line not in dic:
    dic[line] = 1
  else:
    dic[line] += 1

def fieldCheck(line):
  data =  line.split('\t')
  return len(data)

def find_index(feature, project):
  fr = open(SRC_PATH+project+".txt")
  line =  fr.readline() ## header
  line = line.strip()
  data = re.findall("[^\t]+",line)
  for i in range(len(data)):
    if data[i] == feature:
      return i

    
def check_problem(line):
  line = line.strip()
  data = re.findall("[^\t]+",line)
      
    
  dates =  data[len(data)-5]
  dates = re.findall("[^,]+",dates)

  prev = 0
  for d in dates:
    d = int(d)

    if d<0:
      return 1

    if d<prev:
      return 1
    prev =d 
  
  return 0

if __name__ == "__main__":
      
  check()
