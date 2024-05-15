import math
import os
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111)

styles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]
marks = ["^", "d", "o", "v", "p", "s", "<", ">"]
width = [3, 3, 3, 3, 3, 3, 3, 3]
marks_size = [20, 20, 20, 20, 20, 10, 12, 15]
marker_color = ['#0F52BA', '#ff7518', '#6CA939', '#e34234', '#756bb1', 'brown', '#c994c7', '#636363']
gaps = [4, 4, 4, 4, 4, 4, 4, 4]

selected_features = ['ChangeAtMethodAge', 'DiffSizes']


def extract_from_file(indexes, SRC_PATH):
    ages = []
    list_change_dates = []
    list_revisions = []
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            age = int(data[0])
            ages.append(age)
            revisions = data[indexes['DiffSizes']]
            revisions = revisions.split(",")
            list_revisions.append(revisions)
            change_dates = data[indexes['ChangeAtMethodAge']]
            change_dates = change_dates.split(",")
            list_change_dates.append(change_dates)

    return ages, list_revisions, list_change_dates


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
                years = calculate_years_from_days_with_ceil(day)
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
        years = calculate_years_from_days(age)

        for year in range(0, years + 1):
            if year not in age_vs_number_of_methods:
                age_vs_number_of_methods[year] = 1
            else:
                age_vs_number_of_methods[year] += 1
    return age_vs_number_of_methods


def calculate_years_from_days(days):
    years = int(days / 365)
    return years


def calculate_years_from_days_with_ceil(days):
    years = math.ceil(float(days / 365))
    return int(years)


def find_indexes(SRC_PATH):
    indexes = {}
    fr = open(SRC_PATH + "checkstyle.txt")
    line = fr.readline()
    fr.close()
    data = line.strip().split("\t")
    for i in range(len(data)):
        indexes[data[i]] = i
    return indexes


def draw_graph(methods, revisions):
    ln = (plt.plot(range(1, len(methods)+1), methods))
    plt.setp(ln, linewidth=width[0], ls=styles[0], color=marker_color[0])

    ln = (plt.plot(range(1, len(revisions) + 1), revisions))
    plt.setp(ln, linewidth=width[1], ls=styles[1], color=marker_color[1])

    plt.xlabel("Year", fontsize=24)
    plt.ylabel("Percent", fontsize=22)
    plt.legend(['Methods', 'Revisions'], loc=0, fontsize=20)
    #plt.xscale("log")
    #plt.yscale("log")

    for label in ax.get_xticklabels():
        label.set_fontsize(20)
    for label in ax.get_yticklabels():
        label.set_fontsize(20)
    plt.tight_layout()
    plt.grid(True)
    plt.xticks(np.arange(1, draw_upto + 1, 1))
    # plt.xlim(0.0, 0.3)
    plt.show()


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
    global max_year
    max_year = 20
    SRC_PATH = "../../data/cleaned/"
    indexes = find_indexes(SRC_PATH)
    ages, list_revisions, list_change_dates = extract_from_file(indexes, SRC_PATH)
    age_vs_revisions = count_revisions(list_revisions, list_change_dates)
    age_vs_number_of_methods = count_methods(ages)
    methods, revisions = prepare_for_drawing(age_vs_number_of_methods, age_vs_revisions)
    print(age_vs_number_of_methods[5], 100 * (age_vs_number_of_methods[5] / age_vs_number_of_methods[0]))
    print(age_vs_revisions[5], 100 * (age_vs_revisions[5] / age_vs_revisions[max_year]))
    #print(methods)
    #print(revisions)
    draw_graph(methods, revisions)
