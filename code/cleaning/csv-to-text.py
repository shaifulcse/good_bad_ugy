import re
import os
import time

PROJECTS_LIST = "../../../mydata/info/saved-settings-project-with-first-date.txt"


SRC_PATH="../../../mydata/data/uncleaned/"

DEST_PATH="../../../mydata/data/cleaned/"

def convert():

  for file in os.listdir(SRC_PATH):
    print (file)
    fr = open(SRC_PATH+file,"r")
    lines = fr.readlines()
    fr.close()
    newfile = file.replace(".csv", ".txt")
    fw = open(DEST_PATH+newfile,"w")
    track_header = 0
    c = 0
    for line in lines:
      line = line.strip()
      if track_header == 1:
        problem =  check_problem(line) 
        if problem == 1:
          c+=1
          continue
      fw.write(line+"\n")
      track_header = 1

    print (file, c)
    fw.flush()
    fw.close()
    

def check_problem(line):
  line = line.strip()
  data = re.findall("[^\t]+",line)
      
    
  dates =  data[len(data)-12]
  dates = re.findall("[^,]+",dates)

  
  

  prev = 0
  for d in dates:
    d = int(d)

    if d<0:
      return 1

    if d<prev:
      return 1
    prev = d 
  
  return 0

if __name__ == "__main__":
      
  convert()
