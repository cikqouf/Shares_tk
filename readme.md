# Shares tech anal

## 声明

本项目不为任何因使用本项目代码参与经济活动等造成的经济损失或获利负责.

## 简述

这是一个方便股票技术分析的python模块，可以配合图形库，实现可视化

### 特色

- 方便自定义各种技术(尤其是周期性的)指标和条件

### 快速上手

```
import Shares_tk as stk
stock = stk.Stock_tk()
stock.read('your_csv_file_path') # here to get a stock's ohlcvat data

# you can draw a chart of close price

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, len(stock.c))
plt.plot(x, stock.c, 'o-') # 绘制收盘价点线图
plt.show()
```

指标设置繁复多样, 本模块提供一个算周期指标的模板, 用法如下
```
import Shares_tk as stk

ind = stk.Indicator()

ind_args = {
    'name': 'your_ind_name', # 指标的名字
    'cal': [cal1:str,cal2:str] 
    # cal1 是第一个完整周期出现之前的计算式
    # cal2 是之后的每个周期的计算式
}

ind.set_cycle_ind(**ind_args)
```

如设置一个rsv指标

```
import Shares_tk stk

ind = stk.Indicator()

ind_args = {
    'name' = 'rsv'
    'cal' = [None,
    r"""
    (stock.c[i] - min(stock.l[i-p+1:i+1]))/(max(stock.h[i-p+1:i+1])-min(stock.l[i-p+1:i+1]))
    """]
}

ind.set_cycle_ind(**ind_args)

# 运行这个脚本, 会在当前工作目录创建一个名为`own_ind`的文件夹, 包含文件`rsv.py`
# 接下来调用这个文件中的方法`rsv(stock, period:list[int], **kwargs)`

from own_ind.rsv import rsv

stock = stk.Stock_tk()
stock.read('your_csv_file_path')
ind_rsv = rsv(stock=stock,
              period=[9, 18, 27])
# `ind_rsv`是一个二维列表, 行指标按照每一个周期计算的指标储存列表
# 例如要查看 9 日的 rsv 指标数据
print(ind_rsv[0])
# 查看 18 日的 rsv 指标数据
print(ind_rsv[1])
```

由于`own_ind`文件夹下的`.py`文件是模板生成的, 所以有几个关键字注意小心使用

`ls` 是`.py`文件中方法的返回值, 考虑有些指标需要用到指标本身的数据, 可以这样实现
```
...
ind_args = {
    'name' = 'ind_a',
    'cal' = [10,
    r"""
    ls[i] = ls[i - 1]/2
    """]
}
...
```
这样运行`ind_a`方法后的内容如下

`[[10, 10, 10, ..., 10 #第一个周期结束, 5, 2.5, ...], # 其他周期[...],[...],[],...]`

`r`是参数的行指标, `i`是参数的列指标, 如
```
...
ind_args = {
    'name' = 'ind_a',
    'cal' = [10,
    r"""
    kwargs['rsv'][r][i] - stock.c[i]
    """]
}
...
```
然后调用生成的`ind_a.py`中的`ind_a`方法

```
from own_ind.ind_a import ind_a
from own_ind.rsv import rsv
import Shares_tk as stk

stock = stk.Shares_tk()
stock.read(your_csv_file_path)

ind_rsv = rsv(stock=stock,
              period=[9, 18, 27])

ind_a = ind_a(stock=stock,
              period=[5, 10, 20],
              rsv=ind_rsv)
```

`p`是周期的值, 如计算移动平均收盘价
```
...
ind_args = {
    'name': 'mav',
    'cal': [None,
    r"""
    stock.c[i-p+1:i+1]/p
    """]
}
...
```

## 回测指标(考虑加入)

- 最大资金使用率
- 测试天数
- 测试周期数
- 信号个数
- 初始资金
- 最大资金利用率
- 杠杆倍数
- 收益
- 收益率
- 年化单利收益率
- 夏普比率
- 权益最大回撤
- 权益最大回撤比率
- 胜率
- 盈亏比率
- 最大每手盈利
- 最大每手亏损
- 手续费
- 手续费/收益
- vwap算法、twap算法
