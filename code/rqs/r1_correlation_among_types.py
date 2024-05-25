"""
What is the correlation between ranking by revisions and ranking by edits?
"""
from scipy.stats.stats import kendalltau
import math
from util import utility
from util import graphs


def process(change_type1, change_type2, project):
    methods = {}
    for method in project:
        if utility.apply_age_restriction and project[method]['age'] < utility.age_restriction:
            continue
        method_change1 = process_method(change_type1, project[method])
        method_change2 = process_method(change_type2, project[method])
        if method not in methods:
            methods[method] = {}
            methods[method]['change1'] = method_change1
            methods[method]['change2'] = method_change2
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


def calculate_correlations(STATS):
    correlations = []
    for project in STATS:
        a = []
        b = []
        for method in STATS[project]:
            if STATS[project][method]['change1'] == 0 and utility.restrict_zero_revs:
                continue
            a.append(STATS[project][method]['change1'])
            b.append(STATS[project][method]['change2'])
        cr = kendalltau(a, b)
        correlations.append(cr[0])
    return correlations


def draw_graph(X, Y):
    configs = {}
    configs["x_label"] = "Correlation"
    configs["y_label"] = "CDF"
    configs["legends"] = ['Rev-Edit', 'Diff-Edit']
    configs['marker'] = True
    #configs["x_ticks"] = np.arange(20, 110, 10)
    graphs.draw_line_graph_multiple_with_x(X, Y, configs)


if __name__ == "__main__":
    STATS = {}
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']

    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    selected_features = ['ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances', 'RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)

    X = []
    Y = []

    change_type1 = change_types[0]
    change_type2 = change_types[3]
    for project in project_data:
        methods = process(change_type1, change_type2, project_data[project])
        if len(methods) < utility.minimum_required_methods:
            #print("discarded project due to less than 30 samples: ", project)
            continue
        STATS[project] = methods
    correlations = calculate_correlations(STATS)
    x, y = utility.ecdf(correlations)
    X.append(x)
    Y.append(y)

    change_type1 = change_types[2]
    change_type2 = change_types[3]
    for project in project_data:
        methods = process(change_type1, change_type2, project_data[project])
        if len(methods) < utility.minimum_required_methods:
            # print("discarded project due to less than 30 samples: ", project)
            continue
        STATS[project] = methods
    correlations = calculate_correlations(STATS)
    x, y = utility.ecdf(correlations)
    X.append(x)
    Y.append(y)

    draw_graph(X, Y)
