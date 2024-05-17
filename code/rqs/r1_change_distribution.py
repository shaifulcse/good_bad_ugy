import re
import numpy as np
import matplotlib.pyplot as plt
from util import utility

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


def process(change_type, project):
    methods = {}
    for method in project:
        if utility.apply_age_restriction and project[method]['age'] < utility.age_restriction:
            continue
        method_change = process_method(change_type, project[method])
        if method not in methods:
            methods[method] = method_change
            utility.total_change = utility.total_change + method_change
        else:
            print("This should not happen")
    return methods


def process_method(change_type, method_data):
    change_ages = method_data['ChangeAtMethodAge']
    values = get_change_values_with_type(change_type, method_data)
    diff_values = get_change_values_with_type("diffs", method_data)
    value = calculate_value(change_type, values, diff_values, change_ages)
    return value


def calculate_value(change_type, values, diff_values, change_ages):
    value = 0
    for i in range(1, len(values)):
        if int(change_ages[i]) > utility.age_restriction and utility.apply_age_restriction == 1:
            break
        if change_type == 'revision':
            if int(values[i]) > 0:
                value = value + 1
        elif change_type == 'bugs':
            if int(values[i]) > 0 and int(diff_values[i]) > 0:
                value = value + 1
        else:
            value = value + int(values[i])

    return value


def get_change_values_with_type(change_type, method_data):
    if change_type == 'revision' or change_type == 'diffs':
        return method_data['DiffSizes']
    if change_type == 'adds':
        return method_data['NewAdditions']
    if change_type == 'edits':
        return method_data['EditDistances']

    if change_type == 'bugs':
        return method_data['RiskyCommit']


def analyse(methods):
    print(methods)
    index = 0
    stats = {}
    methods = sorted(methods.items(), key=lambda item: item[1], reverse=True)
    print(methods)
    count_methods = 1.0
    total_methods = len(methods)
    print(total_methods)
    moving_change = 0.0
    for method in methods:
        moving_change += float(method[1])
        current_percent_methods = float(count_methods / total_methods)
        percent_change = float(moving_change / utility.total_change)
        count_methods += 1

        if current_percent_methods * 100 >= given_percent_methods[index]:
            stats[given_percent_methods[index]] = percent_change
            index = index + 1

            if index == len(given_percent_methods):
                break

    return stats
    # print(project, current_percent_methods, percent_change, min, max, name)


def draw_graph(STATS):
    index = 0
    for method_percent in given_percent_methods:
        a = []
        for project in STATS:
            a.append(STATS[project][method_percent])
        X, Y = utility.ecdf(a)
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
    CDF_STATS = {}
    given_percent_methods = [5, 10, 15, 20]
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    change_type = change_types[0]

    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    selected_features = ['ChangeAtMethodAge', 'DiffSizes','NewAdditions','EditDistances','RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)

    for project in project_data:
        utility.total_change = 0
        methods = process(change_type, project_data[project])
        CDF_STATS[project] = analyse(methods)
        break

    #draw_graph(CDF_STATS)
