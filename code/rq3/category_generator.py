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
    header = fr.readline()
    feature_indexes = build_indexes(header)
    lines = fr.readlines()
    for line in lines:
        method, changes, age = process_method(line, feature_indexes)
        # if method == 'invalid':
        #    continue
        if method not in methods:
            methods[method] = {}
            methods[method]['changes'] = changes
            methods[method]['age'] = age

    return methods


def process_method(line, feature_indexes):
    values = line.split("\t")
    method = values[feature_indexes['file']].strip()
    age = int(values[0])
    # if apply_age_restriction == 1 and age < age_restriction:
    #    return 'invalid', -1

    diffs = values[feature_indexes['DiffSizes']]
    adds = values[feature_indexes['NewAdditions']]
    edits = values[feature_indexes['EditDistances']]
    change_ages = values[feature_indexes['ChangeAtMethodAge']].split(",")
    change_values = decide_type(diffs, adds, edits)
    changes = calculate_value(change_values, change_ages)
    return method, changes, age


def calculate_value(values, change_ages):
    values = values.split(",")
    value = 0
    for i in range(1, len(values)):
        # if int(change_ages[i]) > age_restriction and apply_age_restriction == 1:
        #    break
        if change_type == 'revision':
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


def save_category(STATS):
    for project in STATS:
        print(project)
        methods = sorted(STATS[project].items(), key=lambda item: item[1]['changes'], reverse=True)
        total_changes = 0
        for method in methods:
            total_changes = total_changes + int(method[1]['changes'])

        method_categories = {}
        saved_ugly_methods, saved_ugly_changes = calculate_ugly_methods(total_changes, methods, method_categories)
        saved_bad_methods, saved_bad_changes = calculate_bad_methods(saved_ugly_changes[len(saved_ugly_changes) - 1],
                                                                     methods, method_categories)
        saved_good_methods, saved_good_changes = calculate_good_methods(methods, method_categories)

        file_path = BASE_DATA + "cleaned/" + project + ".txt"
        fr = open(file_path, "r")
        header = fr.readline()
        feature_indexes = build_indexes(header)
        lines = fr.readlines()
        write_header(header, project)
        file_index = feature_indexes['file']
        write_values(lines, file_index, method_categories, project)


def write_values(lines, file_index, method_categories, project):
    fw_csv = open(BASE_DATA + "tmp_categorized/csv/" + project + ".csv", "a")
    fw_txt = open(BASE_DATA + "tmp_categorized/txt/" + project + ".txt", "a")
    for line in lines:

        values = line.split("\t")
        file = values[file_index]
        if file.strip() not in method_categories:
            category = "Undecided"  ### limited by age_limit, or has change equals to the last ugly method
        else:
            category = method_categories[file.strip()]
        fw_csv.write(line.strip() + "\t" + category + "\n")

        fw_txt.write(line.strip() + "\t" + category + "\n")
    fw_csv.close()
    fw_txt.close()


def write_header(header, project):
    fw = open(BASE_DATA + "tmp_categorized/csv/" + project + ".csv", "w")
    fw.write(header.strip() + "\t" + "Category\n")
    fw.close()

    fw = open(BASE_DATA + "tmp_categorized/txt/" + project + ".txt", "w")
    fw.write(header.strip() + "\t" + "Category\n")
    fw.close()


def calculate_bad_methods(threshold, methods, method_categories):
    print(threshold)
    saved_bad_methods = []
    saved_bad_changes = []
    for method in methods:

        ## good method should not have a equal (threshold) change value to a ugly method
        if (int(method[1]['changes']) <= good_upper_bound) and \
                (int(method[1]['changes']) > 0) and (int(method[1]['age'] >= age_limit)):
            saved_bad_methods.append(method[0])
            method_categories[method[0]] = 'Bad'
            saved_bad_changes.append(method[1]['changes'])
    return saved_bad_methods, saved_bad_changes


def calculate_good_methods(methods, method_categories):
    ## good method ---  0 change in its whole life, and at least 2 years old
    saved_good_methods = []
    saved_good_changes = []
    for method in methods:
        if int(method[1]['changes']) == 0 and int(method[1]['age']) >= age_limit:
            saved_good_methods.append(method[0])
            method_categories[method[0]] = 'Good'
            saved_good_changes.append(method[1]['changes'])
    return saved_good_methods, saved_good_changes


def calculate_ugly_methods(total_changes, methods, method_categories):
    ##  in top 20%, but we discard methods with 1 or 2 changes only
    count_methods = 1.0
    total_methods = len(methods)
    saved_ugly_methods = []
    saved_ugly_changes = []
    for method in methods:
        if int(method[1]['changes']) < ugly_lower_bound:
            continue
        if method not in saved_ugly_methods:
            saved_ugly_methods.append(method[0])
            method_categories[method[0]] = 'Ugly'
            saved_ugly_changes.append(int(method[1]['changes']))
        current_percent_methods = float(count_methods / total_methods)
        count_methods += 1

        if current_percent_methods * 100 >= 20:
            break
    return saved_ugly_methods, saved_ugly_changes


if __name__ == "__main__":
    global given_percent_methods
    STATS = {}
    global change_type
    global age_limit
    global ugly_lower_bound
    global good_upper_bound
    ugly_lower_bound = 3
    good_upper_bound = 2
    age_limit = 730
    change_types = ['revision', 'adds', 'diffs', 'edits']
    change_type = change_types[0]
    projects = list_projects()
    # print(len(projects))

    for project in projects:
        methods = process(project)
        STATS[project] = methods
    save_category(STATS)
