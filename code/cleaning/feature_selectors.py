import re
import os
import time

PROJECTS_LIST = "../../../mydata/info/saved-settings-project-with-first-date.txt"


SRC_PATH="../../../mydata/data/cleaned/"

DEST_PATH="../../../mydata/data/cleaned-public/"

features = ["Age", "SLOCStandard", "Readability", "McCabe", "totalFanOut", "MaintainabilityIndex",
            "isGetterSetter", "ChangeAtMethodAge", "NewAdditions", "DiffSizes", "EditDistances", 
            "TangledCommit", "TangledWMoveandFileRename", "Buggycommiit",  "RiskyCommit", "file"]


feature_index = {}

def find_index():
    fr = open(SRC_PATH + "checkstyle" + ".txt")
    line = fr.readline()  # headerfeature_index
    line = line.strip()
    data = re.findall("[^\t]+", line)
    for feature in features:

        for i in range(len(data)):
            if data[i] == feature:
               feature_index[feature] = i
               

def process():

  for file in os.listdir(SRC_PATH):
    print (file)
    fr = open(SRC_PATH + file, "r")
    line = fr.readline()
    lines = fr.readlines()
    fr.close()
    fw = open(DEST_PATH + file, "w")
    headers(fw)
   
    for line in lines:
      data = line.strip().split("\t")
      for feature in features:
        index = feature_index[feature]
        fw.write(data[index] +"\t")
      fw.write("\n")
    fw.close()      
    
    
def headers(fw):

  for feature in features:
    fw.write(feature+"\t")
  fw.write("\n")        

if __name__ == "__main__":
      
  find_index()
  #print (feature_index)
  process()
