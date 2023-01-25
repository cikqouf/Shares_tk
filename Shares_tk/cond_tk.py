import os

class Cond_tk():
    def set_cond(self, name: str, cal: list[str]) -> None:
        """
        This method is to generate a `.py` file by template of condtion expressions, 
        and `.py` file is saved at `pwd/own_cond`, you can use the generated `.py` 
        method by ::
        
        ```
        import Shares_tk as stk
        from own_cond.the_name_of_your_cond import the_name_of_your_cond
        
        stock = stk.Stock_tk()
        period = [5, 10, 20]
        
        kwargs = ...
        cond = the_name_of_your_cond(stock=stock, period=period, kwargs=kwargs)
        ``` 
        and `cond` is a 2-d `list`, the row index is devided by `period`, 
        ```
        cond[0] # a 1-d `list` when period[0] = 5
        ...
        ```
        
        the template have three key words::
        
        ```
        ls # stands for the 2-d `list` of conditions to return
        p # element in `period` list
        r # stands for row index of `ls`
        ```
        
        We recommand be careful to use the key words above for your `cal`, which 
        stands for 'the calculation method of your condition expression', 
        usually, `cal` is a list with two elements in it, like
        ```
        cal = [default_cal_method_before_the_first_whole_period:str,
                cal_method_after_a_whole_period:str]
        ```
        And below is a good way to generate as many condition expressions as you want, for example ::
        
        ```
        import Shares_tk as stk
        cond = stk.Cond_tk()
        
        cond_dict = {
        'name': 'A_cond',
        'cal': [1>0,
            r""\"
            stock.c[i] > stock.o[i]
            ""\"]}
        cond.set_cond(**cond_dict)

        cond_dict = {
            'name': 'B_cond',
            'cal': [1>0,
                r""\"
                kwargs['A_ind'][r][i] > 0
                ""\"]}
        cond.set_cond(**cond_dict)
        ...
        ``` 
        Now you can enjoy the condition expressions you have just created.
        
        `period` in this template is for in some cases, the condition expressions are 
        created by cycle indicators.
        ```
        import Shares_tk as stk
        from own_cond.A_cond import A_cond
        from own_cond.B_cond import B_cond
        stock = stk.Stock_tk()
        stock.read(your_csv_file_path)

        ind_a:list[float]: [[]]
        period = [9]
        stg_A_cond = A_cond(stock, period)
        period = [3]
        stg_B_cond = b_cond(stock, period, A_ind=ind_a)
        
        # now you can create a srtategy signal by 
        # below
        stg_signal = ['signal' if cond else '' for cond in stg_A_cond[0]]
        ...
        ```
        """
        if not os.path.exists('own_cond'):
            os.mkdir('own_cond')
        with open('own_cond/'+name+'.py', 'w') as file:
            tplt = f"""
def {name}(stock, period:list[int], **kwargs:list[float]) -> list[bool]:
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