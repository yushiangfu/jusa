import urllib.request
from datetime import datetime, timedelta
import dateutil
from dateutil import rrule, relativedelta
import csv

# called from each filter
def fetch_data(stock, date, addition, category, field = None):
    if '-' in date: # period
        [start, end] = date.split('-')
        start_dt = datetime.strptime(start, '%Y/%m/%d').date()
        end_dt = datetime.strptime(end, '%Y/%m/%d').date()
    else: # single day
        start_dt = datetime.strptime(date, '%Y/%m/%d').date()
        end_dt = start_dt

    # case: stock price 
    if category == 'stock price':
        return fetch_stock_price(stock, start_dt, end_dt, addition, field)



def fetch_stock_price(stock, start_dt, end_dt, addition, field = None):
    dt  = end_dt
    res = []
    while dt.month >= start_dt.month or addition:
        filename = 'data/' + stock + '/' + 'price-' + str(dt.year) + '-' + ('%02d') % (dt.month) + '.txt'
        if not os.path.exists('data/' + stock):
            os.mkdir('data/' + stock)
        # FIXME: don't need to fetch from url everytime
        #fetch_stock_price_from_url(stock, dt, filename)

        f = open(filename, 'r')
        next(f, None) # to skip header
        csvf = csv.DictReader(f, delimiter = ',')
        for row in reversed(list(csvf)):
            [year, month, day] = row['日期'].split('/')
            csv_dt = datetime(int(year) + 1911, int(month), int(day)).date()
            if csv_dt > end_dt:
                continue
            elif csv_dt < start_dt and not addition:
                return res
            else:
                if field:
                    res.append(row[field])
                else:
                    res.append(row)

            if csv_dt < start_dt:
                addition -= 1
        f.close()
        dt -= relativedelta.relativedelta(months = 1)    
     
    return res


def fetch_stock_price_test(stock, date, addition, category, expect, field = None):
    res = fetch_data(stock, date, addition, category, field)
    if res == expect:
        print('pass')
    else:
        print('fail, res: ', res, 'expect: ', expect)
    



