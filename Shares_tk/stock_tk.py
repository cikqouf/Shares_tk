import configparser as cpr


class Stock_tk():
    def __init__(self) -> None:
        """A `stock_tk()` has seven basic attributes:

        `o` stands for open price,
        `h` stands for high price,
        `l` stands for low price,
        `c` stands for close price,
        `vol` stands for deal volume,
        `amo` stands for deal amount,
        and `t` stands for deal time in a period.
        """
        self.o: list[float] = []
        self.h: list[float] = []
        self.l: list[float] = []
        self.c: list[float] = []
        self.vol: list[float] = []
        self.amo: list[float] = []
        self.t: list[str] = []

    def read(self, file: str) -> None:
        """read a csv file to get a stock's basic data
        """
        # 股票csv数据储存为一个2d list
        with open(file, encoding='utf-8') as f:
            text: list[str] = []
            for r in f.readlines():
                text.append(r.split(','))
            f.close()
        """下面的`tuple`存了常见的股票数据栏的台头, 并将对应列写入配置文件`config.ini',
        可以自行修改.
        """
        config = cpr.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        # Initial config
        sec_ls: list[str] = ['csv_data_column',
                             'indicator', 'strategy', 'others']
        # -------------------------
        cdc_ls: list[str] = ['open', 'high',
                             'low', 'close', 'vol', 'amo', 'time']
        ind_ls: list[str] = ['mav', 'mav_diff']
        stg_ls: list[str] = ['buy', 'sell', 'add', 'sub']
        ots_ls: list[str] = ['name', 'code']
        if config.sections() != sec_ls:
            for sec in sec_ls:
                if not config.has_section(sec):
                    config.add_section(sec)
            # -------------------------------
            for ls in cdc_ls:
                config.set('csv_data_column', ls, '')
            for ls in ind_ls:
                config.set('indicator', ls, '')
            for ls in stg_ls:
                config.set('strategy', ls, '')
            for ls in ots_ls:
                config.set('others', ls, '')
        # -----------------------------------------------------
        item_tuple = (("open",
                       "Open",
                      "o",
                       "开盘价"),
                      ("high",
                       "High",
                      "h",
                       "最高价"),
                      ("low",
                       "Low",
                      "l",
                       "最低价"),
                      ("close",
                       "Close",
                      "c",
                       "收盘价"),
                      ("volume",
                       "Volume",
                      "vol",
                       "v",
                       "成交量"),
                      ("amount",
                       "Amount",
                      "amo",
                       "a",
                       "成交额"),
                      ("date",
                       "Date",
                      "time",
                       "Time",
                       "日期"))
        # set csv_data_column
        # `iter` is a mapping for `csv_data_column` index
        iter: int = -1
        for target in item_tuple:
            iter += 1
            for sub_target in target:
                if sub_target in text[0]:
                    config.set('csv_data_column',
                               config.items('csv_data_column')[iter][0],
                               str(text[0].index(sub_target)))
                    with open('config.ini', 'w') as f:
                        config.write(f)
                        f.close()
        # 根据配置文件读取数据
        for data in text[1:]:
            self.o.append(float(data[int(config['csv_data_column']['open'])]))
            self.h.append(float(data[int(config['csv_data_column']['high'])]))
            self.l.append(float(data[int(config['csv_data_column']['low'])]))
            self.c.append(float(data[int(config['csv_data_column']['close'])]))
            self.vol.append(float(data[int(config['csv_data_column']['vol'])]))
            self.amo.append(float(data[int(config['csv_data_column']['amo'])]))
            self.t.append(data[int(config['csv_data_column']['time'])])

    def indicator(self, **kwargs: list) -> dict[str, list]:
        """indicator methods:

        usage::

        ```
        stock = stock_tk()
        stock.read('your_csv_file')
        ind = stock.indicator(mav=(5, 10, 20), 
                              mav_diff=((5, 10), (10, 20)))
        ```

        Returns:
            dict[str, list]: `ind` is a `dict`, like

        ```
            print(ind['mav'])
        ```
        """

        def mav(*args: int) -> list[float]:
            """args expects a tuple contains mav periods

            Returns:
                list[float]: a list contains mav every period
            """
            ls: list[float] = [[None
                               if i < args[k] - 1
                                else
                                sum(self.c[(i - args[k] + 1)
                                    : (i + 1)]) / args[k]
                                for i in range(len(self.c))]
                               for k in range(len(args))]
            return ls

        def mav_diff(*args: int) -> list[float]:
            """args expects a pair of tuple, like
            `((a, b), (c, d), ...)`

            Returns:
                list[float]: a list contains mav_diff by `a-b`, `c-d`, ...
            """
            pair_ls: list[float] = [mav(*args[i]) for i in range(len(args))]
            # get the max time
            max_t: list[float] = [args[i][0] if args[i][0] >= args[i][1] else args[i][1]
                                  for i in range(len(args))]
            ls: list[float] = [[None
                               if i < max_t[k] - 1
                               else
                               # default `a - b` in a sub tuple `(a, b)`
                                pair_ls[k][0][i] - pair_ls[k][1][i]
                                for i in range(len(self.c))]
                               for k in range(len(args))]
            return ls

        for k, v in kwargs.items():
            if k == 'mav':
                kwargs[k] = mav(*v)
            if k == 'mav_diff':
                kwargs[k] = mav_diff(*v)

        return kwargs
