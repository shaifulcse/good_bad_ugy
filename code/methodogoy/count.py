import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from  scipy import stats
from matplotlib.patches import Rectangle

fig = plt.figure()
ax = fig.add_subplot(111)

PROJECTS_LIST = "settings-project.txt"

RESULT_PATH="../../data/cleaned/"

PROJECTS = {}
DIST ={}
feature_to_look = "Age"
AGES={}
MAX = 0

def list_projects():
  fr = open(PROJECTS_LIST,"r")
  lines = fr.readlines()
  fr.close()
  projects = []
  c = 0
  for line in lines:
    if len(line)<5:
      break 
       
    line = line.strip()
    data = re.findall("[^\t]+",line)
    if data[0] not in PROJECTS:
      PROJECTS[data[0]]=data[2]
      ### to help step2

   

def find_index(feature, project):
  fr = open(RESULT_PATH+project+".txt")
  line =  fr.readline() ## header
  line = line.strip()
  data = re.findall("[^\t]+",line)
  for i in range(len(data)):
    if data[i] == feature:
      return i

def parse_age(index, getter_setter_index):
  
  totGetterSetter = 0
  STATS = {}

  for project in PROJECTS:

    STATS[project] = {}
    STATS[project]['getter_setter'] = 0
    STATS[project]['total'] = 0
    STATS[project]['old'] = 0
    STATS[project]['rest'] = 0

    fr = open(RESULT_PATH+project+".txt")
    line =  fr.readline() ## header
    lines = fr.readlines()
    fr.close()
    
    for line in lines:
      STATS[project]['total'] += 1

      line = line.strip()
      data = re.findall("[^\t]+",line)
      age = int(data[index])
      getter_setter = int(data[getter_setter_index][0])
      
      if getter_setter == 1:
        STATS[project]['getter_setter'] += 1
         
      
      if age>=730:
        STATS[project]['old'] += 1
        if getter_setter == 0:
          STATS[project]['rest'] += 1  
    
          #print data[getter_setter_index]
        

  ls =  sorted(STATS.items(), key = lambda x: x[1]['total'], reverse = True)  
 
  tot = 0
  rest = 0
  for p in ls:
    #print "project: ", p[0], "#Methods", p[1]['total'], "#Getter_Setter", p[1]['getter_setter'], "#Old", p[1]['old'], "#Usable", p[1]['rest'], PROJECTS[p[0]][:6]
    print (p[0], "&", decimal_presentation(p[1]['total']), "&", decimal_presentation(p[1]['getter_setter']), "&", decimal_presentation(p[1]['old']), "&", decimal_presentation(p[1]['rest']), "&", "\\texttt{"+PROJECTS[p[0]][:6]+"}","\\\\")
    
    tot += p[1]['total']
    rest += p[1]['rest']
  print ("\\hline")
  print ("\\textbf{Total}", "&", "&", "&", "\\textbf{"+str(tot)+"}", "&", "&", "&", str(rest), "&","\\\\")
  print (tot, rest)

def decimal_presentation(number):
  if len(str(number))<4:
    return number
  else:
    return str(number)[:len(str(number))-3]+","+ str(number)[len(str(number))-3:]

if __name__ == "__main__":
      
  list_projects()
  print ("total projects", len(PROJECTS))
  index = find_index("Age", "checkstyle")
  getter_setter_index = find_index("isGetterSetter", "checkstyle")
  parse_age(index, getter_setter_index)
 
