import stock_framework as sf
# terminal ui


def terminal_ui():
    print('Terminal Ui of stock info get and deal')
    print('1. get stock info from Netease \t 2. matplotlib_chart \n\
3. plotly_chart \t 4. cate_quick_check\n\
5. clean csv and tmp file')
    x = int(input())
    if x == 1:
        sf.stock_get()
        terminal_ui()
    elif x == 2:
        sf.technic_chart_matplotlib(dayline='')
        terminal_ui()
    elif x == 3:
        sf.technic_chart_plotly()
        terminal_ui()
    elif x == 4:
        sf.cate_quick_check()
        terminal_ui()
    elif x == 5:
        sf.clean_tmp_file()
        terminal_ui()

terminal_ui()
