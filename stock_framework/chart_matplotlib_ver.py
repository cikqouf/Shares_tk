import re

import requests
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator
from bs4 import BeautifulSoup


def technic_chart_matplotlib():

    def csv_wash(csvpath):
        """Return dayline dataframe, dealing with the .csv fetched
        from NetEase source."""
        # fix path isuue
        csvpath = re.sub(r'["& \']', "", csvpath)
        dayline = pd.read_csv(csvpath)
        # sort by time series
        dayline.sort_values(by='日期', inplace=True)
        return dayline

    def latest_data(t, _code, stock):
        if t.tm_hour > 9 and t.tm_hour < 15 and t.tm_wday != 5 and t.tm_wday != 6:
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
            stock.open.append(_o)
            stock.high.append(_h)
            stock.low.append(_l)
            stock.close.append(_c)
            stock.vol.append(_volume)
            stock.amo.append(_amo)

    class stock_ohlcva:
        """A class contains a stock's ohlcva"""
        open = []
        high = []
        low = []
        close = []
        time = []
        vol = []
        amo = []

        def __init__(self, dayline):
            # make ohlc in a list, including time series, vol and amo
            """
            attention, pandas' dataframe cannot sort values by property
            'loc', must using 'iloc' for sorted value.
            """
            for i in range(len(dayline)):
                self.open.append(dayline.iloc[i, 6])
                self.high.append(dayline.iloc[i, 4])
                self.low.append(dayline.iloc[i, 5])
                self.close.append(dayline.iloc[i, 3])
                self.time.append(dayline.iloc[i, 0])
                self.vol.append(dayline.iloc[i, 11])
                self.amo.append(dayline.iloc[i, 12])
            # ------------------------------
            # latest data from xueqiu
            t = time.localtime()
            _code = re.sub(r'["& \']', "", dayline.iloc[1, 1])
            latest_data(t=t, _code=_code, stock=self)

    class stock_factor(stock_ohlcva):
        """A class contains factors"""

        def __init__(self, **kwargs):
            """
            factor:
            cycle factor, recommanding using condition expression list.
            """
            stock_factor.avrp = [
                stock_ohlcva.amo[i]/stock_ohlcva.vol[i] for i in range(len(stock_ohlcva.close))]
            stock_factor.arip = [
                (stock_ohlcva.high[i] + stock_ohlcva.low[i])/2 for i in range(len(stock_ohlcva.close))]
            stock_factor.avrp_arip_minus = [
                abs(stock_factor.avrp[i] - stock_factor.arip[i]) for i in range(len(stock_ohlcva.close))]

            mavn = list(kwargs['mavn'])
            stock_factor.mav = [[stock_ohlcva.close[i]
                                if i < (mavn[k] - 1)
                                else
                                sum(stock_ohlcva.close[(
                                    i - mavn[k] + 1): i + 1]) / mavn[k]
                                for i in range(len(stock_ohlcva.close))]
                                for k in range(len(mavn))]
            stock_factor.mav_diff = [stock_factor.mav[0][i] - stock_factor.mav[2][i]
                                     for i in range(len(stock_ohlcva.close))]
            mavdif_boxn = list(kwargs['mavdif_boxn'])
            stock_factor.mav_diff_box = [[0
                                          if i < (mavdif_boxn[k] - 1)
                                          else
                                          (stock_factor.mav_diff[i] -
                                              min(stock_factor.mav_diff[(
                                                  i - mavdif_boxn[k] + 1): i + 1])) /
                                          (max(stock_factor.mav_diff[(
                                              i - mavdif_boxn[k] + 1): i + 1]) -
                                              min(stock_factor.mav_diff[(
                                                  i - mavdif_boxn[k] + 1): i + 1]))
                                          for i in range(len(stock_factor.close))]
                                         for k in range(len(mavdif_boxn))]
            boxn = list(kwargs['boxn'])
            stock_factor.box = [[0
                                if i < (boxn[k] - 1)
                                else
                                (stock_ohlcva.close[i] -
                                 min(stock_ohlcva.low[(
                                     i - boxn[k] + 1): i + 1])) /
                                (max(stock_ohlcva.high[(
                                    i - boxn[k] + 1): i + 1]) -
                                    min(stock_ohlcva.low[(
                                        i - boxn[k] + 1): i + 1]))
                                for i in range(len(stock_ohlcva.close))]
                                for k in range(len(boxn))]
            boxdn = list(kwargs['boxdn'])
            stock_factor.boxd = [[.11
                                  if i < (boxdn[k] - 1)
                                  else
                                  (stock_ohlcva.low[i] -
                                   min(stock_ohlcva.low[(
                                       i - boxdn[k] + 1): i + 1])) /
                                  (max(stock_ohlcva.high[(
                                      i - boxdn[k] + 1): i + 1]) -
                                      min(stock_ohlcva.low[(
                                          i - boxdn[k] + 1): i + 1]))
                                  for i in range(len(stock_ohlcva.close))]
                                 for k in range(len(boxdn))]
            volboxn = list(kwargs['volboxn'])
            stock_factor.vol_box = [[0
                                    if i < (volboxn[k] - 1)
                                    else
                                    (stock_ohlcva.vol[i] -
                                     min(stock_ohlcva.vol[(
                                         i - volboxn[k] + 1): i + 1])) /
                                    (max(stock_ohlcva.vol[(
                                        i - volboxn[k] + 1): i + 1]) -
                                        min(stock_ohlcva.vol[(
                                            i - volboxn[k] + 1): i + 1]))
                                    for i in range(len(stock_ohlcva.close))]
                                    for k in range(len(volboxn))]
            avrp_arip_boxn = list(kwargs['avrp_arip_boxn'])
            stock_factor.avrp_arip_box = [[0
                                           if i < (avrp_arip_boxn[k] - 1)
                                           else
                                           (stock_factor.avrp_arip_minus[i] -
                                            min(stock_factor.avrp_arip_minus[(
                                                i - avrp_arip_boxn[k] + 1): i + 1])) /
                                           (max(stock_factor.avrp_arip_minus[(
                                               i - avrp_arip_boxn[k] + 1): i + 1]) -
                                               min(stock_factor.avrp_arip_minus[(
                                                   i - avrp_arip_boxn[k] + 1): i + 1]))
                                           for i in range(len(stock_ohlcva.close))]
                                          for k in range(len(avrp_arip_boxn))]

    class stock_strategy(stock_factor):
        """A class contains trading strategies"""

        def __init__(self):
            # meta strategy
            self.avrp_ge_arip_strategy = [
                stock_factor.avrp[i] > stock_factor.arip[i] for i in range(len(stock_factor.close))]
            self.avrp_arip_box_strategy = [[stock_factor.avrp_arip_box[j][i] > 0.618
                                            for i in range(len(stock_factor.close))]
                                           for j in range(len(stock_factor.avrp_arip_box))]
            self.box_strategy = [[stock_factor.box[j][i] < 0.618
                                  for i in range(len(stock_factor.close))]
                                 for j in range(len(stock_factor.box))]
            self.box_dstrike_strategy = [[stock_factor.boxd[j][i] == 0
                                         for i in range(len(stock_factor.close))]
                                         for j in range(len(stock_factor.boxd))]
            self.price_rise_strategy = [stock_factor.close[i] >= stock_factor.open[i]
                                        for i in range(len(stock_factor.close))]
            self.vol_box_strategy = [[stock_factor.vol_box[j][i] > 0.618
                                      for i in range(len(stock_factor.close))]
                                     for j in range(len(stock_factor.vol_box))]
            self.mav_diff_strategy = [(stock_factor.mav_diff[i] - stock_factor.mav_diff[i - 1]) *
                                      (stock_factor.mav_diff[i - 1] -
                                       stock_factor.mav_diff[i - 2]) <= 0
                                      and
                                      (stock_factor.mav_diff[i] -
                                       stock_factor.mav_diff[i - 1]) >= 0
                                      if i > 1
                                      else 0
                                      for i in range(len(stock_factor.close))]
            self.mav_diff_box_strategy = [[stock_factor.mav_diff_box[j][i] < 0.236
                                           for i in range(len(stock_factor.close))]
                                          for j in range(len(stock_factor.mav_diff_box))]
            self.long_strategy = [(stock_factor.close[i] - stock_factor.avrp[i]) /
                                  (stock_factor.high[i] -
                                   stock_factor.avrp[i]) > 0
                                  for i in range(len(stock_factor.close))]
            self.tencm_block = [stock_factor.close[i]/stock_factor.close[i - 1] < 1.09
                                if i > 0
                                else
                                False
                                for i in range(len(stock_factor.close))]

    # ---------------------------------------
    """begin"""
    print('Input csv path: ', end='')
    dayline = csv_wash(input())
    stock = stock_ohlcva(dayline)
    factor = stock_factor(mavn=(5, 10, 20, 60),
                          boxn=(9, 10),
                          volboxn=(9, 10),
                          avrp_arip_boxn=(9, 10),
                          boxdn=(9, 6),
                          mavdif_boxn=(40, 6))
    strategy = stock_strategy()
    # ----------------------------------
    # put strategy here by the combination of meta strategy
    """STRATEGY"""
    b1 = ['B1'  # 放量负溢价放大B
          if
          strategy.avrp_arip_box_strategy[0][i]  # 溢价放大
          and
          not (strategy.avrp_ge_arip_strategy[i])  # 负溢价
          and
          strategy.vol_box_strategy[0][i]  # 成交量放大
          and
          strategy.box_strategy[0][i]  # 9日箱体
          and
          strategy.tencm_block[i]  # 涨停限制
          else ''
          for i in range(len(stock.close))
          ]
    b2 = ['B2'  # 9日新低突破排除涨停板多头进入缩量
          if
          strategy.box_dstrike_strategy[0][i]  # 9日低点突破
          and
          strategy.long_strategy[i]  # 多头进入
          and
          not (strategy.vol_box_strategy[0][i])  # 缩量
          and
          strategy.tencm_block[i]
          else ''
          for i in range(len(stock.close))]
    b3 = ['B3'  # 放量9日新低突破
          if
          strategy.box_dstrike_strategy[0][i]  # 9日低点突破
          and
          strategy.vol_box_strategy[0][i]  # 放量
          and
          strategy.tencm_block[i]
          else ''
          for i in range(len(stock.close))]
    s1 = ['S1'  # 放量正溢价放大S
          if
          strategy.avrp_arip_box_strategy[0][i]  # 溢价放大
          and
          strategy.avrp_ge_arip_strategy[i]  # 正溢价
          and
          strategy.vol_box_strategy[0][i]  # 成交放大
          and
          not (strategy.box_strategy[0][i])  # 突破箱体
          else ''
          for i in range(len(stock.close))
          ]
    s2 = ['S2'  # 缩量9日新高无溢价多头离去
          if
          not (strategy.avrp_arip_box_strategy[0][i])  # 无溢价
          and
          not (strategy.box_strategy[0][i])  # 突破箱体
          and
          not (strategy.vol_box_strategy[0][i])  # 缩量
          and
          not (strategy.long_strategy[i])  # 多头离开
          else ''
          for i in range(len(stock.close))
          ]
    # -----------------------------------

    print('technic 0.0.1beta')

    """technic chart"""
    # create fig
    fig = plt.figure(figsize=(16, 10))

    # ohlc_chart postion
    ax_1 = plt.subplot2grid((5, 4), (0, 0), rowspan=3, colspan=4)
    x = np.arange(0, len(stock.close))
    # grid
    plt.grid(True, which='both', ls='dashed')
    # basic_ohlc
    print('loading ohlc...')
    for i in range(len(stock.close)):
        if strategy.price_rise_strategy[i]:
            plt.vlines(i, stock.low[i], stock.high[i], color='red')
            plt.hlines(stock.open[i],
                       i - .3,
                       i,
                       color='red')
            plt.hlines(stock.close[i],
                       i,
                       i + .3,
                       color='red')
        else:
            plt.vlines(i, stock.low[i], stock.high[i], color='green')
            plt.hlines(stock.open[i],
                       i - .3,
                       i,
                       color='green')
            plt.hlines(stock.close[i],
                       i,
                       i + .3,
                       color='green')

    # ----------------------------------
    """let factors visible"""
    print('loading factor...')
    # factor plot
    plt.plot(x, factor.avrp, linewidth=1., color='orange', label='成交平均价')
    plt.plot(x, factor.arip, linewidth=1., color='purple', label='算数平均价')
    plt.plot(x, factor.mav[0], linewidth=1., label='5日均线')
    plt.plot(x, factor.mav[1], linewidth=1., label='10日均线')
    plt.plot(x, factor.mav[2], linewidth=1., label='20日均线')
    plt.plot(x, factor.mav[3], linewidth=1., label='60日均线')

    # -------------------------------------
    """strategy plot"""
    print('loading strategy...')
    for i in range(0, len(stock.close)):
        plt.text(x=x[i], y=stock.close[i], s=b1[i], color='red', rotation=20)
    for i in range(len(stock.close)):
        plt.text(x=x[i], y=stock.low[i], s=b2[i], color='red', rotation=20)
    for i in range(len(stock.close)):
        plt.text(x=x[i], y=stock.low[i], s=b3[i], color='red', rotation=20)
    for i in range(0, len(stock.close)):
        plt.text(x=x[i], y=stock.close[i], s=s1[i], color='blue', rotation=20)
    for i in range(0, len(stock.close)):
        plt.text(x=x[i], y=stock.close[i], s=s2[i], color='blue', rotation=20)
    # ------------------------------------

    # label location
    plt.legend(loc='best')

    # tick labels date by month
    plt.xticks(ticks=np.arange(0, len(dayline), step=20),
               labels=stock.time[::20], rotation=30, size=7)

    # ------------------------------------
    ax_2 = plt.subplot2grid((5, 4), (3, 0), rowspan=1, colspan=4)
    """净值曲线"""
    # grid
    plt.grid(True, which='both', ls='dashed')
    N = 0
    if N == 1:
        infooo = []
        asset = [1 for _ in range(len(stock.close))]
        cashfree = 1
        hold_count = 0
        for i in range(0, len(asset) - 1):
            if (b1[i] == 'B1' or b2[i] == 'B2') and cashfree == 1:
                asset[i + 1] = asset[i]*(stock.close[i + 1]/stock.close[i])
                cashfree = 0
                hold_count += 1
                infooo.append('买入')
            elif (s1[i] == 'S1' or s2[i] == 'S2') \
                    and\
                    cashfree == 0 \
                    and \
                    (factor.mav_diff[i] - factor.mav_diff[i - 1]) <= \
                    (factor.mav_diff[i - 1] - factor.mav_diff[i - 2]):  # 卖点保守化
                asset[i + 1] = asset[i]
                cashfree = 1
                hold_count = 0
                infooo.append('卖出')
            elif cashfree == 0:
                if asset[i] / asset[i - hold_count] < .62:  # 注: 可以加时间限制，如3天内亏损超过某一阈值
                    asset[i + 1] = asset[i]
                    cashfree = 1
                    hold_count = 0
                    infooo.append('止损')
                else:
                    asset[i + 1] = asset[i]*(stock.close[i + 1]/stock.close[i])
                    cashfree = 0
                    hold_count += 1
                    infooo.append('')
            elif cashfree == 1:
                asset[i + 1] = asset[i]
                cashfree = 1
                hold_count = 0
                infooo.append('')
        infooo.append('')
        plt.plot(x, asset)
        for i in range(len(stock.close)):
            plt.text(x=i, y=asset[i], s=infooo[i], color='red')
    plt.bar(x, stock.vol)
    # tick labels date by month
    plt.xticks(ticks=np.arange(0, len(dayline), step=20),
               labels=stock.time[::20], rotation=30, size=7)
    ax_3 = plt.subplot2grid((5, 4), (4, 0), rowspan=1, colspan=4)
    plt.bar(x, factor.mav_diff)

    # tick labels date by month
    plt.xticks(ticks=np.arange(0, len(dayline), step=20),
               labels=stock.time[::20], rotation=30, size=7)

    # tick setting
    # major tick is half a month
    majorLocator = MultipleLocator(10)
    # minor tick in 2 days
    minorLocator = MultipleLocator(2)
    # tick show setting
    ax_1.xaxis.set_major_locator(majorLocator)
    ax_1.xaxis.set_minor_locator(minorLocator)
    ax_2.xaxis.set_major_locator(majorLocator)
    ax_2.xaxis.set_minor_locator(minorLocator)
    ax_3.xaxis.set_major_locator(majorLocator)
    ax_3.xaxis.set_minor_locator(minorLocator)
    # tick labels date by month
    plt.xticks(ticks=np.arange(0, len(dayline), step=20),
               labels=stock.time[::20], rotation=30, size=7)
    # font setting
    plt.rcParams["font.sans-serif"] = ["HanaMinA"]
    # title
    plt.title(dayline.iloc[1, 2])
    plt.tight_layout()
    print('done')
    plt.show()
