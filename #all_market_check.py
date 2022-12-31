import stock_framework as sf
import pandas as pd
import re
import time
import random
from bs4 import BeautifulSoup
import requests

"""Buy point quick check whole market(random 10)"""


def check_once(_code):
    t = time.localtime()
    # get latest 10 days data
    if t.tm_mday > 16 and t.tm_mon > 1:
        sf.stock_get_code(stock_code=_code, start_date=(
            str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday - 15)))
    elif t.tm_mday < 16 and t.tm_mon > 1:
        sf.stock_get_code(stock_code=_code, start_date=(
            str(t.tm_year) + str(t.tm_mon - 1) + str(1)))
    elif t.tm_mon == 1:
        sf.stock_get_code(stock_code=_code, start_date=(
            str(t.tm_year - 1) + str(12) + str(1)))
    # check if today has opportunity

    class stock_ohlc:
        """A class contains a stock's ohlc"""
        o = list()
        h = list()
        l = list()
        c = list()
        t = list()
        v = list()
        d = list()

        def __init__(self, o, h, l, c, t, v, d):
            # make ohlc in a list, including time series, vol and deal
            self.o.append(o)
            self.h.append(h)
            self.l.append(l)
            self.c.append(c)
            self.t.append(t)
            self.v.append(v)
            self.d.append(d)

    class factor:
        """A class contains a stock's factor"""
        # avrp stands for the deal avrage price
        avrp = list()
        # arip stands for arithmetic price by high and low
        arip = list()
        # mav stands for moving average price by n days close price
        mav = list()
        # box stands for close price positon ratio in last 10 days
        box = list()

        def __init__(self, avrp, arip, mav, box):
            self.avrp.append(avrp)
            self.arip.append(arip)
            self.mav.append(mav)
            self.box.append(box)

    # read dayline
    dayline = pd.read_csv('csv/' + _code + '.csv')
    # sort by time series
    dayline.sort_values(by='日期', inplace=True)
    # dayline lenth
    lenth = len(dayline)
    # make ohlc a list, using iloc for time-sorted values
    for i in range(lenth):
        _ohlc = stock_ohlc(o=dayline.iloc[i, 6],
                           h=dayline.iloc[i, 4],
                           l=dayline.iloc[i, 5],
                           c=dayline.iloc[i, 3],
                           t=dayline.iloc[i, 0],
                           v=dayline.iloc[i, 11],
                           d=dayline.iloc[i, 12])
    # make factor a list
    for i in range(lenth):
        if i < 10:
            _factor = factor(avrp=_ohlc.d[i]/_ohlc.v[i],
                             arip=(_ohlc.h[i]+_ohlc.l[i])/2,
                             mav=dayline.iloc[i, 3],
                             box=(dayline.iloc[i, 3] - dayline.iloc[0: i + 1, 5].min()) /
                             (dayline.iloc[0: i + 1, 4].max() - dayline.iloc[0: i + 1, 5].min()))
        else:
            _factor = factor(avrp=_ohlc.d[i]/_ohlc.v[i],
                             arip=(_ohlc.h[i]+_ohlc.l[i])/2,
                             mav=dayline.iloc[i, 3],
                             box=(dayline.iloc[i, 3] - dayline.iloc[i - 9: i + 1, 5].min()) /
                             (dayline.iloc[i - 9: i + 1, 4].max() - dayline.iloc[i - 9: i + 1, 5].min()))
    stock_name = dayline.iloc[0, 2]

    # get latest data from xueqiu during trade time
    if t.tm_hour < 15 and t.tm_wday != (6 or 5):
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
            _volume = float(_volume)*10e3

        _ohlc.o.append(_o)
        _ohlc.h.append(_h)
        _ohlc.l.append(_l)
        _ohlc.c.append(_c)
        _ohlc.v.append(float(_volume))
        _ohlc.d.append(float(_amo))

        _factor.avrp.append(_ohlc.d[lenth]/_ohlc.v[lenth]/100)
        _factor.arip.append((_ohlc.h[lenth]+_ohlc.l[lenth])/2)
        if _c > dayline.iloc[lenth - 10: lenth, 4].max():
            _factor.box.append(1.)
        elif _c < dayline.iloc[lenth - 10: lenth, 5].min():
            _factor.box.append(0.)
        else:
            _factor.box.append((_c - dayline.iloc[lenth - 10: lenth, 5].min()) /
                               (dayline.iloc[lenth - 10: lenth, 4].max() - dayline.iloc[lenth - 10: lenth, 5].min()))

        lenth = lenth + 1

    del dayline
    # inverse stragety enhanced with k speed up
    k = list()
    k.append(0)
    for i in range(1, lenth):
        k.append(_factor.avrp[i] - _factor.avrp[i - 1])
    # n day inverse
    n = 2
    e_rpt_s = list()
    for i in range(0, 2):
        if k[lenth - 1 - i] * k[lenth - 2 - i] > 0:
            # speed up if abs(k) is greater
            if abs(k[lenth - 1 - i]) > abs(k[lenth - 2 - i]):
                e_rpt_s.append('加速')
            else:
                e_rpt_s.append('减速')
        else:
            # inverse signal
            for j in range(1, n):
                if k[lenth - 1 - i] * k[lenth - 2 - i - j] <= 0:
                    e_rpt_s.append(str(n) + '日反转')
                else:
                    e_rpt_s.append('無')
    # inverse
    # to make sure the real inverse happens
    # 1. red candle
    # 2. avrp-arip cross
    # 3. avrp-arip diff limit
    # 4. box limit by Fibonacci
    if k[lenth - 1] > 0 and e_rpt_s[0] == str(n) + '日反转'\
        and _ohlc.c[lenth - 1] > _ohlc.o[lenth - 1]\
        and ((_factor.avrp[lenth - 1] > _factor.arip[lenth - 1] - 0.01
              and _factor.avrp[lenth - 2] - 0.01 < _factor.arip[lenth - 2])
             or (_factor.avrp[lenth - 2] > _factor.arip[lenth - 2] - 0.01
                 and _factor.avrp[lenth - 3] - 0.01 < _factor.arip[lenth - 3]))\
            and _factor.box[lenth - 1] < 0.618:
        print(
            'B1买点' +
            '(' + str(round(_factor.box[lenth - 1], 2)
                      ) + ')' + ' ' + str(e_rpt_s[0]) + ' '
            + stock_name + str(_code) + '现价: ' + str(_ohlc.c[lenth - 1]))
        return
    # inverse enhance
    # 1. inverse happened before the day
    # 2. red candle
    # 3. speed up happened today
    # 4. avrp-arip diff limit by Fibonacci
    # 5. box limit by Fibonacci
    elif k[lenth - 2] > 0 and e_rpt_s[1] == str(n) + '日反转' \
            and _ohlc.c[lenth - 2] > _ohlc.o[lenth - 2] \
            and ((_factor.avrp[lenth - 2] > _factor.arip[lenth - 2] - 0.01
                  and _factor.avrp[lenth - 3] - 0.01 < _factor.arip[lenth - 3])
                 or (_factor.avrp[lenth - 3] > _factor.arip[lenth - 3] - 0.01
                     and _factor.avrp[lenth - 4] - 0.01 < _factor.arip[lenth - 4]))\
            and e_rpt_s[0] == '加速' \
            and (_factor.avrp[lenth - 2] - _factor.arip[lenth - 2]) / (_factor.avrp[lenth - 1] - _factor.arip[lenth - 1]) > 0.618\
            and _factor.box[lenth - 2] < 0.618\
            and _factor.box[lenth - 1] < 0.618:
        print(
            'B2买点' +
            '(' + str(round(_factor.box[lenth - 1], 2)
                      ) + ')' + ' ' + str(e_rpt_s[0]) + ' '
            + stock_name + str(_code) + '现价: ' + str(_ohlc.c[lenth - 1]))
        return
    # right trade trending follow
    # 1. at least 2 days k > 0
    # 2. red candle today
    # 3. avrp-arip diff limit by Fibonacci
    elif (k[lenth - 1] > 0 and _factor.avrp[lenth - 1] > _factor.arip[lenth - 1]
          and _ohlc.c[lenth - 1] > _ohlc.o[lenth - 1]) \
            and (k[lenth - 2] > 0 and _factor.avrp[lenth - 2] > _factor.arip[lenth - 2])\
            and (_factor.avrp[lenth - 2] - _factor.arip[lenth - 2]) / (_factor.avrp[lenth - 1] - _factor.arip[lenth - 1]) > 0.618:
        print(
            'B3买点' +
            '(' + str(round(_factor.box[lenth - 1], 2)
                      ) + ')' + ' ' + str(e_rpt_s[0]) + ' '
            + stock_name + str(_code) + '现价: ' + str(_ohlc.c[lenth - 1]))
        return
    # high risk right trade by down strike and avr line
    elif e_rpt_s[0] == str(n) + '日反转'\
            and k[lenth - 1] < 0\
            and _ohlc.c[lenth - 1] < _ohlc.o[lenth - 1]\
            and (_ohlc.c[lenth - 1] - _ohlc.l[lenth - 1]) / (_ohlc.o[lenth - 1] - _ohlc.c[lenth - 1]) > 1\
            and _factor.box[lenth - 1] < 0.618:
        print(
            'B4买点' +
            '(' + str(round(_factor.box[lenth - 1], 2)
                      ) + ')' + ' ' + str(e_rpt_s[0]) + ' '
            + stock_name + str(_code) + '现价: ' + str(_ohlc.c[lenth - 1]))
        return
    else:
        if k[lenth - 1] < 0:
            print(
                '無买点' + '(' + str(round(_factor.box[lenth - 1], 2)) + ')' + ' ' + str(e_rpt_s[0]) +
                '下跌' + ' ' + stock_name + str(_code) + '现价: ' + str(_ohlc.c[lenth - 1]))
        else:
            print(
                '無买点' + '(' + str(round(_factor.box[lenth - 1], 2)) + ')' + ' ' + str(e_rpt_s[0]) +
                '上涨' + ' ' + stock_name + str(_code) + '现价: ' + str(_ohlc.c[lenth - 1]))
        return


df_sh = pd.read_excel('GPLIST.xls', dtype={'A股代码': str})
df_sz = pd.read_excel('gplist_shenzhen.xlsx', dtype={'A股代码': str})
shanghai_list = list()
shenzhen_list = list()
for i in range(len(df_sh)):
    shanghai_list.append(df_sh.iloc[i, 0])
for i in range(len(df_sz)):
    shenzhen_list.append(df_sz.iloc[i, 4])
del df_sz
del df_sh
code_list = shenzhen_list + shanghai_list
random.shuffle(code_list)
for _code in code_list[0: 10]:
    delta_t = random.random()*20 + 10 + random.random()*3
    check_once(_code)
    time.sleep(delta_t)
