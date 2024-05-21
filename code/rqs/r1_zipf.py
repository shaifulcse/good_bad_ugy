import math
from util import utility
from util import graphs
import numpy as np

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
    stats = {}
    methods = sorted(methods.items(), key=lambda item: item[1], reverse=True)
    total_methods = len(methods)
    for percent in utility.given_percent_methods:
        stats[percent] = 0
        num_top_methods = math.ceil((percent / 100) * total_methods)
        count = 0
        moving_change = 0.0
        for method in methods:
            moving_change += float(method[1])
            count += 1
            if count <= num_top_methods:
                stats[percent] = float(moving_change / utility.total_change)
            else:
                break

    return stats
    # print(project, current_percent_methods, percent_change, min, max, name)


def draw_graph(STATS):
    Y = []
    X = []
    methods = sorted(STATS['hadoop.txt'].items(), key=lambda item: item[1], reverse=True)
    a = []
    for method in methods:
        a.append(int(method[1]))
    Y.append(a)
    X.append(range(1, len(a)+1))

    methods = sorted(STATS['checkstyle.txt'].items(), key=lambda item: item[1], reverse=True)
    a = []
    for method in methods:
        a.append(int(method[1]))
    Y.append(a)
    X.append(range(1, len(a)+1))

    methods = sorted(STATS['jna.txt'].items(), key=lambda item: item[1], reverse=True)
    a = []
    for method in methods:
        a.append(int(method[1]))
    Y.append(a)
    X.append(range(1, len(a) + 1))

    methods = sorted(STATS['ant.txt'].items(), key=lambda item: item[1], reverse=True)
    a = []
    for method in methods:
        a.append(int(method[1]))
    Y.append(a)
    X.append(range(1, len(a) + 1))

    methods = sorted(STATS['intellij-community.txt'].items(), key=lambda item: item[1], reverse=True)
    a = []
    for method in methods:
        a.append(int(method[1]))
    Y.append(a)
    X.append(range(1, len(a) + 1))
    index = 0
    configs = {}
    configs["x_label"] = "Rank"
    configs["y_label"] = "EditDistances"
    configs["legends"] = ['hadoop', 'checkstyle', 'jna', 'ant', 'intellij']
    configs["xscale"] = True
    configs["yscale"] = True
    #configs["x_ticks"] = np.arange(20, 110, 10)
    graphs.draw_line_graph_multiple_with_x(X, Y, configs)


if __name__ == "__main__":
    STATS = {}
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    change_type = change_types[3]

    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    selected_features = ['ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances', 'RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)

    for project in project_data:
        utility.total_change = 0
        methods = process(change_type, project_data[project])
        if len(methods) < utility.minimum_required_methods:
            print("discarded project due to less than 30 samples: ", project)
            continue
        STATS[project] = methods
    draw_graph(STATS)
