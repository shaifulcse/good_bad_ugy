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
        if apply_age_restriction and project[method]['age'] < age_restriction:
            continue
        method_change = process_method(change_type, project[method])
        if method not in methods:
            methods[method] = method_change
        else:
            print("This should not happen")
    return methods

    # for project in project_data:
    #     #print(project)
    #     methods = {}
    #     list_values = get_change_values_with_type(change_type, project_data[project])
    #     for i in range(len(list_values)):
    #         method = project_data[project]['file'][i]
    #         values = list_values[i]
    #         change_dates = project_data[project]['ChangeAtMethodAge'][i]
    #         age = project_data[project]['ages'][i]
    #         #process_method(age, change_type, values, change_dates)
    #         print (project, method, age, values)

def process_method(change_type, method_data):
    global total_change
    change_ages = method_data['ChangeAtMethodAge']
    values = get_change_values_with_type(change_type, method_data)
    value = calculate_value(values, change_ages)
    total_change = total_change + value
    return value


def calculate_value(values, change_ages):
    #values = values.split(",")
    #change_ages = change_ages.split(",")
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


def get_change_values_with_type(change_type, method_data):

    if change_type == 'revision' or change_type == 'diffs':
        return method_data['DiffSizes']
    if change_type == 'adds':
        return method_data['NewAdditions']
    if change_type == 'edits':
        return method_data['EditDistances']

    if change_type == 'bugs':
        return method_data['RiskyCommit']


def analyse(project, methods, total_change):
    index = 0
    stats = {}
    methods = sorted(methods.items(), key=lambda item: item[1], reverse=True)
    count_methods = 1.0
    total_methods = len(methods)
    moving_change = 0.0
    for method in methods:
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
    global total_change
    CDF_STATS = {}
    given_percent_methods = [5, 10, 15, 20]
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    change_type = change_types[0]
    apply_age_restriction = True
    age_restriction = 2 * 365
    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    selected_features = ['ChangeAtMethodAge', 'DiffSizes','NewAdditions','EditDistances','RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)
    for project in project_data:
        total_change = 0
        methods = process(change_type, project_data[project])
        CDF_STATS[project] = analyse(project, methods, total_change)

    draw_graph(CDF_STATS)
