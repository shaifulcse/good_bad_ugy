"""
We are categorizing methods into ugly, good, bad, and noise.. top x% are ugly.
0 changes are good. In between are bad, but if change is not at least 10% lower than ugly, then
it's a noise.

The first two fields, project and file, are there for debugging. the second last feature, changevlaue is there for debugging
We must remove these three fields while doing ML modeling
"""
from util import utility
from scipy.stats.stats import kendalltau
from util import graphs
import numpy as np

def process(change_type, project):
    methods = {}
    for method in project:
        method_change, age = process_method(change_type, project[method])
        if method not in methods:
            methods[method] = {}
            methods[method]['change'] = method_change
            methods[method]['age'] = age
        else:
            print("This should not happen")
    return methods


def process_method(change_type, method_data):
    change_ages = method_data['ChangeAtMethodAge']
    values = get_change_values_with_type(change_type, method_data)
    diff_values = get_change_values_with_type("diffs", method_data)
    value = calculate_value(change_type, values, diff_values, change_ages)
    age = int(method_data['age'])
    return value, age


def calculate_value(change_type, values, diff_values, change_ages):
    value = 0
    for i in range(1, len(values)):

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


def draw_graph(X, Y):
    configs = {}
    configs["x_label"] = "Correlation"
    configs["y_label"] = "CDF"
    #configs["legends"] = ['Rev-Edit', 'Diff-Edit']
    #configs['marker'] = True
    #configs["x_ticks"] = np.arange(20, 110, 10)
    graphs.draw_line_graph_multiple_with_x(X, Y, configs)
def calculate_correlation(methods):
    ages = []
    revs = []
    for method in methods:
        ages.append(methods[method]['age'])
        revs.append(methods[method]['change'])
    cr = kendalltau(ages, revs)
    return cr
    #correlations.append(cr[0])
if __name__ == "__main__":
    global feature_interest

    change_types = ['revision', 'adds', 'diffs', 'edits']
    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    DEST_PATH = utility.BASE_PATH + "/data/ML/all/"

    selected_features = ['ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances',
                         'RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)

    change_type = 'revision'
    correlations = []
    for project in project_data:
        methods = process(change_type, project_data[project])
        cr = calculate_correlation(methods)
        correlations.append(cr[0])
    print(correlations)
    print(np.min(correlations), np.max(correlations))
    x, y = utility.ecdf(correlations)
    X =[]
    Y = []
    X.append(x)
    Y.append(y)
    draw_graph(X, Y)

