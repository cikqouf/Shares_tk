import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator


def technic_chart_matplotlib(dayline):

    def csv_wash(csvpath):
        """Return dayline dataframe, dealing with the .csv fetched
        from NetEase source."""
        # fix path isuue
        csvpath = re.sub(r'["& \']', "", csvpath)
        dayline = pd.read_csv(csvpath)
        # sort by time series
        dayline.sort_values(by='date', inplace=True)
        return dayline

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
                self.open.append(dayline.iloc[i, 2])
                self.high.append(dayline.iloc[i, 3])
                self.low.append(dayline.iloc[i, 4])
                self.close.append(dayline.iloc[i, 5])
                self.time.append(dayline.iloc[i, 0])
                self.vol.append(dayline.iloc[i, 7])
                self.amo.append(dayline.iloc[i, 8])
            # ------------------------------

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
    """initial stock factor and strategy"""
    import matplotlib.style as mplstyle
    mplstyle.use('fast')
    if dayline == '':
        show_switch = 1
        print('Input csv path: ', end='')
        dayline = csv_wash(input())
    else:
        show_switch = 0
        dayline = csv_wash(csvpath=dayline)
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
    """BEGIN"""
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
    """vol plot"""
    # grid
    plt.grid(True, which='both', ls='dashed')
    plt.bar(x, stock.vol)
    # tick labels date by month
    plt.xticks(ticks=np.arange(0, len(dayline), step=20),
               labels=stock.time[::20], rotation=30, size=7)
    """mav_diff bar plot"""
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
    plt.title(dayline.iloc[1, 1])
    plt.tight_layout()
    print('done')
    plt.savefig(dayline.iloc[1, 1] + '.png')
    if show_switch == 1:
        plt.show()
