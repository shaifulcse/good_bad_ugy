"""
We are categorizing methods into ugly, good, bad, and noise.. top x% are ugly.
0 changes are good. In between are bad, but if change is not at least 10% lower than ugly, then
it's a noise.

The first two fields, project and file, are there for debugging. the second last feature, changevlaue is there for debugging
We must remove these three fields while doing ML modeling
"""
from util import utility


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


def check_threshold(methods):
    method_type = {}
    methods = sorted(methods.items(), key=lambda item: item[1]['change'], reverse=True)
    a = []
    b = []
    total_methods = len(methods)
    ugly_range = int((top_methods / 100) * total_methods)

    c = 0
    for method in methods:
        change_value = method[1]['change']
        method_name = method[0]
        method_type[method_name] = {}
        method_type[method_name]['change'] = change_value
        c += 1
        if c <= ugly_range:
            method_type[method_name]['type'] = 'ugly'
            ugly_threshold = change_value
        ## due to sorting, we come here after done with ugly
        elif change_value == 0:
            method_type[method_name]['type'] = 'good'
        elif change_value <= int((10 / 100) * ugly_threshold):
            method_type[method_name]['type'] = 'bad'
        else:
            method_type[method_name]['type'] = 'noise'
    print(ugly_threshold)
    print(methods[ugly_range][1]['change'])
    #print(b[int(percent)], b[int((30 / 100) * total_methods)])
    return method_type


def write_to_file(project, SRC_PATH, DEST_PATH, method_type, indexes, feature_to_write):
    fr = open(SRC_PATH + project)
    fw = open(DEST_PATH + project[:-4]+".csv", "w")
    header = fr.readline().strip()  # read the header

    fw.write("Project\t")
    for feature in feature_to_write:
        fw.write(feature + "\t")
    fw.write("ChangeValue\tType\n")

    lines = fr.readlines()
    fr.close()
    for line in lines:
        data = line.strip().split("\t")
        method = data[indexes['file']]

        if method in method_type:
            fw.write(project[:-4] + "\t")
            for feature in feature_to_write:
                index = indexes[feature]
                values = data[index].split(",")
                fw.write(values[0] + "\t")
            fw.write(str(method_type[method]['change']) + "\t" + method_type[method]['type'] + "\n")

            #
    fw.close()



if __name__ == "__main__":
    global feature_interest
    global top_methods
    top_methods = 20

    feature_to_write = [ "file",
                         "SLOCAsItIs",
                         "SLOCNoCommentPrettyPrinter",
                         "SLOCStandard",
                         "CommentCodeRation",
                         "Readability",
                         "SimpleReadability",
                         "NVAR",
                         "NCOMP",
                         "Mcclure",
                         "McCabe",
                         "McCabeWOCases",
                         "IndentSTD",
                         "MaximumBlockDepth",
                         "totalFanOut",
                         "uniqueFanOut",
                         "n1",
                         "n2",
                         "N1",
                         "N2",
                         "Vocabulary",
                         "Length",
                         "Volume",
                         "Difficulty",
                         "Effort",
                         "Time",
                         "HalsteadBugs",
                         "MaintainabilityIndex",
                         "isPrivate",
                         "isProtected",
                         "isDefault",
                         "isPublic",
                         "isStatic",
                         "isAbstract",
                         "isGetterSetter",
                         "Parameters",
                         "LocalVariables",
                         "EnclosedExpressions",
                         "MaxEnclosedNesting",
                        ]
    method_type = {}
    change_types = ['revision', 'adds', 'diffs', 'edits']
    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"
    DEST_PATH = utility.BASE_PATH + "/data/ML/all/"
    feature_interest = 'McCabe'

    selected_features = [feature_interest, 'ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances',
                         'RiskyCommit', 'file']

    indexes = utility.find_indexes(SRC_PATH)
    project_data = utility.extract_from_file_with_project(indexes, SRC_PATH, selected_features)
    all_overlaps = []
    change_type = 'edits'
    for project in project_data:
        #if project != 'checkstyle.txt':
        #    continue
        methods = process(change_type, project_data[project])
        if len(methods) < utility.minimum_required_methods:
            #print("discarded project due to less than 30 samples: ", project)
            continue
        method_type = check_threshold(methods)
        print(project)
        write_to_file(project, SRC_PATH, DEST_PATH, method_type, indexes, feature_to_write)

