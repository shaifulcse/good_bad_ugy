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
    total_change = 0
    c = 0
    for line in lines:
        method, value, total_change = process_method(line, feature_indexes, total_change)
        if method == 'invalid':
            continue
        if method not in methods:
            methods[method] = value
    return methods, total_change


def process_method(line, feature_indexes, total_change):
    values = line.split("\t")
    method = values[feature_indexes['file']].strip()
    age = int(values[0])
    if apply_age_restriction == 1 and age < age_restriction:
        return 'invalid', 0, total_change

    diffs = values[feature_indexes['DiffSizes']]
    adds = values[feature_indexes['NewAdditions']]
    edits = values[feature_indexes['EditDistances']]
    bugs = values[feature_indexes['RiskyCommit']]
    change_ages = values[feature_indexes['ChangeAtMethodAge']].split(",")
    values = decide_type(diffs, adds, edits, bugs)
    value = calculate_value(values, change_ages)
    total_change = total_change + value
    return method, value, total_change


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


def analyse(project, methods, total_change):
    index = 0
    stats = {}
    methods = sorted(methods.items(), key=lambda item: item[1], reverse=True)
    count_methods = 1.0
    total_methods = len(methods)
    moving_change = 0.0
    for method in methods:
       # if method[1] > max:
       #     max = method[1]
       # if method[1] < min:
       #     min = method[1]
        moving_change += float(method[1])
        current_percent_methods = float(count_methods / total_methods)
        percent_change = float(moving_change / total_change)
        #print(count_methods, total_methods, current_percent_methods, moving_change, total_change, percent_change)
        count_methods += 1

        if current_percent_methods * 100 >= given_percent_methods[index]:
            stats[given_percent_methods[index]] = percent_change
            index = index + 1

            if index == len(given_percent_methods):
                break

    return stats
    # print(project, current_percent_methods, percent_change, min, max, name)


def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]


def draw_graph(STATS):
    index = 0
    for method_percent in given_percent_methods:
        a = []
        for project in STATS:
            a.append(STATS[project][method_percent])
        X, Y = ecdf(a)
        ln = (plt.plot(X * 100, Y))
        plt.setp(ln, linewidth=width[index], ls=styles[index], marker=marks[index], markersize=marks_size[index],
                 color=marker_color[index], markevery=gaps[index])
        index += 1

        
    plt.xlabel("Coverage", fontsize=24)
    plt.ylabel("CDF", fontsize=22)
    # plt.xscale("log")
    for label in ax.get_xticklabels():
        label.set_fontsize(23)
    for label in ax.get_yticklabels():
        label.set_fontsize(23)
    plt.tight_layout()
    plt.grid(True)
    plt.legend(given_percent_methods, loc=0, fontsize=20)
    # plt.xticks(np.arange(0.5, 0.88, 0.1))
    # plt.xlim(0.0, 0.3)
    plt.show()


if __name__ == "__main__":
    global given_percent_methods
    global age_restriction
    global change_type
    CDF_STATS = {}
    given_percent_methods = [5, 10, 15, 20]
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    change_type = change_types[4]
    apply_age_restriction = 1
    age_restriction = 2 * 365
    projects = list_projects()

    for project in projects:
        methods, total_change = process(project)
        CDF_STATS[project] = analyse(project, methods, total_change)

    draw_graph(CDF_STATS)
