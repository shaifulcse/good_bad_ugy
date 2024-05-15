import r0_age_selection
from util import utility


def test_count_methods():
    age_vs_number_of_methods = r0_age_selection.count_methods([729, 730, 731, 300, 365, 400])
    assert age_vs_number_of_methods[0] == 6
    assert age_vs_number_of_methods[1] == 5
    assert age_vs_number_of_methods[2] == 2
    age_vs_number_of_methods = r0_age_selection.count_methods([1096, 729, 730, 731, 300, 365, 400, 1095, 1000])
    assert age_vs_number_of_methods[2] == 5
    assert age_vs_number_of_methods[3] == 2


def test_count_revisions():
    list_revisions = [[0, 2, 0, 3], [0, 0, 5, 4]]
    list_change_dates = [[0, 365, 731, 2000], [0, 400, 366, 1000]]
    revs = r0_age_selection.count_revisions(list_revisions, list_change_dates)
    assert revs[1] == 1
    assert revs[2] == 2
    assert revs[3] == 3
    assert revs[5] == 3
    assert revs[6] == 4


if __name__ == '__main__':
    path = utility.BASE_PATH + "/data/testing_data/"
    test_count_methods()
    test_count_revisions()
