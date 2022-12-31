# get stock info from NetEase
import os
import requests
import re
import linecache
import platform


def stock_get():
    print("输入股票代码: ", end='')
    stock_code = input()
    print("查询年份: ", end='')
    year = input()
    print("季度数: ", end='')
    season = int(input())
    # Linux's request.text is different from Windows
    # row_num points to the stat row
    if platform.system() == 'Windows':
        row_num = 530
    elif platform.system() == 'Linux':
        row_num = 265
    else:
        print('system is wrong, may occur issue')
        row_num = 265
    for i in range(1, season + 1):
        stock_get_code(stock_code, year, i, row_num)


def stock_get_code(stock_code, year, season, row_num):
    # get stat from NetEase
    # headreferer = {'Referer': 'https://quotes.money.163.com/trade'}
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Cookie': "ariaoldFixedStatus=false; pver_n_f_l_n3=a; UserAdLocation=%u5317%u4EAC; vinfo_n_f_l_n3=2f346f95471c49b9.1.2.1661151095823.1665322806343.1667044342632; _antanalysis_s_id=1667044594990",
    'Referer': "https://baidu.com/"
    }
    website = "https://quotes.money.163.com/trade/lsjysj_" + \
        str(stock_code) + ".html?year=" + str(year) + "&season=" + str(season)
    statastic_raw = requests.get(website, headers=headers)
    with open("tmp/statastic_raw.txt", "w", encoding='utf-8') as f_1:
        print(statastic_raw.text, file=f_1)
    # clear llinecache
    linecache.clearcache()
    # get raw stat
    stata_row = linecache.getline(
        "tmp/statastic_raw.txt", row_num)
    # read the specific row of statastic
    clean_statastic = re.sub(r'[,<a-zA-Z=/\' ]', "", stata_row)
    with open("tmp/statastic_clean.txt", "w", encoding='utf-8') as f_2:
        print(clean_statastic, file=f_2)
    # make the data a list
    with open("tmp/statastic_clean.txt", "r", encoding='utf-8') as f_3:
        list_of_stata = f_3.read().split(">>")
        # save the stat as csv
        # first get stock name in Chinese
        # Linux's request.text is different from Windows
        # here stock_name's position is in ln 7 on Windows while ln 4 on Linux
        if platform.system() == 'Linux':
            linerow = 4
        elif platform.system() == 'Windows':
            linerow = 7
        else:
            linerow = 4
            print('system is wrong, may occur issue')
        stock_name = linecache.getline(
            "tmp/statastic_raw.txt", linerow)
        # using regex to remove html element and leave name and code
        stock_name = re.sub(r'[^（）0-9\u4e00-\u9fa5]', "", stock_name)
        lenth = str(len(stock_name) - 14)
        stock_name = re.sub('(?<=.{' + lenth + '}).{0,7}', "", stock_name)
        stock_name = re.sub(r'（', "(", stock_name)
        stock_name = re.sub(r'）', ')', stock_name)
        with open("csv/" + stock_name + str(year) + str(season) + ".csv", "w", encoding='utf-8') as f_4:
            print("date,open,high,low,close,涨跌额,涨跌幅,volume,amo,振幅百分比,换手率百分比", file=f_4)
            for i in range(len(list_of_stata)):
                if i % 12 == 0:
                    print(list_of_stata[i], end="", file=f_4)
                elif (i+1) % 12 == 0:
                    print(list_of_stata[i], end="", file=f_4)
                    print("\t", file=f_4)
                else:
                    print(list_of_stata[i], end=",", file=f_4)
        # check if file has no stat
        check = linecache.getline(
            "csv/" + stock_name + str(year) + str(season) + ".csv", 2)
        if check == '>\n':
            # 清除缓存
            linecache.clearcache()
            if platform.system() == 'Linux':
                row_num_new = 266
            elif platform.system() == 'Windows':
                row_num_new = 528
            else:
                print('system wrong, may occur issue')
                row_num_new = 264
            stock_get_code(stock_code, year, season, row_num_new)
            # end function here
            return
        # here remove last comma
        file_old = open("csv/" +
                        stock_name + str(year) + str(season) + ".csv", 'rb+')
        file_old.seek(-1, os.SEEK_END)
        # 截断逗号
        file_old.truncate()
        file_old.close()
