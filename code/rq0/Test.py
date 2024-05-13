import pytest
import age_selection


def test_find_indexes():
    indexes = age_selection.find_indexes()
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
def test_years_from_days():
    assert age_selection.calculate_years_from_days(729) == 1
    assert age_selection.calculate_years_from_days(730) == 2
    assert age_selection.calculate_years_from_days(731) == 2
    assert age_selection.calculate_years_from_days(1094) == 2
    assert age_selection.calculate_years_from_days(1095) == 3
    assert age_selection.calculate_years_from_days(1096) == 3


if __name__ == '__main__':
    test_find_indexes()
    test_years_from_days()
    test_count_methods()
