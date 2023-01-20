"""
A framework for technique of a stock

usage::

    import Shares_tk as stk
    stock = Stock_tk()
    stock.read('your_csv_file')

"""
from Shares_tk.shares_tk import Stock_tk
from Shares_tk.chart_matplotlib_ver import technic_chart_matplotlib
from Shares_tk.chart_plotly_ver import technic_chart_plotly