import re

BASE_DATA = "../../data/"
PROJECTS_LIST = BASE_DATA + "info/saved-settings-project-with-first-date.txt"

# RESULT_PATH="../../data/complexity-and-change-data/"

PROJECTS = {}

styles = ['-', '--', '-.', ':']
colors = ['r', 'g', 'b', 'y']
styles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
marks = ["^", "d", "o", "v", "p", "s", "<", ">"]
# marks_size=[15, 17, 10, 15, 17, 10, 12,15]
marks_size = [15, 17, 10, 15, 17, 10, 12, 15]
marker_color = ['#0F52BA', '#ff7518', '#6CA939', '#e34234', '#756bb1', 'brown', '#c994c7', '#636363']

gap = [5, 5, 3, 4, 5, 5]


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
    total_change = 0
    for line in lines:
        method, value, total_change = process_method(line, feature_indexes, total_change)
        if method not in methods:
            methods[method] = value
    return methods, total_change


def process_method(line, feature_indexes, total_change):
    values = line.split("\t")
    method = values[feature_indexes['file']].strip()
    diffs = values[feature_indexes['DiffSizes']]
    adds = values[feature_indexes['NewAdditions']]
    edits = values[feature_indexes['EditDistances']]
    values = decide_type(diffs, adds, edits)
    value = calculate_value(values)
    total_change = total_change + value
    return method, value, total_change


def calculate_value(values):
    values = values.split(",")

    value = 0
    for i in range(1, len(values)):
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


def analyse(project, methods, total_change):
    methods = sorted(methods.items(), key=lambda item: item[1], reverse=True)
    # for method in methods
    # print (methods)
    # print (methods)
    # print(project)
    count = 1.0
    total_methods = len(methods)
    moving_change = 0.0
    for method in methods:
        moving_change += method[1]
        percent_methods = float(count / total_methods)
        percent_change = float(moving_change / total_change)
        count += 1
        if percent_change >= 0.8:
            break
    print(project, percent_methods, percent_change)


if __name__ == "__main__":

    # TODO we did not use age restriction yet
    global age_restriction
    global change_type
    change_type = 'revision'
    apply_age_restriction = 1
    age_restriction = 730

    projects = list_projects()
    for project in projects:
        methods, total_change = process(project)
        analyse(project, methods, total_change)
