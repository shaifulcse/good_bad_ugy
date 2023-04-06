import re
import numpy as np

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

BASE_DATA = "../../data/"
PROJECTS_LIST = BASE_DATA + "info/saved-settings-project-with-first-date.txt"

# RESULT_PATH="../../data/complexity-and-change-data/"

PROJECTS = {}

styles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
marks = ["^", "d", "o", "v", "p", "s", "<", ">"]
width = [3, 3, 3, 3, 3, 3, 3, 3]
marks_size = [20, 20, 20, 20, 20, 10, 12, 15]
marker_color = ['#0F52BA', '#ff7518', '#6CA939', '#e34234', '#756bb1', 'brown', '#c994c7', '#636363']
gaps = [4, 4, 4, 4, 4, 4, 4, 4]


def list_projects():
    projects = {}
    fr = open(PROJECTS_LIST, "r")
    lines = fr.readlines()
    fr.close()
    for line in lines:

        line = line.strip()
        data = re.findall("[^\t]+", line)
        if data[0] not in projects:
            projects[data[0]] = 1
    return projects


def build_indexes(line):
    feature_indexes = {}
    headers = line.split("\t")
    for i in range(len(headers)):
        feature_indexes[headers[i].strip()] = i
    return feature_indexes


def process(project):
    methods = {}
    file_path = BASE_DATA + "cleaned/" + project + ".txt"
    fr = open(file_path, "r")
    line = fr.readline()
    feature_indexes = build_indexes(line)
    lines = fr.readlines()
    for line in lines:
        method, changes = process_method(line, feature_indexes)
        if method == 'invalid':
            continue
        if method not in methods:
            methods[method] = changes

    return methods


def process_method(line, feature_indexes):
    values = line.split("\t")
    method = values[feature_indexes['file']].strip()
    age = int(values[0])
    if apply_age_restriction == 1 and age < age_restriction:
        return 'invalid', -1

    diffs = values[feature_indexes['DiffSizes']]
    adds = values[feature_indexes['NewAdditions']]
    edits = values[feature_indexes['EditDistances']]
    change_ages = values[feature_indexes['ChangeAtMethodAge']].split(",")
    change_values = decide_type(diffs, adds, edits)
    changes = calculate_value(change_values, change_ages)
    return method, changes


def calculate_value(values, change_ages):
    values = values.split(",")
    value = 0
    for i in range(1, len(values)):
        if int(change_ages[i]) > age_restriction and apply_age_restriction == 1:
            break
        if change_type == 'revision':
            if int(values[i]) > 0:
                value = value + 1
        else:
            value = value + int(values[i])

    return value


def decide_type(diffs, adds, edits):
    if change_type == 'revision' or change_type == 'diffs':
        return diffs

    if change_type == 'adds':
        return adds

    if change_type == 'edits':
        return edits


def analyze(STATS):

    print ("######################\nproject %ugly %bad %ugly")
    for project in STATS:
        methods = sorted(STATS[project].items(), key=lambda item: item[1], reverse=True)
        total_changes = 0
        for method in methods:
            total_changes = total_changes + int(method[1])

        saved_ugly_methods, saved_ugly_changes = calculate_ugly_methods(total_changes, methods)
        saved_bad_methods, saved_bad_changes = calculate_bad_methods(saved_ugly_changes[len(saved_ugly_changes) - 1],
                                                                     methods)
        saved_good_methods, saved_good_changes = calculate_good_methods(methods)

        percent_ugly = float (len(saved_ugly_methods)) / float (len(methods))
        percent_bad = float(len(saved_bad_methods)) / float(len(methods))
        percent_good = float(len(saved_good_methods)) / float(len(methods))
        print(project, percent_ugly, percent_bad, percent_good)


def calculate_bad_methods(threshold, methods):
    saved_bad_methods = []
    saved_bad_changes = []
    for method in methods:
        ## good method should not have a equal (threshold) change value to a ugly method
        if (int(method[1]) < threshold) and (int(method[1]) > 0):
            saved_bad_methods.append(method[0])
            saved_bad_changes.append(method[1])
    return saved_bad_methods, saved_bad_changes


def calculate_good_methods(methods):
    saved_good_methods = []
    saved_good_changes = []
    for method in methods:
        if int(method[1]) == 0:
            saved_good_methods.append(method[0])
            saved_good_changes.append(method[1])
    return saved_good_methods, saved_good_changes


def calculate_ugly_methods(total_changes, methods):
    count_methods = 1.0
    total_methods = len(methods)
    saved_ugly_methods = []
    saved_ugly_changes = []
    for method in methods:
        if method not in saved_ugly_methods:
            saved_ugly_methods.append(method[0])
            saved_ugly_changes.append(int(method[1]))
        current_percent_methods = float(count_methods / total_methods)
        count_methods += 1

        if current_percent_methods * 100 >= 20:
            return saved_ugly_methods, saved_ugly_changes


if __name__ == "__main__":
    global given_percent_methods
    STATS = {}
    global age_restriction
    global change_type
    change_types = ['revision', 'adds', 'diffs', 'edits']
    change_type = change_types[0]
    apply_age_restriction = 1
    age_restriction = 730
    projects = list_projects()
    # print(len(projects))

    for project in projects:
        methods = process(project)
        STATS[project] = methods
    analyze(STATS)
