import os
from util import utility
import random

SRC_PATH = utility.BASE_PATH + "/data/ML/train-test/"
DEST_PATH = utility.BASE_PATH + "/data/weka/"


def process(selected_features, indexes, file):
    fr = open(SRC_PATH + file + ".csv", "r")
    fr.readline()  ## ignore header
    lines = fr.readlines()
    fr.close()
    fw = open(DEST_PATH + "weka_"+file+".arff", "w")
    fw.write("@relation bug\n\n")

    for i in range(len(selected_features)):
        fw.write("@attribute " + selected_features[i] + " numeric\n")
    fw.write("@attribute class {good, ugly}\n\n@data\n\n")

    for line in lines:
        line = line.strip()
        data = line.split("\t")
        if data[len(data) - 1] == 'noise' or data[len(data) - 1] == 'bad':
            continue
        for feature in selected_features:
            fw.write(data[indexes[feature]] + ",")
        fw.write(data[len(data) - 1]+"\n")

    fw.close()


if __name__ == "__main__":
    selected_features = [
        "SLOCStandard",
         "CommentCodeRation",
         "Readability",
         "SimpleReadability",
         "NVAR",
         "NCOMP",
         "McCabe",
         "IndentSTD",
         "MaximumBlockDepth",
         "totalFanOut",
         "Length",
         "MaintainabilityIndex",
         "isPublic",
         "isStatic",
         "isGetterSetter",
         "Parameters",
         "LocalVariables"


    ]
    indexes = utility.find_indexes(utility.BASE_PATH + "/data/cleaned/")
    process(selected_features, indexes, "train")
    process(selected_features, indexes, "test")
