import os
from util import utility
import random

SRC_PATH = utility.BASE_PATH + "/data/ML/all/"
DEST_PATH = utility.BASE_PATH + "/data/ML/train-test/"


def split():
    training_files, test_files = select_train_test()
    print(training_files)
    print(len(training_files))
    print(test_files)
    print(len(test_files))

    f_train = open(DEST_PATH + "train.csv", "w")
    f_test = open(DEST_PATH + "test.csv", "w")
    f_all = open(DEST_PATH + "all.csv", "w")
    fr = open(SRC_PATH + 'checkstyle.csv')
    header = fr.readline()
    f_train.write(header.strip() + "\n")
    f_test.write(header.strip() + "\n")
    f_all.write(header.strip() + "\n")
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
            f_all.write(line.strip() + "\n")
        fr.close()
    fw.close()
    f_all.close()
def select_train_test():
    train = []
    test = []
    files = []
    for file in os.listdir(SRC_PATH):
        files.append(file)
    random.seed(0)

    #train = random.sample(files, int((90 / 100) * len(files)))
    train = ['hibernate-search.csv', 'facebook-android-sdk.csv', 'checkstyle.csv', 'lucene-solr.csv', 'junit4.csv', 'atmosphere.csv', 'jgit.csv', 'wicket.csv', 'netty.csv', 'elasticsearch.csv', 'cassandra.csv', 'lombok.csv', 'docx4j.csv', 'mongo-java-driver.csv', 'commons-lang.csv', 'voldemort.csv', 'ant.csv', 'sonarqube.csv', 'flink.csv', 'intellij-community.csv', 'weka.csv', 'xerces2-j.csv', 'hadoop.csv', 'hibernate-orm.csv', 'spring-boot.csv', 'wildfly.csv', 'presto.csv', 'hbase.csv', 'argouml.csv', 'eclipseJdt.csv', 'jna.csv', 'spring-framework.csv', 'commons-io.csv', 'jclouds.csv', 'cucumber-jvm.csv', 'guava.csv']

    for file in files:
        if file not in train:
            test.append(file)

    return train, test


if __name__ == "__main__":
    split()
