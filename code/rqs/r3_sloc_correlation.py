import math
from util import utility
from util import graphs
from scipy.stats.stats import kendalltau

import numpy as np


def process(change_type, project):
    methods = {}
    for method in project:
        if utility.apply_age_restriction and project[method]['age'] < utility.age_restriction:
            continue
        method_change, sloc = process_method(change_type, project[method])
        if method not in methods:
            methods[method] = {}
            methods[method]['change'] = method_change
            methods[method]['sloc'] = sloc
        else:
            print("This should not happen")
    return methods


def process_method(change_type, method_data):
    change_ages = method_data['ChangeAtMethodAge']
    values = get_change_values_with_type(change_type, method_data)
    diff_values = get_change_values_with_type("diffs", method_data)
    value = calculate_value(change_type, values, diff_values, change_ages)
    sloc = int(method_data[feature_interest][0])
    return value, sloc


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


def draw_graph(correlations):
    index = 0
    X = []
    Y = []
    for ls in correlations:
        x, y = utility.ecdf(ls)
        X.append(x)
        Y.append(y)
    configs = {}
    configs["x_label"] = "Correlation"
    configs["y_label"] = "CDF"
    configs["legends"] = utility.change_legends
    configs['marker'] = True
    #configs["x_ticks"] = np.arange(20, 110, 10)
    graphs.draw_line_graph_multiple_with_x(X, Y, configs)


def calculate_correlation(a, b):
    cr = kendalltau(a, b)
    return cr[0]


if __name__ == "__main__":
    global feature_interest
    STATS = {}
    change_types = ['revision', 'adds', 'diffs', 'edits']
    change_type = change_types[3]

    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    feature_interest = 'McCabe'
    selected_features = [feature_interest, 'ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances',
                         'RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)
    #print(project_data['checkstyle.txt'])
    all_correlations = []
    for change_type in change_types:
        cr = []
        for project in project_data:

            methods = process(change_type, project_data[project])
            if len(methods) < utility.minimum_required_methods:
                #print("discarded project due to less than 30 samples: ", project)
                continue

            sloc = []
            change = []
            for method in methods:
                sloc.append(methods[method]['sloc'])
                change.append(methods[method]['change'])
            c = calculate_correlation(sloc, change)
            cr.append(calculate_correlation(sloc, change))
        all_correlations.append(cr)

    draw_graph(all_correlations)