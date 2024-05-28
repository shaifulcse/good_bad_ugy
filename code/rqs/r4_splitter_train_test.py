import os
from util import utility
import random

SRC_PATH = utility.BASE_PATH + "/data/ML/all/"
DEST_PATH = utility.BASE_PATH + "/data/ML/train-test/"


def split():
    training_files, test_files = select_train_test()
    f_train = open(DEST_PATH + "train.csv", "w")
    f_test = open(DEST_PATH + "test.csv", "w")

    fr = open(SRC_PATH + 'checkstyle.csv')
    header = fr.readline()
    f_train.write(header.strip() + "\n")
    f_test.write(header.strip() + "\n")
    fr.close()
  
    for file in os.listdir(SRC_PATH):
        if file in training_files:
            fw = f_train
        else:
            fw = f_test
        fr = open(SRC_PATH + file)
        fr.readline()
        lines = fr.readlines()
        for line in lines:
            fw.write(line.strip() + "\n")
        fr.close()
    fw.close()

def select_train_test():
    train = set()
    test = set()
    files = []
    for file in os.listdir(SRC_PATH):
        files.append(file)

    random.seed(len(files))
    count = 0
    while count < int((70 / 100) * len(files)):
        index = random.randint(0, len(files) - 1)
        if files[index] not in train:
            train.add(files[index])
            count += 1

    for file in files:
        if file not in train:
            test.add(file)

    return train, test


if __name__ == "__main__":
    split()
