"""
this module is for each filter implementation
get params from ui directly
"""
import fetch
from datetime import datetime, date
from tkinter import messagebox
import pandas


def process_filters(stock, period, filters_params):
    # FIXME: should run strict filter first(may save the following filter)
    match = True
    for filt_params in range(len(filters_params)):
        filt = filters_params[filt_params][0]
        params = filters_params[filt_params][1:]
        if not filt(stock, period, params):
            match = False
            break

    if match:
        return stock
    return False
        

def process_stocks(stocks, period, filters_params, show_msg_box=True):
    """
    deal with 'stock' paramter and bypass other params to specified filter
    """
    # check params
    if not stocks or not period or not filters_params:
        title = 'Insufficient Input'
        msg = ''
        if not stocks:
            msg += 'no stock(s)\n'
        if not period:
            msg += 'no date\n'
        if not filters_params:
            msg += 'no filter parameter(s)\n'
        if show_msg_box:
            messagebox.showerror(title, msg)
        return -1 # 0 may be used as match number

    not_in_table = []
    if stocks == 'all':
        stock_list = fetch.stock_table.index
    else:
        stocks = stocks.split(',')
        stock_list = [stock for stock in stocks if stock in fetch.stock_table.index]
        not_in_table = [stock for stock in stocks if stock not in stock_list]

    match = []
    for stock in stock_list:
        res = process_filters(stock, period, filters_params)
        if res:
            match.append(res)

    if match and show_msg_box:
        messagebox.showinfo('Match', match)
    elif not match and show_msg_box:
        messagebox.showinfo('No match', 'No match')
    if not_in_table and show_msg_box:
        messagebox.showwarning('Not in table', not_in_table)

    return len(match)


def is_high(param):
    """ determine whether param is high or not """
    if param in ['high', 'hi', 'h', 'up', 'u', 'top', 't']:
        high = True
    elif param in ['low', 'l', 'down', 'd', 'bottom', 'b']:
        high = False
    else:
        messagebox.showerror('error', 'invalid high/low')

    return high


def new_price_in_n_days(stock, period, params):
    """
    filter out price if it's new high/low in specified days
    """
    # parse params
    days = int(params[0])
    if days <= 0:
        messagebox.showerror('error', 'days can\'t be <= 0')
        return -1
    high = is_high(params[1])

    # -1 for it's included
    res = fetch.fetch_price(stock, period, days - 1)
    if res[0] == False: # empty files for half of a year
        return False
    else:
        df = res[1]

    # be compatible between twse/otc
    if fetch.stock_table.loc[stock]['TWSE/OTC'] == '上櫃':
        price_label = '收盤'
    else:
        price_label = '收盤價'
    
    if high:
        res = pandas.stats.moments.rolling_max(df[price_label], days)
    else:
        res = pandas.stats.moments.rolling_min(df[price_label], days)
    res = (res == df[price_label])

    if True in list(res):
        return True
    else:   
        return False


def new_revenue_in_n_months(stock, period, params):
    """
    filter out revenue if it's new high/low in specified months
    """
    months = int(params[0])
    if months <= 0:
        messagebox.showerror('error', 'months can\'t be <= 0')
        return -1
    high = is_high(params[1])

    res = fetch.fetch_revenue(stock, period, months - 1)
    if res[0] == False:
        return False
    else:
        df = res[1]

    if high:
        res = pandas.stats.moments.rolling_max(df['營業收入'], months)
    else:
        res = pandas.stats.moments.rolling_min(df['營業收入'], months)
    res = (res == df['營業收入'])

    if True in list(res):
        return True
    else:
        return False


