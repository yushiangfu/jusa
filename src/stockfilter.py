import fetch

def process_filter(ft, stocks, date, ft_params):
    print('hi, got you in process_filter()')
    print(ft, stocks, date, ft_params)
    if not (ft and stocks and date):
        # FIXME, replace to msg box
        print('insufficient input of stocks/date/ft_params') 

    if stocks == 'all':
        # FIXME: if read from excel, fix here
        with open('doc/stock-table.txt', 'r') as csvfile: 
            for line in iter(csvfile.readline, b''):
                if not line: # empty line before EOF
                    break
                line = line.split() 
                for i in range(0, len(line), 2):
                    if line[i][0].isdigit(): # to avoid '上市'
                        if len(line[i]) <= 2: # incorrect cell format in excel
                            line[i] = '00' + line[i]
                    ft(line[i], date, ft_params)
    else:
        ft(stocks, date, ft_params)


def new_price_in_n_days(stocks, date, ft_params):
    print('hi, got you in new_price_in_n_days')
    print(stocks, date, ft_params)
    days = int(ft_params[0])
    if days <= 0:
        print('error, days can\'t be <= 0') # FIXME, replace to msg box
        return
    high_str = ft_params[1]
    if high_str in ['high', 'hi', 'h', 'up', 'u', 'top', 't']:
        high = 1
    elif high_str in ['low', 'l', 'down', 'd', 'bottom', 'b']:
        high = 0
    else:
        print('error, days can\'t be <= 0') # FIXME, replace to msg box

    print('a')
    price_data = fetch.fetch_data(stocks, date, days - 1, 'stock price', '收盤價') # 1 is included in date
    print('b')
    print(price_data)
    #res = [0] * len(price_data)
    #for day in price_data:
        
        
    


