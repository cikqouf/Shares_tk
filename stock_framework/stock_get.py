import requests


def stock_get():
    print('输入股票代码: ', end='')
    stock_code = input()
    print('输入起始日期: ', end='')
    start_date = input()
    stock_get_code(stock_code, start_date)


def stock_get_code(stock_code, start_date):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        'Referer': "https://baidu.com/"
    }
    s = requests.session()
    s.keep_alive = False
    if int(stock_code) < 100000:
        stock_data = requests.get(
            "https://quotes.money.163.com/service/chddata.html?code=1"
                + stock_code + '&start=' + start_date, headers=headers)
    else:
        stock_data = requests.get(
            "https://quotes.money.163.com/service/chddata.html?code=0"
                + stock_code + '&start=' + start_date, headers=headers)
    stock_data.encoding="gb18030"
    with open('csv/' + stock_code + '.csv', 'w', encoding='utf8') as f_1:
        print(stock_data.text, file=f_1)
