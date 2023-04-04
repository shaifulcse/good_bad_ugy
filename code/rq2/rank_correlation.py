import re
import numpy as np
from scipy.stats.stats import kendalltau
import scipy

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
marks_size = [20, 15, 12, 14, 20, 10, 12, 15]
marker_color = ['#0F52BA', '#ff7518', '#6CA939', '#e34234', '#756bb1', 'brown', '#c994c7', '#636363']
gaps = [5, 4, 2, 3, 5, 4, 4, 4]


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
    slocs = []
    values = []

    file_path = BASE_DATA + "cleaned/" + project + ".txt"
    fr = open(file_path, "r")
    line = fr.readline()
    feature_indexes = build_indexes(line)
    lines = fr.readlines()
    for line in lines:
        method, value, sloc = process_method(line, feature_indexes)
        if method == 'invalid':
            continue
        slocs.append(sloc)
        values.append(value)
    return slocs, values


def process_method(line, feature_indexes):
    values = line.split("\t")
    method = values[feature_indexes['file']].strip()
    age = int(values[0])
    if apply_age_restriction == 1 and age < age_restriction:
        return 'invalid', -1, -1

    diffs = values[feature_indexes['DiffSizes']]
    adds = values[feature_indexes['NewAdditions']]
    edits = values[feature_indexes['EditDistances']]
    bugs = values[feature_indexes['RiskyCommit']]
    change_ages = values[feature_indexes['ChangeAtMethodAge']].split(",")
    slocs = values[feature_indexes['Mcclure']].split(",")
    values = decide_type(diffs, adds, edits, bugs)
    value = calculate_value(values, change_ages)
    sloc = calculate_sloc(slocs)
    return method, value, sloc


def calculate_sloc(slocs):
    return float(slocs[0])


def calculate_value(values, change_ages):
    values = values.split(",")
    value = 0
    for i in range(1, len(values)):
        if int(change_ages[i]) > age_restriction and apply_age_restriction == 1:
            break
        if change_type == 'revision' or change_type == 'bugs':
            if int(values[i]) > 0:
                value = value + 1
        else:
            value = value + int(values[i])

    return value


def decide_type(diffs, adds, edits, bugs):
    if change_type == 'revision' or change_type == 'diffs':
        return diffs

    if change_type == 'adds':
        return adds

    if change_type == 'edits':
        return edits

    if change_type == 'bugs':
        return bugs


def correlation(slocs, values):
    cr = kendalltau(slocs, values)
    #print (cr, cr[0])
    return cr[0]

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]


def draw_graph(STATS):
    index = 0
    change_types = ['revision', 'adds', 'diffs', 'edits']
    for change_type in change_types:
        X, Y = ecdf(STATS[change_type])
        ln = (plt.plot(X, Y))
        plt.setp(ln, linewidth=width[index], ls=styles[index], marker=marks[index], markersize=marks_size[index],
             color=marker_color[index], markevery=gaps[index])
        index += 1

    plt.xlabel("Correlation", fontsize=24)
    plt.ylabel("CDF", fontsize=22)
    # plt.xscale("log")
    for label in ax.get_xticklabels():
        label.set_fontsize(23)
    for label in ax.get_yticklabels():
        label.set_fontsize(23)
    plt.tight_layout()
    plt.grid(True)
    plt.legend(['Revisions', 'Additions', 'Diffs', 'Edits'], loc=0, fontsize=20)
    # plt.xticks(np.arange(0.5, 0.88, 0.1))
    # plt.xlim(0.0, 0.3)
    plt.show()


if __name__ == "__main__":
    global age_restriction
    global change_type

    change_types = ['revision', 'adds', 'diffs', 'edits']
    apply_age_restriction = 1
    age_restriction = 730
    projects = list_projects()

    STATS = {}
    for change_type in change_types:
        STATS[change_type] = []
        for project in projects:
            slocs, values = process(project)
            STATS [change_type].append(correlation(slocs, values))

        print (STATS[change_type])

    draw_graph(STATS)
