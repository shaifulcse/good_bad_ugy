import re
import os
import matplotlib.pyplot as plt
import re
import numpy as np

SRC_PATH = "../../data/cleaned/"
selected_features = ['ChangeAtMethodAge', 'DiffSizes']
age_vs_methods = {}  # how many methods we can catch with an age threshold
age_vs_revisions = {}  # how many revisions we can catch with an age threshold
indexes = {}
total_revisions = 0
max_year = 20


def calculate_total_revisions():
    global total_revisions
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        fr.close()
        for line in lines:
            data = line.strip().split("\t")
            revisions = data[indexes['DiffSizes']]
            revisions = revisions.split(",")
            for value in revisions:
                if int(value) > 0:
                    total_revisions += 1


def calculate_year_based():
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            age = int(data[0])
            count_methods(age)
            count_revisions(age, data)


def count_methods(age):
    years = int(age / 365)
    for year in range(0, years + 1):
        if year not in age_vs_methods:
            age_vs_methods[year] = 1
        else:
            age_vs_methods[year] += 1


def count_revisions(age, data):
    global max_year
    revisions = data[indexes['DiffSizes']]
    revisions = revisions.split(",")
    change_dates = data[indexes['ChangeAtMethodAge']]
    change_dates = change_dates.split(",")

    for i in range(0, len(revisions)):
        if int(revisions[i]) > 0:
            day = int(change_dates[i])
            years = int(day / 365)
            for year in range(max_year, years - 1, -1):
                if year not in age_vs_revisions:
                    age_vs_revisions[year] = 1
                else:
                    age_vs_revisions[year] += 1


def find_indexes():
    fr = open(SRC_PATH + "ant.txt")
    line = fr.readline()
    fr.close()
    data = line.strip().split("\t")
    for f in selected_features:
        for i in range(len(data)):
            if f == data[i]:
                indexes[f] = i
                break


if __name__ == "__main__":
    find_indexes()
    calculate_total_revisions()
    calculate_year_based()
    print("total_revisions", total_revisions)
    print(age_vs_revisions)
