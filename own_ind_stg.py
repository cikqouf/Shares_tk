import Shares_tk as stk
"""This is a template for your own indicator and strategy struct, 
here recommanding using `list` to design your indicator, of course 
you can use your own way to design your own indicator.
below is an example for mav indicator's template and a simple strategy
template based on mav.
"""


def own_ind(stock: stk.Stock_tk, **kwargs: tuple) -> dict[str, float]:
    def mav(*args) -> list[float]:
        ls: list[float] = [[None if i < args[k] - 1 else sum(stock.c[(i - args[k] + 1): (
            i + 1)]) / args[k] for i in range(len(stock.c))] for k in range(len(args))]
        return ls

    for k, v in kwargs.items():
        if k == 'mav':
            kwargs[k] = mav(*v)
    return kwargs


def own_stg(stock: stk.Stock_tk, ind: dict[str, float]) -> list[bool]:
    def long_s(stock, ind) -> list[bool]:
        ls = [ind['mav'][0][i] > stock.c[i]
              for i in range(4, len(stock.c))]
        return ls

    def short_s(stock, ind) -> list[bool]:
        ls = [ind['mav'][0][i] <= stock.c[i]
              for i in range(4, len(stock.c))]
        return ls
    stg_ls = long_s(stock, ind)
    return stg_ls
