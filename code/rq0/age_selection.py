import os
import matplotlib.pyplot as plt

SRC_PATH = "../../data/cleaned/"
selected_features = ['ChangeAtMethodAge', 'DiffSizes']
age_vs_revisions = {}  # how many revisions we can catch with an age threshold
max_year = 20


def calculate_total_revisions():
    total_revisions = 0
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        fr.close()
        for line in lines:
            data = line.strip().split("\t")
            revisions = data[indexes['DiffSizes']]
            revisions = revisions.split(",")
            for value in revisions:
                if int(value) > 0:
                    total_revisions += 1
    return total_revisions


def calculate_year_based():
    ages = []
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            age = int(data[0])
            ages.append(age)
            #count_revisions(age, data)
    age_vs_number_of_methods = count_methods(ages)
    return age_vs_number_of_methods


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


def count_revisions(age, data):
    global max_year
    revisions = data[indexes['DiffSizes']]
    revisions = revisions.split(",")
    change_dates = data[indexes['ChangeAtMethodAge']]
    change_dates = change_dates.split(",")

    for i in range(0, len(revisions)):
        if int(revisions[i]) > 0:
            day = int(change_dates[i])
            years = int(day / 365)
            for year in range(max_year, years - 1, -1):
                if year not in age_vs_revisions:
                    age_vs_revisions[year] = 1
                else:
                    age_vs_revisions[year] += 1


def find_indexes():
    indexes = {}
    fr = open(SRC_PATH + "ant.txt")
    line = fr.readline()
    fr.close()
    data = line.strip().split("\t")
    for i in range(len(data)):
        indexes[data[i]] = i
    return indexes


if __name__ == "__main__":
    indexes = find_indexes()
    #total_revisions = calculate_total_revisions()
    calculate_year_based()
    #print("total_revisions", total_revisions)
    #print(age_vs_revisions)
