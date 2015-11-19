"""
this module is for each filter implementation
get params from ui directly
"""
import fetch
from datetime import datetime, date
from dateutil import relativedelta
import csv

def process_filter(stocks, period, filters):
    """
    deal with 'stock' paramter and bypass other params to specified filter
    """
    fetch.update_index() # FIXME: move to suitable place if possible

    if not (stocks and period):
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
                        match = True
                        for j in range(len(filters)):
                            ift = filters[j][0]
                            ft_params = filters[j][1]
                            if not ift(line[i], period, ft_params):
                                match = False
                                break
                        if match:
                            print(line[i], 'match')

    else:
        for j in range(len(filters)):
            ift = filters[j][0]
            ft_params = filters[j][1]
            ift(stocks, period, ft_params)


def new_revenue_in_n_months(stock, _, ft_params):
    """
    filter out revenue if it's new high/low in specified months
    """
    months = int(ft_params[0])
    if months <= 0:
        print('error, days can\'t be <= 0') # FIXME, replace to msg box
        return
    high_str = ft_params[1]
    if high_str in ['high', 'hi', 'h', 'up', 'u', 'top', 't']:
        high = 1
    elif high_str in ['low', 'l', 'down', 'd', 'bottom', 'b']:
        high = 0
    else:
        print('error, months can\'t be <= 0') # FIXME, replace to msg box

    try:
        revenue_data_str = fetch.fetch_revenue(stock, months)
        revenue_data = [float(i.replace(',', '')) for i in revenue_data_str]
        if high:
            res = [float('nan')] * (months - 1) + [revenue_data[i] > \
                max(revenue_data[i-(months-1):i]) \
                for i in range(months - 1, len(revenue_data))]
        else:
            res = [float('nan')] * (months - 1) + [revenue_data[i] < \
                min(revenue_data[i-(months-1):i]) \
                for i in range(months - 1, len(revenue_data))]

        if True in res:
            return True
        else:
            return False
            

    except ValueError:
        print(stock, price_data_str, 'format error')

    


def new_price_in_n_days(stock, idate, ft_params):
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


    if '-' in idate: # period
        [start, end] = idate.split('-')
        start_dt = datetime.strptime(start, '%Y/%m/%d').date()
        end_dt = datetime.strptime(end, '%Y/%m/%d').date()
    else: # single day
        if idate == 'today':
            start_dt = date.today()
        else:
            start_dt = datetime.strptime(idate, '%Y/%m/%d').date()
        end_dt = start_dt


    try:
        price_data_str = fetch.fetch_price(stock, start_dt, end_dt, days - 1, '收盤價') # 1 is included in date
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
            return True
        else:   
            return False
    except ValueError:
        print(stock, price_data_str, 'format error')

