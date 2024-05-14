import math
import os
import matplotlib.pyplot as plt

selected_features = ['ChangeAtMethodAge', 'DiffSizes']
max_year = 30


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


if __name__ == "__main__":

    SRC_PATH = "../../data/cleaned/"
    indexes = find_indexes(SRC_PATH)
    ages, list_revisions, list_change_dates = extract_from_file(indexes, SRC_PATH)
    age_vs_revisions = count_revisions(list_revisions, list_change_dates)
    age_vs_number_of_methods = count_methods(ages)

    print (age_vs_number_of_methods[5])
    print(age_vs_revisions[5])

