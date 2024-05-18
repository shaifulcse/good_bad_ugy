import r1_change_distribution
from util import utility

apply_age_restriction = True
age_restriction = 2 * 365

def test_get_change_values_with_type():
    change_types = ['revision', 'adds', 'diffs', 'edits', 'bugs']
    method = {'age': 5193, 'ChangeAtMethodAge': ['0', '99', '777'], 'DiffSizes': ['0', '14', '0'],
     'NewAdditions': ['0', '9', '0'], 'EditDistances': ['0', '143', '0'], 'RiskyCommit': ['0', '1', '1'],
     'file': ['1333.json']}

    values = r1_change_distribution.get_change_values_with_type(change_types[4], method)
    equal = 1
    for i in range(len(values)):
        if int(values[i]) != int(method['RiskyCommit'][i]):
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

    values = r1_change_distribution.get_change_values_with_type(change_types[0], method)

    equal = 1
    for i in range(len(values)):
        if int(values[i]) != int(method['DiffSizes'][i]):
            equal = 0
            break
        if equal == 0:
            break
    assert equal == 1

def test_calculate_value():
    change_type = 'revision'
    values = [0, 20, 0, 2, 10]
    diff_values = [0, 20, 0, 2, 10]
    change_ages = [0, 700, 720, 730, 900]
    value = r1_change_distribution.calculate_value(change_type, values, diff_values, change_ages)
    assert value == 2

    change_type = 'diffs'
    values = [0, 20, 0, 2, 10]
    diff_values = [0, 20, 0, 2, 10]
    change_ages = [0, 700, 720, 730, 900]
    value = r1_change_distribution.calculate_value(change_type, values, diff_values, change_ages)
    assert value == 22

    change_type = 'adds'
    values = [0, 20, 0, 2, 10]
    diff_values = [0, 20, 0, 2, 10]
    change_ages = [0, 700, 720, 730, 900]
    value = r1_change_distribution.calculate_value(change_type, values, diff_values, change_ages)
    assert value == 22

    change_type = 'edits'
    values = [0, 20, 0, 2, 10]
    diff_values = [0, 20, 0, 2, 10]
    change_ages = [0, 700, 720, 730, 730]
    value = r1_change_distribution.calculate_value(change_type, values, diff_values, change_ages)
    assert value == 32

    change_type = 'bugs'
    values = [0, 1, 0, 1, 1]
    diff_values = [0, 20, 0, 0, 10]
    change_ages = [0, 700, 720, 730, 900]
    value = r1_change_distribution.calculate_value(change_type, values, diff_values, change_ages)
    assert value == 1

def  test_process_method():
    change_type = 'revision'
    method = {'age': 5193, 'ChangeAtMethodAge': ['0', '99', '777'], 'DiffSizes': ['0', '14', '0'],
              'NewAdditions': ['0', '9', '0'], 'EditDistances': ['0', '143', '0'], 'RiskyCommit': ['0', '1', '1'],
              'file': ['1333.json']}
    value = r1_change_distribution.process_method(change_type, method)
    assert value ==  1

    change_type = 'revision'
    method =     {'age': 1043, 'ChangeAtMethodAge': ['0', '301', '305', '392', '544', '881', '969'],
     'DiffSizes': ['0', '18', '0', '0', '3', '9', '1'], 'NewAdditions': ['0', '9', '0', '0', '3', '3', '1'],
     'EditDistances': ['0', '36', '0', '0', '90', '116', '56'], 'RiskyCommit': ['0', '0', '1', '0', '0', '0', '1'],
     'file': ['21928.json']}
    value = r1_change_distribution.process_method(change_type, method)
    assert value == 2

    change_type = 'diffs'
    method = {'age': 1043, 'ChangeAtMethodAge': ['0', '301', '305', '392', '544', '881', '969'],
              'DiffSizes': ['0', '18', '0', '0', '3', '9', '1'], 'NewAdditions': ['0', '9', '0', '0', '3', '3', '1'],
              'EditDistances': ['0', '36', '0', '0', '90', '116', '56'],
              'RiskyCommit': ['0', '0', '1', '0', '0', '0', '1'],
              'file': ['21928.json']}
    value = r1_change_distribution.process_method(change_type, method)
    assert value == 21

    change_type = 'edits'
    method = {'age': 1043, 'ChangeAtMethodAge': ['0', '301', '305', '392', '544', '881', '969'],
              'DiffSizes': ['0', '18', '0', '0', '3', '9', '1'], 'NewAdditions': ['0', '9', '0', '0', '3', '3', '1'],
              'EditDistances': ['0', '36', '0', '0', '90', '116', '56'],
              'RiskyCommit': ['0', '0', '1', '0', '0', '0', '1'],
              'file': ['21928.json']}
    value = r1_change_distribution.process_method(change_type, method)
    assert value == 126

    change_type = 'bugs'
    method = {'age': 1043, 'ChangeAtMethodAge': ['0', '301', '305', '392', '544', '881', '969'],
              'DiffSizes': ['0', '18', '0', '0', '3', '9', '1'], 'NewAdditions': ['0', '9', '0', '0', '3', '3', '1'],
              'EditDistances': ['0', '36', '0', '0', '90', '116', '56'],
              'RiskyCommit': ['0', '0', '1', '0', '0', '0', '1'],
              'file': ['21928.json']}
    value = r1_change_distribution.process_method(change_type, method)
    assert value == 0

    change_type = 'bugs'
    method = {'age': 1043, 'ChangeAtMethodAge': ['0', '301', '305', '392', '544', '881', '969'],
              'DiffSizes': ['0', '18', '0', '0', '3', '9', '1'], 'NewAdditions': ['0', '9', '0', '0', '3', '3', '1'],
              'EditDistances': ['0', '36', '0', '0', '90', '116', '56'],
              'RiskyCommit': ['0', '1', '1', '0', '0', '0', '1'],
              'file': ['21928.json']}
    value = r1_change_distribution.process_method(change_type, method)
    assert value == 1

def test_analyze():
  methods =  {'1421.json': 0, '3874.json': 10, '2413.json': 5, '1589.json': 6, '4217.json': 8,
              '213.json': 200, '1000.json': 100, '10000.json': 30, '1500.json': 20,
              '2500': 40, '2600': 60}
  utility.total_change = 479
  stats = r1_change_distribution.analyse(methods)

  assert stats[5] == 0.4175365344467641
  assert stats[10] == 0.6263048016701461
  assert stats[15] == 0.6263048016701461
  assert stats[20] == 0.7515657620041754



if __name__ == '__main__':
    utility.age_restriction = 2 * 365 ## because this is what we test with
    test_get_change_values_with_type()
    test_calculate_value()
    test_process_method()
    test_analyze()
