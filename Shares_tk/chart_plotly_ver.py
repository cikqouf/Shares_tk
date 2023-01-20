import pandas as pd
import re
import plotly
import plotly.graph_objs as go
import numpy as np


def technic_chart_plotly():

    def csv_wash(csvpath):
        """Return dayline dataframe, dealing with the .csv fetched
        from NetEase source."""
        # fix path isuue
        csvpath = re.sub(r'["& \']', "", csvpath)
        dayline = pd.read_csv(csvpath)
        # sort by time series
        dayline.sort_values(by='日期', inplace=True)
        return dayline

    class stock_ohlcva:
        """A class contains a stock's ohlc"""
        open = []
        high = []
        low = []
        close = []
        time = []
        vol = []
        amo = []

        def __init__(self, dayline):
            # make ohlc in a list, including time series, vol and deal
            for i in range(len(dayline)):
                self.open.append(dayline.iloc[i, 6])
                self.high.append(dayline.iloc[i, 4])
                self.low.append(dayline.iloc[i, 5])
                self.close.append(dayline.iloc[i, 3])
                self.time.append(dayline.iloc[i, 0])
                self.vol.append(dayline.iloc[i, 11])
                self.amo.append(dayline.iloc[i, 12])

    class stock_factor(stock_ohlcva):
        """A class contains factors"""
        avrp = []
        arip = []
        mav = []
        box = []

        def __init__(self, **kwargs):

            stock_factor.avrp = [
                stock_ohlcva.amo[i]/stock_ohlcva.vol[i] for i in range(len(dayline))]
            stock_factor.arip = [
                (stock_ohlcva.high[i] + stock_ohlcva.low[i])/2 for i in range(len(dayline))]

            mavn = list(kwargs['mavn'])
            stock_factor.mav = [[stock_ohlcva.close[i]
                                if i < (mavn[k] - 1)
                                else
                                sum(stock_ohlcva.close[(
                                    i - mavn[k] + 1): i + 1]) / mavn[k]
                                for i in range(len(dayline))]
                                for k in range(len(mavn))]

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
                                for i in range(len(dayline))]
                                for k in range(len(boxn))]

    class stock_strategy(stock_factor):
        """A class contains trading strategies"""
        # meta strategy
        avrp_arip_strategy = []
        box_strategy = []
        rise_strategy = []
        speed_strategy = []  # based on avrp
        inverse_strategy = []  # in 2 days

        def __init__(self):
            # meta strategy
            self.avrp_arip_strategy = [stock_factor.avrp[i] > stock_factor.arip[i]
                                       for i in range(len(dayline))]
            self.box_strategy = [[stock_factor.box[j][i] < 0.618
                                  for i in range(len(dayline))]
                                 for j in range(len(stock_factor.box))]
            self.rise_strategy = [stock_factor.close[i] > stock_factor.open[i]
                                  for i in range(len(dayline))]
            self.speed_strategy = [abs(stock_factor.avrp[i] - stock_factor.avrp[i - 1]) >
                                   abs(stock_factor.avrp[i - 1] -
                                       stock_factor.avrp[i - 2])
                                   and
                                   (stock_factor.avrp[i] - stock_factor.avrp[i - 1]) *
                                   (stock_factor.avrp[i - 1] -
                                    stock_factor.avrp[i - 2]) > 0
                                   if i > 1
                                   else False
                                   for i in range(len(dayline))]
            self.inverse_strategy = [(stock_factor.avrp[i] - stock_factor.avrp[i - 1]) *
                                     (stock_factor.avrp[i - 1] -
                                     stock_factor.avrp[i - 2]) < 0
                                     and
                                     (stock_factor.avrp[i - 1] - stock_factor.avrp[i - 2]) *
                                     (stock_factor.avrp[i - 2] -
                                     stock_factor.avrp[i - 3]) > 0
                                     if i > 2
                                     else False
                                     for i in range(len(dayline))]

    print('Input csv path: ', end='')
    dayline = csv_wash(input())
    stock = stock_ohlcva(dayline)
    factor = stock_factor(mavn=(5, 10, 20), boxn=(9, 10))
    strategy = stock_strategy()
    b1 = ['B1'
          if strategy.avrp_arip_strategy[i]
          and
          strategy.box_strategy[0][i]
          and
          strategy.rise_strategy[i]
          and
          strategy.inverse_strategy[i]
          else ''
          for i in range(len(dayline))
          ]

    print('technic 0.0.1beta')

    """technic chart"""
    fig = go.Figure()
    x = np.arange(0, len(stock.close))
    trace1 = go.Scatter(
        x=x,
        y=factor.avrp,
        mode='lines',
        name='成交平均价',
        hovertext=stock.time,
        line={
            'color': 'orange',
            'width': .7
        }
    )
    trace2 = go.Scatter(
        x=x,
        y=factor.arip,
        mode='lines',
        name='算数平均价',
        hovertext=stock.time,
        line={
            'color': 'purple',
            'width': .7
        }
    )
    mav = go.Scatter(
        x=x,
        y=factor.mav[0],
        mode='lines+markers',
        name='5日均线',
        hovertext=stock.time,
        line={
            'width': .7
        }
    )
    data = [trace1, trace2, mav]
    layout = go.Layout(
        title=dayline.iloc[1, 2],
        legend={
            'x': 1,
            'y': 1
        },
        font={
            'size': 15,
            'family': 'sans-serif'
        },
        xaxis={
            'tickvals': np.arange(0, len(stock.close), 20),
            'ticktext': stock.time[::20],
            'showgrid': True
        }
    )
    fig = go.Figure(data=data, layout=layout)
    print('loading ohlc...')
    if len(stock.close) > 60:
        print('data is too much, need to wait...')
    for i in range(len(stock.close)):
        if strategy.rise_strategy[i]:
            fig.add_shape(
                type='line',
                x0=i,
                y0=stock.low[i],
                x1=i,
                y1=stock.high[i],
                line={
                    'color': 'red'
                }
            )
            fig.add_shape(
                type='line',
                x0=i - .3,
                y0=stock.open[i],
                x1=i,
                y1=stock.open[i],
                line={
                    'color': 'red'
                }
            )
            fig.add_shape(
                type='line',
                x0=i,
                y0=stock.close[i],
                x1=i + .3,
                y1=stock.close[i],
                line={
                    'color': 'red'
                }
            )
        else:
            fig.add_shape(
                type='line',
                x0=i,
                y0=stock.low[i],
                x1=i,
                y1=stock.high[i],
                line={
                    'color': 'green'
                }
            )
            fig.add_shape(
                type='line',
                x0=i - .3,
                y0=stock.open[i],
                x1=i,
                y1=stock.open[i],
                line={
                    'color': 'green'
                }
            )
            fig.add_shape(
                type='line',
                x0=i,
                y0=stock.close[i],
                x1=i + .3,
                y1=stock.close[i],
                line={
                    'color': 'green'
                }
            )
    print('done')
    plotly.offline.plot(fig)
