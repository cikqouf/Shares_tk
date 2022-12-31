import os
from os import listdir
def clean_tmp_file():
    # get currunt workpace directory
    pwdd = os.getcwd()
    # del svg and csv
    for fname in listdir(pwdd):
        if fname.endswith('.svg'):
            os.remove(pwdd + '/' + fname)
        if fname.endswith('.csv'):
            os.remove(pwdd + '/' + fname)
        if fname.endswith('.html'):
            os.remove(pwdd + '/' + fname)
    # del tmp/.txt
    pwdd_tmp = pwdd + '/tmp'
    for fname in listdir(pwdd_tmp):
        if fname.endswith('.txt'):
            os.remove(pwdd_tmp + '/' + fname)
        if fname.endswith('.html'):
            os.remove(pwdd_tmp + '/' + fname)
    # del csv/.csv
    for i in range(1000):
        print('delete csv files? (y or n)')
        x = input()
        if x == 'y':
            pwdd_csv = pwdd + '/csv'
            for fname in listdir(pwdd_csv):
                if fname.endswith('.csv'):
                    os.remove(pwdd_csv + '/' + fname)
            return
        elif x == 'n':
            return
        else:
            i = 0
