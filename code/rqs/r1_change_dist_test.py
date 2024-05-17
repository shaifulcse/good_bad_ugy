import r1_change_distribution
from util import utility

def test_get_change_values_with_type():
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    features_values = {}
    features_values['DiffSizes'] = [[1,2,3], [0,5]]
    features_values['RiskyCommit'] = [[0, 1, 0], [1, 0]]
    features_values['NewAdditions'] = [[5, 6, 0], [10, 0]]
    features_values['EditDistances'] = [[15, 16, 30], [10, 1000]]

    list_values = r1_change_distribution.get_change_values_with_type(change_types[4], features_values)
    equal = 1
    for i in range(len(list_values)):
        given_values = features_values['RiskyCommit'][i]
        values = list_values[i]
        for j in range(len(given_values)):
            if int(values[j]) != given_values[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

    list_values = r1_change_distribution.get_change_values_with_type(change_types[2], features_values)
    equal = 1
    for i in range(len(list_values)):
        given_values = features_values['DiffSizes'][i]
        values = list_values[i]
        for j in range(len(given_values)):
            if int(values[j]) != given_values[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

    list_values = r1_change_distribution.get_change_values_with_type(change_types[1], features_values)
    equal = 1
    for i in range(len(list_values)):
        given_values = features_values['NewAdditions'][i]
        values = list_values[i]
        for j in range(len(given_values)):
            if int(values[j]) != given_values[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

    list_values = r1_change_distribution.get_change_values_with_type(change_types[3], features_values)
    equal = 1
    for i in range(len(list_values)):
        given_values = features_values['EditDistances'][i]
        values = list_values[i]
        for j in range(len(given_values)):
            if int(values[j]) != given_values[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

if __name__ == '__main__':
    test_get_change_values_with_type()