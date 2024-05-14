import pytest
import age_selection


def test_find_indexes(path):
    indexes = age_selection.find_indexes(path)
    assert indexes['SLOCStandard'] == 3
    assert indexes['SimpleReadability'] == 6
    assert indexes['n1'] == 16
    assert indexes['ChangeAtMethodAge'] == 40
    assert indexes['DiffSizes'] == 44


def test_count_methods():
    age_vs_number_of_methods = age_selection.count_methods([729, 730, 731, 300, 365, 400])
    assert age_vs_number_of_methods[0] == 6
    assert age_vs_number_of_methods[1] == 5
    assert age_vs_number_of_methods[2] == 2
    age_vs_number_of_methods = age_selection.count_methods([1096, 729, 730, 731, 300, 365, 400, 1095, 1000])
    assert age_vs_number_of_methods[2] == 5
    assert age_vs_number_of_methods[3] == 2


def calculate_years_from_days_with_ceil():
    assert age_selection.calculate_years_from_days_with_ceil(731) == 3
    assert age_selection.calculate_years_from_days_with_ceil(730) == 2
    assert age_selection.calculate_years_from_days_with_ceil(729) == 2
    assert age_selection.calculate_years_from_days_with_ceil(366) == 2
    assert age_selection.calculate_years_from_days_with_ceil(365) == 1
    assert age_selection.calculate_years_from_days_with_ceil(364) == 1


def test_years_from_days():
    assert age_selection.calculate_years_from_days(729) == 1
    assert age_selection.calculate_years_from_days(730) == 2
    assert age_selection.calculate_years_from_days(731) == 2
    assert age_selection.calculate_years_from_days(1094) == 2
    assert age_selection.calculate_years_from_days(1095) == 3
    assert age_selection.calculate_years_from_days(1096) == 3


def test_count_revisions():
    list_revisions = [[0, 2, 0, 3], [0, 0, 5, 4]]
    list_change_dates = [[0, 365, 731, 2000], [0, 400, 366, 1000]]
    revs = age_selection.count_revisions(list_revisions, list_change_dates)
    assert revs[1] == 1
    assert revs[2] == 2
    assert revs[3] == 3
    assert revs[5] == 3
    assert revs[6] == 4


def test_extract_from_file(path):
    given_list_revisions = [[0, 0, 0, 13, 10, 7, 2, 10, 10], [0, 0, 0, 2, 2], [0], [0, 0, 0],
                            [0], [0, 0], [0, 0, 2, 0, 2], [0, 21], [0, 2, 1, 1], [0, 0, 2, 2]
                            ]

    given_ages = [5167, 5167, 2035, 5647, 1165, 1034, 6184, 1908, 1644, 4520]

    indexes = age_selection.find_indexes(path)
    ages, list_revisions, list_change_dates = age_selection.extract_from_file(indexes, path)

    equal = 1
    for i in range (len(given_ages)):
        if given_ages[i] != ages [i]:
            equal = 0
            break
    assert equal == 1

    equal = 1
    for i in range(len(given_list_revisions)):
        given_revisions = given_list_revisions[i]
        revisions = list_revisions[i]
        for j in range(len(revisions)):
            if int(revisions[j]) != given_revisions[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

    given_list_change_dates = [[0, 279, 660, 1002, 1402, 1405, 1419, 1509, 1884],
                               [0, 279, 660, 3043, 3139],
                               [0],
                               [0, 758, 1139],
                               [0],
                               [336],
                               [0, 3934, 4255, 4394, 4473],
                               [0, 1010],
                               [0, 0, 212, 221],
                               [0, 2271, 2800, 3586],
                               ]
    equal = 1
    for i in range(len(given_list_change_dates)):
        given_change_dates = given_list_change_dates[i]
        change_dates = list_change_dates[i]
        for j in range(len(given_change_dates)):
            if int(change_dates[j]) != given_change_dates[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1


if __name__ == '__main__':
    path = "../../data/testing_data/"
    test_find_indexes(path)
    test_years_from_days()
    test_count_methods()
    calculate_years_from_days_with_ceil()
    test_count_revisions()
    test_extract_from_file(path)
