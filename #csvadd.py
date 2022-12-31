import pandas as pd
import re
# 合并csv文件


def csvadd():
    print("csv合并个数: ", end='')
    count = int(input())
    # dataframe as list
    df = list()
    for i in range(0, count):
        print('csv_path[', i + 1, ']: ', end='')
        csv_path = input()
        # fix path issue
        csv_path = re.sub(r'[& \']', "", csv_path)
        df.append(pd.read_csv(csv_path, index_col=0))
    for k in range(0, count - 1):
        if k == 0:
            dfa = pd.concat([df[k + 1], df[k]])
            dfa.drop_duplicates()
            continue
        dfa = pd.concat([dfa, df[k + 1]])
        dfa.drop_duplicates()
    dfa.sort_values(by='date', inplace=True)
    fname = re.sub(r'[\\_a-z./:]', "", csv_path)
    lenth = str(len(fname) - 1)
    fname = re.sub('(?<=.{' + lenth + '}).{0,1}', "", fname) + '+' + str(count)
    dfa.to_csv(fname + '.csv', encoding='utf-8')
