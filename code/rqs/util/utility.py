import os
import math

BASE_PATH = "/home/shaiful/research/good_bad_ugy"

def find_indexes(SRC_PATH):
    indexes = {}
    fr = open(SRC_PATH + "checkstyle.txt")
    line = fr.readline()
    fr.close()
    data = line.strip().split("\t")
    for i in range(len(data)):
        indexes[data[i]] = i
    return indexes

def extract_from_file(indexes, SRC_PATH, features):

    collect_fields = {}
    for feature in features:
        collect_fields[feature] = []
    collect_fields["ages"] = []
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            collect_fields["ages"].append(int(data[0]))
            for feature in features:
                collect_fields[feature].append(data[indexes[feature]].split(","))
    return collect_fields

def extract_from_file_with_project (indexes, SRC_PATH, features):

    project_data = {}
    for file in os.listdir(SRC_PATH):
        project_data[file] = {}

        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            method = data[indexes['file']]
            project_data[file][method] = {}
            project_data[file][method]['age'] = int(data[0])

            for feature in features:
                project_data[file][method][feature] = data[indexes[feature]].split(",")
    return project_data

def calculate_years_from_days_with_ceil(days):
    years = math.ceil(float(days / 365))
    return int(years)


def calculate_years_from_days(days):
    years = int(days / 365)
    return years
