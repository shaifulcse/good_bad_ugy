import math
from util import utility
from util import graphs


def process(change_type, project):
    methods = {}
    for method in project:
        if utility.apply_age_restriction and project[method]['age'] < utility.age_restriction:
            continue
        method_change = process_method(change_type, project[method])
        bugs = process_method("bugs", project[method])
        if method not in methods:
            methods[method] = {}
            methods[method]['change'] = method_change
            methods[method]['bugs'] = bugs
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


def draw_graph(STATS):
    index = 0
    X = []
    Y = []
    for method_percent in utility.given_percent_methods:
        a = []
        for project in STATS:
            a.append(STATS[project][method_percent])
        x, y = utility.ecdf(a)
        X.append(x * 100)
        Y.append(y)
    print(len(X), len(Y))
    configs = {}
    configs["x_label"] = "Coverage"
    configs["y_label"] = "CDF"
    configs["legends"] = utility.given_percent_methods
    #configs["x_ticks"] = np.arange(20, 110, 10)
    graphs.draw_line_graph_multiple_with_x(X, Y, configs)


def bug_distribution(methods):
    stats = {}
    methods = sorted(methods.items(), key=lambda item: item[1]['change'], reverse=True)
    total_bugs = 0
    for method in methods:
        total_bugs += method[1]['bugs']
    total_methods = len(methods)
    for percent in utility.given_percent_methods:
        stats[percent] = 0
        num_top_methods = math.ceil((percent / 100) * total_methods)
        count = 0
        moving_bugs = 0.0
        for method in methods:
            moving_bugs += float(method[1]['bugs'])
            count += 1
            if count <= num_top_methods:
                stats[percent] = float(moving_bugs / total_bugs)
            else:
                break

    return stats

def draw_graph(STATS):
    index = 0
    X = []
    Y = []
    for method_percent in utility.given_percent_methods:
        a = []
        for project in STATS:
            a.append(STATS[project][method_percent])
        x, y = utility.ecdf(a)
        X.append(x * 100)
        Y.append(y)
    configs = {}
    configs["x_label"] = "Coverage"
    configs["y_label"] = "CDF"
    configs["legends"] = utility.given_percent_methods
    configs['marker'] = True
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
        methods = process(change_type, project_data[project])
        STATS[project] = bug_distribution(methods)
    draw_graph(STATS)
    #print(STATS)
