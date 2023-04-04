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
        method, changes, bugs = process_method(line, feature_indexes)
        if method == 'invalid':
            continue
        if method not in methods:
            methods[method] = {}
            methods[method]['changes'] = changes
            methods[method]['bugs'] = bugs

    return methods


def process_method(line, feature_indexes):
    values = line.split("\t")
    method = values[feature_indexes['file']].strip()
    age = int(values[0])
    if apply_age_restriction == 1 and age < age_restriction:
        return 'invalid', -1, -1

    diffs = values[feature_indexes['DiffSizes']]
    adds = values[feature_indexes['NewAdditions']]
    edits = values[feature_indexes['EditDistances']]
    not_conservative_bugs = values[feature_indexes['RiskyCommit']]
    conservative_bugs = values[feature_indexes['Buggycommiit']]
    tangled_commits = values[feature_indexes['TangledWMoveandFileRename']]
    change_ages = values[feature_indexes['ChangeAtMethodAge']].split(",")
    change_values = decide_type(diffs, adds, edits)
    changes = calculate_value(change_values, change_ages)
    if bug_type == 'not_conservative':
        bugs = get_not_conservative_bugs(not_conservative_bugs, change_ages)
    else:
        bugs = get_conservative_bugs(conservative_bugs, change_ages, tangled_commits)

    return method, changes, bugs


def get_conservative_bugs(values, change_ages, tangled_commits):
    values = values.split(",")
    tangled_commits = tangled_commits.split(",")
    value = 0
    for i in range(1, len(values)):
        if int(change_ages[i]) > age_restriction and apply_age_restriction == 1:
            break
        if int(values[i]) > 0 and int(tangled_commits[i]) <= tangle_limit:
            value = value + 1

    return value


def get_not_conservative_bugs(values, change_ages):
    values = values.split(",")
    value = 0
    for i in range(1, len(values)):
        if int(change_ages[i]) > age_restriction and apply_age_restriction == 1:
            break
        if int(values[i]) > 0:
            value = value + 1

    return value


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


def decide_type(diffs, adds, edits):
    if change_type == 'revision' or change_type == 'diffs':
        return diffs

    if change_type == 'adds':
        return adds

    if change_type == 'edits':
        return edits


def calculate(STATS):
    CDF_STATS = {}
    for project in STATS:
        percents = {}
        total_bugs = 0
        methods = sorted(STATS[project].items(), key=lambda item: item[1]['changes'], reverse=True)
        for method in methods:
            total_bugs = total_bugs + method[1]['bugs']

        #print(methods)
        #print(project)
        #break

        count_methods = 1.0
        total_methods = len(methods)
        moving_bugs = 0.0
        index = 0
        for method in methods:
            moving_bugs += float(method[1]['bugs'])
            current_percent_methods = float(count_methods / total_methods)
            percent_bugs = float(moving_bugs / total_bugs)
            count_methods += 1

            if current_percent_methods * 100 >= given_percent_methods[index]:
                percents[given_percent_methods[index]] = percent_bugs
                index = index + 1

                if index == len(given_percent_methods):
                    break
        CDF_STATS[project] = percents

    return CDF_STATS

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]


def draw_graph(CDF_STATS):
    index = 0
    for method_percent in given_percent_methods:
        a = []
        for project in STATS:
            a.append(CDF_STATS[project][method_percent])
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
    STATS = {}
    global age_restriction
    global change_type
    global bug_type
    global total_bugs
    global tangle_limit
    tangle_limit = 1
    bug_type = 'not_conservative'  # 'conservative' or 'not_conservative'
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    given_percent_methods = [5, 10, 15, 20]
    change_type = change_types[3]
    apply_age_restriction = 0
    age_restriction = 730
    projects = list_projects()

    for project in projects:
        methods = process(project)
        STATS[project] = methods

    CDF_STATS = calculate(STATS)
    draw_graph(CDF_STATS)