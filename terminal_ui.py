import stock_framework as sf
# terminal ui


def terminal_ui():
    print('Terminal Ui of stock info get and deal')
    print('1. matplotlib_chart \n\
2. plotly_chart\n\
3. clean csv and tmp file')
    x = int(input())
    if x == 1:
        sf.technic_chart_matplotlib(dayline='')
        terminal_ui()
    elif x == 2:
        sf.technic_chart_plotly()
        terminal_ui()
    elif x == 3:
        sf.clean_tmp_file()
        terminal_ui()


terminal_ui()
