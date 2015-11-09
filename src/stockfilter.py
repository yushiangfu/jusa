
def process_filter(ft, stocks, date, ft_params):
    print('hi, got you in process_filter()')
    print(ft, stocks, date, ft_params)
    if ft:
        ft(stocks, date, ft_params)



def new_price_in_n_days(stocks, date, ft_params):
    print('hi, got you in new_price_in_n_days')
    print(stocks, date, ft_params)


