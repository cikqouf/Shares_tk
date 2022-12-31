import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import time
import random
from stock_framework import stock_get_code


def cate_quick_check():
    category = ['*',
                'A 农林牧渔',
                'B 采矿业',
                'C 制造业',
                'D 水电煤气',
                'E 建筑业',
                'F 批发零售',
                'G 运输仓储',
                'H 住宿餐饮',
                'I 信息技术',
                'J 金融业',
                'K 房地产',
                'L 商务服务',
                'M 科研服务',
                'N 公共环保',
                'O 居民服务',
                'P 教育',
                'Q 卫生',
                'R 文化传播',
                'S 综合']
    data = pd.read_csv('stock_csv/all_sz_list.csv',
                       dtype={'all_sz_list': str, '自选': str}
                       )
    data_1 = [data.iloc[i, 0] for i in range(len(data))]
    data_2 = [data.iloc[i, 1] for i in range(len(data))]
    data_3 = [str(data.iloc[i, 2]) for i in range(len(data))]
    ind_1 = []
    print('输入行业代码: ', end='')
    k = int(input())
    for i in range(len(data)):
        if data_3[i] == category[k] and k == 0:
            ind_1.append(data_1[i])
        elif data_2[i] == category[k] and k!= 0:
            ind_1.append(data_1[i])
    print(category[k], '共有', len(ind_1), '个')
    print('connecting to server...')
    random.shuffle(ind_1)
    for _code in ind_1:
        # get data from xueqiu
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Referer': "https://baidu.com/",
            'Cookie': "device_id=a76bc3fe8cbf861c3af7c49761fd16b4; s=d1120q2qgx; bid=1cd25fd82dec71ebdfa72e1bf28b28f7_l6396ajf; acw_tc=2760779d16670473167334413ef7d5c3c09abdcbeac5dd795f4740c8750087; xq_a_token=ae5fc472c3ac4a0910f1d64f4c84e313e3c62d82; xqat=ae5fc472c3ac4a0910f1d64f4c84e313e3c62d82; xq_r_token=126b64f24abcc1b2d0b168de6cfeecdd2220d891; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTY2OTU5NDUxMywiY3RtIjoxNjY3MDQ3MjcxNjkwLCJjaWQiOiJkOWQwbjRBWnVwIn0.f1kWsFHP-Xum9huUESSGXH9IQKVFIznuxQ0KWOCIvhXLxu1ht76iRcALbAp52gpoZ1BE4dOOhk9KPD4DT9NY_O9rF7wYRxsax9CAhap30iEmxTbN9_pw0Fhvs6Gq1iE_YVfsVKJFefD2CDnR2QSBCyUUyqb2FbdgAZnbr7fr4b8zA8PYdwb705gTVdWXcZnKXj6k5n_og_rwaKUxS3BVFx3rVjGuXlGjKmajCzlCF5yy_XOr5CQActZKRvlsN2af6J0BR_tj3TLrFZz39habkIApU6zRjO322NZSxBJ4qvO41_RZwT5ivNu0JC_TfcF22fP5vSSBPFU-3xu4dCsSNQ; u=481667047316740; Hm_lvt_1db88642e346389874251b5a1eded6e3=1666964002,1666968695,1667043992,1667047320; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1667047783"
        }
        if int(_code) < 100000:
            website = 'https://xueqiu.com/S/' + 'SZ' + str(_code)
        else:
            website = 'https://xueqiu.com/S/' + 'SH' + str(_code)
        with open('tmp/xueqiu.html', 'w', encoding='utf-8') as f_1:
            print(requests.get(website, headers=headers).text, file=f_1)
        f_2 = open('tmp/xueqiu.html', 'rb')
        soup = BeautifulSoup(f_2, 'html.parser')
        info = list()
        for item in soup.find_all('td'):
            info.append(item.get_text())
        for item in soup.find_all('strong'):
            info.append(item.get_text())
        _o = float(re.sub(r'[：\u4e00-\u9fa5]', "", info[1]))
        _h = float(re.sub(r'[：\u4e00-\u9fa5]', "", info[0]))
        _l = float(re.sub(r'[：\u4e00-\u9fa5]', "", info[4]))
        _c = float(re.sub(r'[¥]', "", info[35]))
        _volume = re.sub(r'[：\u4e00-\u9fa5]', "", info[3])
        _amo = re.sub(r'[：\u4e00-\u9fa5]', "", info[7])
        if info[7] == '成交额：' + _amo + '亿':
            _amo = float(_amo)*10e7
        elif info[7] == '成交额：' + _amo + '万':
            _amo = float(_amo)*10e3
        if info[3] == '成交量：' + _volume + '万手':
            _volume = float(_volume)*10e5
        else:
            _volume = float(_volume)*10e1
        _amo = float(_amo)
        # get stock name and history data
        stock_get_code(_code, str(20220101))
        tmppd = pd.read_csv('csv/' + _code + '.csv')
        short_name = tmppd.iloc[1, 2]
        # print info
        delta_t = random.random()*5 + random.random()*3
        print(_code, short_name, '\t', '开:', _o, '高:', _h, '低:', _l,
              '收:', _c, '溢价率:', round(_amo/_volume/(_l+_h)*2 - 1, 3), end=' ')
        if _c < _o:
            print('green')
        elif _c > _o:
            print('red')
        else:
            print('-')
        print('请等待', round(delta_t, 2), '秒')
        time.sleep(delta_t)
