"""
this module is for each filter implementation
get params from ui directly
"""
import fetch

def process_filter(ift, stocks, date, ft_params):
    """
    deal with 'stock' paramter and bypass other params to specified filter
    """
    if not (ift and stocks and date):
        # FIXME, replace to msg box
        print('insufficient input of stocks/date/ft_params')

    fetch.update_index()

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
                        print(line[i])
                        ift(line[i], date, ft_params)
    else:
        ift(stocks, date, ft_params)


def new_price_in_n_days(stock, date, ft_params):
    """
    filter out price if it's new high/low in specified days
    """
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

    try:
        price_data_str = fetch.fetch_data(stock, date, days - 1, 'stock price',
                                          '收盤價') # 1 is included in date
        price_data = [float(i.replace(',', '')) for i in price_data_str]
        if high:
            res = [float('nan')] * (days - 1) + [price_data[i] > \
                max(price_data[i-(days-1):i]) \
                for i in range(days - 1, len(price_data))]
        else:
            res = [float('nan')] * (days - 1) + [price_data[i] < \
                min(price_data[i-(days-1):i]) \
                for i in range(days - 1, len(price_data))]

        if True in res:
            print(stock, 'matched')
    except ValueError:
        print(stock, price_data_str, 'format error')