def fetch_stock_price_tests():
    print('fetch_stock_price_tests:')

    # both period date & addtion step across month
    expect = ['196.50', '194.50', '190.50', '193.50', '194.00', '195.50', '197.50', '195.00', '197.00', '202.50', '200.00', '190.50', '186.50', '186.50', '184.50', '187.00', '183.50', '181.50', '182.00', '183.50', '180.50', '182.50', '180.00', '177.00', '174.00', '178.50', '179.50', '187.50']
    res = fetch_stock_price_test('9914', '2015/10/1-2015/11/3', 5, 'stock price', expect, '收盤價')

    # single date
    expect = ['180.00']
    res = fetch_stock_price_test('9914', '2015/10/1', 0, 'stock price', expect, '收盤價')

    # single date, addition steps across month
    expect = ['180.00', '177.00', '174.00']
    res = fetch_stock_price_test('9914', '2015/10/1', 2, 'stock price', expect, '收盤價')

    # period date, addition steps across month
    expect = ['180.50', '182.50', '180.00', '177.00', '174.00']
    res = fetch_stock_price_test('9914', '2015/10/1-2015/10/5', 2, 'stock price', expect, '收盤價')

    # period date, addition steps across month, full data
    expect = [{'最低價': '180.00', '成交股數': '409,897', '成交筆數': '386', '漲跌價差': '-2.00', '成交金額': '74,278,754', '日期': ' 104/10/05', '收盤價': '180.50', '開盤價': '184.00', '最高價': '184.00'}, {'最低價': '178.00', '成交股數': '962,273', '成交筆數': '630', '漲跌價差': '+2.50', '成交金額': '174,530,819', '日期': ' 104/10/02', '收盤價': '182.50', '開盤價': '179.50', '最高價': '183.00'}, {'最低價': '176.50', '成交股數': '1,217,096', '成交筆數': '1,075', '漲跌價差': '+3.00', '成交金額': '219,720,184', '日期': ' 104/10/01', '收盤價': '180.00', '開盤價': '177.00', '最高價': '183.00'}, {'最低價': '171.50', '成交股數': '2,593,029', '成交筆數': '1,601', '漲跌價差': '+3.00', '成交金額': '455,027,604', '日期': ' 104/09/30', '收盤價': '177.00', '開盤價': '172.00', '最高價': '177.50'}, {'最低價': '174.00', '成交股數': '805,838', '成交筆數': '683', '漲跌價差': '-4.50', '成交金額': '142,120,650', '日期': ' 104/09/25', '收盤價': '174.00', '開盤價': '181.00', '最高價': '181.00'}]
    res = fetch_stock_price_test('9914', '2015/10/1-2015/10/5', 2, 'stock price', expect)

    # period date steps across month, addition
    expect =  ['180.50', '182.50', '180.00', '177.00', '174.00', '178.50', '179.50', '187.50']
    res = fetch_stock_price_test('9914', '2015/9/25-2015/10/5', 3, 'stock price', expect, '收盤價')

    # period date steps across month, addition, full data
    expect = [{'成交筆數': '386', '日期': ' 104/10/05', '成交股數': '409,897', '最高價': '184.00', '成交金額': '74,278,754', '漲跌價差': '-2.00', '開盤價': '184.00', '收盤價': '180.50', '最低價': '180.00'}, {'成交筆數': '630', '日期': ' 104/10/02', '成交股數': '962,273', '最高價': '183.00', '成交金額': '174,530,819', '漲跌價差': '+2.50', '開盤價': '179.50', '收盤價': '182.50', '最低價': '178.00'}, {'成交筆數': '1,075', '日期': ' 104/10/01', '成交股數': '1,217,096', '最高價': '183.00', '成交金額': '219,720,184', '漲跌價差': '+3.00', '開盤價': '177.00', '收盤價': '180.00', '最低價': '176.50'}, {'成交筆數': '1,601', '日期': ' 104/09/30', '成交股數': '2,593,029', '最高價': '177.50', '成交金額': '455,027,604', '漲跌價差': '+3.00', '開盤價': '172.00', '收盤價': '177.00', '最低價': '171.50'}, {'成交筆數': '683', '日期': ' 104/09/25', '成交股數': '805,838', '最高價': '181.00', '成交金額': '142,120,650', '漲跌價差': '-4.50', '開盤價': '181.00', '收盤價': '174.00', '最低價': '174.00'}, {'成交筆數': '654', '日期': ' 104/09/24', '成交股數': '720,705', '最高價': '183.00', '成交金額': '129,004,285', '漲跌價差': '-1.00', '開盤價': '180.00', '收盤價': '178.50', '最低價': '176.00'}, {'成交筆數': '805', '日期': ' 104/09/23', '成交股數': '895,266', '最高價': '186.00', '成交金額': '162,593,880', '漲跌價差': '-8.00', '開盤價': '186.00', '收盤價': '179.50', '最低價': '179.50'}, {'成交筆數': '675', '日期': ' 104/09/22', '成交股數': '714,183', '最高價': '187.50', '成交金額': '132,046,221', '漲跌價差': '+4.50', '開盤價': '183.00', '收盤價': '187.50', '最低價': '181.00'}]
    res = fetch_stock_price_test('9914', '2015/9/25-2015/10/5', 3, 'stock price', expect)

    # period date steps across month
    expect =  ['180.50', '182.50', '180.00', '177.00', '174.00']
    res = fetch_stock_price_test('9914', '2015/9/25-2015/10/5', 0, 'stock price', expect, '收盤價')

    # period date steps across month, full data
    expect = [{'最低價': '180.00', '成交股數': '409,897', '成交筆數': '386', '漲跌價差': '-2.00', '成交金額': '74,278,754', '日期': ' 104/10/05', '收盤價': '180.50', '開盤價': '184.00', '最高價': '184.00'}, {'最低價': '178.00', '成交股數': '962,273', '成交筆數': '630', '漲跌價差': '+2.50', '成交金額': '174,530,819', '日期': ' 104/10/02', '收盤價': '182.50', '開盤價': '179.50', '最高價': '183.00'}, {'最低價': '176.50', '成交股數': '1,217,096', '成交筆數': '1,075', '漲跌價差': '+3.00', '成交金額': '219,720,184', '日期': ' 104/10/01', '收盤價': '180.00', '開盤價': '177.00', '最高價': '183.00'}, {'最低價': '171.50', '成交股數': '2,593,029', '成交筆數': '1,601', '漲跌價差': '+3.00', '成交金額': '455,027,604', '日期': ' 104/09/30', '收盤價': '177.00', '開盤價': '172.00', '最高價': '177.50'}, {'最低價': '174.00', '成交股數': '805,838', '成交筆數': '683', '漲跌價差': '-4.50', '成交金額': '142,120,650', '日期': ' 104/09/25', '收盤價': '174.00', '開盤價': '181.00', '最高價': '181.00'}]
    res = fetch_stock_price_test('9914', '2015/9/25-2015/10/5', 0, 'stock price', expect)

    # period date
    expect =  ['180.50', '182.50', '180.00']
    res = fetch_stock_price_test('9914', '2015/10/1-2015/10/5', 0, 'stock price', expect, '收盤價')

    # period date, full data
    expect = [{'成交金額': '74,278,754', '漲跌價差': '-2.00', '開盤價': '184.00', '成交股數': '409,897', '最低價': '180.00', '收盤價': '180.50', '成交筆數': '386', '最高價': '184.00', '日期': ' 104/10/05'}, {'成交金額': '174,530,819', '漲跌價差': '+2.50', '開盤價': '179.50', '成交股數': '962,273', '最低價': '178.00', '收盤價': '182.50', '成交筆數': '630', '最高價': '183.00', '日期': ' 104/10/02'}, {'成交金額': '219,720,184', '漲跌價差': '+3.00', '開盤價': '177.00', '成交股數': '1,217,096', '最低價': '176.50', '收盤價': '180.00', '成交筆數': '1,075', '最高價': '183.00', '日期': ' 104/10/01'}]
    res = fetch_stock_price_test('9914', '2015/10/1-2015/10/5', 0, 'stock price', expect)



