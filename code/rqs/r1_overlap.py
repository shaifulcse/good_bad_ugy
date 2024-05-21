"""
size(intersaction) / size (union) when top 20% methods are selected
based on two change types
"""
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


def overlap(methods1, methods2):
    methods1 = sorted(methods1.items(), key=lambda item: item[1], reverse=True)
    methods2 = sorted(methods2.items(), key=lambda item: item[1], reverse=True)

    a = set()
    b = set()
    total_methods  = len(methods1)
    percent = int((20/100) * total_methods)
    c = 0
    for method in methods1:
        a.add(method[0])
        c += 1
        if c > percent:
            break
    c = 0
    for method in methods2:
        b.add(method[0])
        c += 1
        if c > percent:
            break
    print (len(a.intersection(b)) / len(a.union(b)))
    # print(project, current_percent_methods, percent_change, min, max, name)


if __name__ == "__main__":
    STATS = {}
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    change_type1 = change_types[2]
    change_type2 = change_types[3]
    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    selected_features = ['ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances', 'RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)

    for project in project_data:
        utility.total_change = 0
        methods1 = process(change_type1, project_data[project])
        utility.total_change = 0
        methods2 = process(change_type2, project_data[project])
        if len(methods1) < utility.minimum_required_methods:
            #print("discarded project due to less than 30 samples: ", project)
            continue
        overlap(methods1, methods2)

