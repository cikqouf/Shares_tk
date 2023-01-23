import os

class Indicator_tk():
    def set_cycle_ind(self, name: str, cal: list[str]) -> None:
        """
        This method is to generate a `.py` file by template of cycle indicators, 
        and `.py` file is saved at `pwd/own_ind`, you can use the generated `.py` 
        method by ::
        
        ```
        import Shares_tk as stk
        from own_ind.the_name_of_your_ind import the_name_of_your_ind
        
        stock = stk.tock_tk()
        period = [5, 10, 20]
        
        kwargs = ...
        ind = the_name_of_your_ind(stock=stock, period=period, kwargs=kwargs)
        ``` 
        and `ind` is a 2-d `list`, the row index is devided by `period`, 
        ```
        ind[0] # a 1-d `list` when period[0] = 5
        ...
        ```
        
        the template have three key words::
        
        ```
        ls # stands for the 2-d `list` of cycle indicator to return
        p # element in `period` list
        r # stands for row index of `ls`
        ```
        
        We recommand be careful to use the key words above for your `cal`, which 
        stands for 'the calculation method of your cycle indicator', 
        usually, `cal` is a list with two elements in it, like
        ```
        cal = [default_cal_method_before_the_first_whole_period:str,
                cal_method_after_a_whole_period:str]
        ```
        And below is a good way to generate as many cycle indicators as you want, for example ::
        
        ```
        import Shares_tk as stk
        ind = stk.Indicator()
        
        ind_dict = {
        'name': 'rsv',
        'cal': [100,
            r""\"
            (stock.c[i] - min(stock.l[i-p+1 :i]))/(max(stock.h[i-p+1:i]) - min(stock.l[i-p+1:i]))*100
            ""\"]}
        ind.set_cycle_ind(**ind_dict)

        ind_dict = {
            'name': 'kdj_k',
            'cal': [100,
                    r""\"
        sum(kwargs['ind_rsv'][r][i-p+1:i])/p
            ""\"]}
        ind.set_cycle_ind(**ind_dict)
        ...
        ``` 
        Now you can enjoy the cycle indicator you have just created.
        ```
        import Shares_tk as stk
        from own_ind.kdj_k import kdj_k
        from own_ind.rsv import rsv
        stock = stk.Stock_tk()
        stock.read(your_csv_file_path)

        period = [9]
        ind_rsv = rsv(stock, period)
        period = [3]
        ind_kdj_k = kdj_k(stock, period, ind_rsv=ind_rsv)
        ...
        ```
        """
        if not os.path.exists('own_ind'):
            os.mkdir('own_ind')
        with open('own_ind/'+name+'.py', 'w') as file:
            tplt = f"""
def {name}(stock, period, **kwargs) -> list[float]:
    ls = []
    for i in range(len(period)):
        ls.append([])
    r:int = -1
    for p in period:
        r+=1
        for i in range(len(stock.c)):
            if i < p - 1:
                ls[r].append({cal[0]})
            else:
                ls[r].append({cal[1]})
    return ls
            """
            print(tplt, file=file)
            file.close()