def fetch_stock_price_from_url(stock, date, filename):
    if stock == 'index':
        url = ('http://www.twse.com.tw' +
                '/ch/trading/exchange/FMTQIK/FMTQIK2.php' +
                '?STK_NO=&myear=%(year)d&mmon=%(month)2d&type=csv') % {
                'year': date.year,
                'month': date.month}
    else:
        url = ('http://www.twse.com.tw' +
                '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' +
                '?genpage=genpage/Report%(year)d%(month)02d/' + 
                '%(year)d%(month)02d_F3_1_8_%(stock)s.php&type=csv') % {
                'year': date.year,
                'month': date.month,
                'stock': stock}

    # write file after decoding
    with urllib.request.urlopen(url) as response, open(filename, 'w') as out_file:
        out_file.write(response.read().decode('big5hkscs')) # for '恒', '碁'
        

import os
import filecmp
def fetch_stock_price_from_url_test(stock, year, month, filename, expect_url, expect_filename):

    # output
    if os.path.exists(filename):
        os.remove(filename)
    dt = datetime(year, month, day = 1) # dont't mind, day won't be used
    fetch_stock_price_from_url(stock, dt, filename)

    # expect
    if os.path.exists(expect_filename):
        os.remove(expect_filename)
    with urllib.request.urlopen(expect_url) as response, open(expect_filename, 'w') as expect_file:
        expect_file.write(response.read().decode('big5hkscs')) 

    if filecmp.cmp(filename, expect_filename): # same
        print('pass')
    else:
        print('fail')


def fetch_stock_price_from_url_tests():
    print('fetch_stock_price_from_url_tests:')

    # trivial test
    fetch_stock_price_from_url_test('2415', 2015, 11, '/tmp/2415.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_2415.php&type=csv',
        '/tmp/2415.expect')

    # test for index
    fetch_stock_price_from_url_test('index', 2015, 11, '/tmp/index.output', 
        'http://www.twse.com.tw/ch/trading/exchange/FMTQIK/FMTQIK2.php?STK_NO=&myear=2015&mmon=11&type=csv',
        '/tmp/index.expect')

    # test for 'T' in '01002T'
    fetch_stock_price_from_url_test('01002T', 2015, 11, '/tmp/01002T.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_01002T.php&type=csv',
        '/tmp/01002T.expect')

    # test for six numbers in '911616'
    fetch_stock_price_from_url_test(911616, 2015, 11, '/tmp/911616.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_911616.php&type=csv',
        '/tmp/911616.expect')

    # test for '恒', '碁' in content
    fetch_stock_price_from_url_test(910708, 2015, 11, '/tmp/910708.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_910708.php&type=csv',
        '/tmp/910708.expect')
    
if __name__ == '__main__':
    fetch_stock_price_tests()
    fetch_stock_price_from_url_tests()
