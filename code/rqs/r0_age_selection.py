
import numpy as np
from util import utility
from util import graphs
selected_features = ['ChangeAtMethodAge', 'DiffSizes']
max_year = 20

def count_revisions(list_revisions, list_change_dates):
    """
      given a list of a list of revisions and list of a list of change dates (in days), we count how many revisions can be captured
      with a particular age threshold (in years)
    """
    global max_year
    age_vs_revisions = {}
    for i in range(len(list_revisions)):
        revisions = list_revisions[i]
        change_dates = list_change_dates[i]
        for j in range(len(revisions)):
            if int(revisions[j]) > 0:

                day = int(change_dates[j])
                years = utility.calculate_years_from_days_with_ceil(day)
                for year in range(max_year, years - 1, -1):
                    if year not in age_vs_revisions:
                        age_vs_revisions[year] = 1
                    else:
                        age_vs_revisions[year] += 1
    return age_vs_revisions


def count_methods(ages):
    """
    given a list of ages (in days), we count how many methods can be captured
    with a particular age threshold (in years)
    """
    age_vs_number_of_methods = {}
    for age in ages:
        years = utility.calculate_years_from_days(age)

        for year in range(0, years + 1):
            if year not in age_vs_number_of_methods:
                age_vs_number_of_methods[year] = 1
            else:
                age_vs_number_of_methods[year] += 1
    return age_vs_number_of_methods


def draw_graph(methods, revisions):
    lists = []
    lists.append(methods)
    lists.append(revisions)
    configs = {}
    configs["x_label"] = "Year"
    configs["y_label"] = "Percent"
    configs["legends"] = ["Methods", "Revisions"]
    configs["x_ticks"] = np.arange(1, draw_upto + 1, 1)
    graphs.draw_line_graph(lists, configs)


def prepare_for_drawing(age_vs_number_of_methods, age_vs_revisions):
    global max_year
    global draw_upto
    draw_upto = 10
    methods = []
    revisions = []

    for i in range(1, draw_upto + 1):
        v = 100 * (age_vs_number_of_methods[i] / age_vs_number_of_methods[0])
        methods.append(v)
        v = 100 * (age_vs_revisions[i] / age_vs_revisions[max_year])
        revisions.append(v)

    return methods, revisions


if __name__ == "__main__":
   
    SRC_PATH = utility.BASE_PATH + "/data/cleaned/"

    indexes = utility.find_indexes(SRC_PATH)
    features_values = utility.extract_from_file(indexes, SRC_PATH, selected_features)
    age_vs_revisions = count_revisions(features_values["DiffSizes"], features_values["ChangeAtMethodAge"])
    age_vs_number_of_methods = count_methods(features_values["ages"])
    methods, revisions = prepare_for_drawing(age_vs_number_of_methods, age_vs_revisions)
    print(age_vs_number_of_methods[5], 100 * (age_vs_number_of_methods[5] / age_vs_number_of_methods[0]))
    print(age_vs_revisions[5], 100 * (age_vs_revisions[5] / age_vs_revisions[max_year]))
    draw_graph(methods, revisions)
