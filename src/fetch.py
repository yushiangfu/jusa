"""
this module is for fetch utilities
"""
from urllib import request
from datetime import datetime, date
from dateutil import relativedelta
import csv
import os
from os import path
from bs4 import BeautifulSoup


def update_index():
    """ update index for each stock to refer to """
    for filename in os.listdir('data/index'):
        [_, filename_year, filename_month] = filename.split('-')
        filename_month = filename_month.replace('.txt', '')

        mod_dt = datetime.fromtimestamp(path.getmtime('data/index/' + filename)).date()
        if mod_dt.month <= int(filename_month):
            tmp_dt = datetime(int(filename_year), int(filename_month), 1).date()
            fetch_price_from_url('index', tmp_dt, '/tmp/' + filename)
            if path.getsize('/tmp/' + filename) > \
                    path.getsize('data/index/' + filename):
                print('real update index', filename)
                os.rename('/tmp/' + filename, 'data/index/' + filename)


def need_update_price(dt_iter, filename):
    """
    compare with index file so as not to update stock price everytime
    """
    [prefix, _, suffix] = filename.split('/')
    idx_filename = prefix + '/index/' + suffix

    if not os.path.exists('data/index'): # FIXME: move to first time setup
        os.mkdir('data/index')

    if not os.path.exists(idx_filename):
        fetch_price_from_url('index', dt_iter, idx_filename)
        return True
    elif not os.path.exists(filename):
        return True
    else: # both index/stock file exist
          # FIXME: when to update index file?
        idx_mtime = os.stat(idx_filename).st_mtime
        stock_mtime = os.stat(filename).st_mtime
        if idx_mtime > stock_mtime: # idx file is newer
            with open(idx_filename) as idx_file, open(filename) as stock_file:
                idx_lines = sum(1 for line in idx_file)
                stock_lines = sum(1 for line in stock_file)
                if idx_lines > stock_lines: # idx file data is more
                    return True
    return False

def need_update_revenue(filename):
    """
    compare with index file so as not to update stock price everytime
    """
    if not os.path.exists(filename):
        return True
    file_dt = datetime.fromtimestamp(path.getmtime(filename)).date()
    today_dt = date.today()
    if file_dt < today_dt:
        return True
    return False

def fetch_revenue(stock, months):
    """
    dispatched by fetch_data() to fetch revenue data within date from file
    download from url first if necessary
    """
    filename = 'data/' + stock + '/revenue.txt'
    if need_update_revenue(filename):
        fetch_revenue_from_url(stock, filename)
    
    res = []
    with open(filename, 'r') as revenue_f:
        csvf = csv.DictReader(revenue_f, delimiter=',')
        cnt = 0
        for row in csvf:
            res.append(row['營業收入'])
            cnt += 1
            if cnt >= months:
                break
    return res[::-1]

def fetch_price(stock, start_dt, end_dt, addition, field=None):
    """
    dispatched by fetch_data() to fetch price data within date from file
    download from url first if necessary
    """

    # FIXME: should consider case of stock without data
    dt_iter = end_dt
    res = []
    while dt_iter.month >= start_dt.month or addition:
        filename = 'data/' + stock + '/' + 'price-' + str(dt_iter.year) + \
            '-' + ('%02d') % (dt_iter.month) + '.txt'
        if not os.path.exists('data/' + stock):
            os.mkdir('data/' + stock)
        if need_update_price(dt_iter, filename):
            fetch_price_from_url(stock, dt_iter, filename)

        price_f = open(filename, 'r')
        next(price_f, None) # to skip header
        csvf = csv.DictReader(price_f, delimiter=',')
        for row in reversed(list(csvf)):
            [year, month, day] = row['日期'].split('/')
            csv_dt = datetime(int(year) + 1911, int(month), int(day)).date()
            if csv_dt > end_dt:
                continue
            elif csv_dt < start_dt:
                if not res: # if specified date gets no data, keep at least one
                    addition += 1
                if not addition:
                    return res
                addition -= 1

            if '--' in row.values(): # skip invalid data
                continue
            elif field:
                res.insert(0, row[field]) # FIXME: return date info as well
            else:
                res.insert(0, row)

        price_f.close()
        dt_iter -= relativedelta.relativedelta(months=1)

    return res


def fetch_price_test(input_params, expect, field=None):
    """
    test module for fetch_data('stock price')
    """
    stock, idate, addition, category = input_params
    res = fetch_data(stock, idate, addition, category, field)
    if res == expect:
        print('pass')
    else:
        print('fail, res: ', res, 'expect: ', expect)




def fetch_price_tests():
    """
    unit test cases for fetch_data('stock price')
    """
    print('fetch_price_tests:')

#fetch_price_test(['1469', '2015/11/1-2015/11/13', 0, 'stock price'],
#[], '收盤價')

    # both period date & addtion step across month
    expect = ['196.50', '194.50', '190.50', '193.50', '194.00', '195.50', \
              '197.50', '195.00', '197.00', '202.50', '200.00', '190.50', \
              '186.50', '186.50', '184.50', '187.00', '183.50', '181.50', \
              '182.00', '183.50', '180.50', '182.50', '180.00', '177.00', \
              '174.00', '178.50', '179.50', '187.50']
    fetch_price_test(['9914', '2015/10/1-2015/11/3', 5, 'stock price'],
                     expect[::-1], '收盤價')

    # single date
    expect = ['180.00']
    fetch_price_test(['9914', '2015/10/1', 0, 'stock price'],
                     expect[::-1], '收盤價')

    # single date, addition steps across month
    expect = ['180.00', '177.00', '174.00']
    fetch_price_test(['9914', '2015/10/1', 2, 'stock price'],
                     expect[::-1], '收盤價')

    # period date, addition steps across month
    expect = ['180.50', '182.50', '180.00', '177.00', '174.00']
    fetch_price_test(['9914', '2015/10/1-2015/10/5', 2, 'stock price'],
                     expect[::-1], '收盤價')

    # period date, addition steps across month, full data
    ex = [{'最低價': '180.00', '成交股數': '409,897', \
          '成交筆數': '386', '漲跌價差': '-2.00', \
          '成交金額': '74,278,754', '日期': ' 104/10/05', \
          '收盤價': '180.50', '開盤價': '184.00', '最高價': '184.00'}, \
         {'最低價': '178.00', '成交股數': '962,273', \
          '成交筆數': '630', '漲跌價差': '+2.50', \
          '成交金額': '174,530,819', '日期': ' 104/10/02', \
          '收盤價': '182.50', '開盤價': '179.50', '最高價': '183.00'}, \
         {'最低價': '176.50', '成交股數': '1,217,096', \
          '成交筆數': '1,075', '漲跌價差': '+3.00', \
          '成交金額': '219,720,184', '日期': ' 104/10/01', \
          '收盤價': '180.00', '開盤價': '177.00', '最高價': '183.00'}, \
         {'最低價': '171.50', '成交股數': '2,593,029', \
          '成交筆數': '1,601', '漲跌價差': '+3.00', \
          '成交金額': '455,027,604', '日期': ' 104/09/30', \
          '收盤價': '177.00', '開盤價': '172.00', '最高價': '177.50'}, \
         {'最低價': '174.00', '成交股數': '805,838', \
          '成交筆數': '683', '漲跌價差': '-4.50', \
          '成交金額': '142,120,650', '日期': ' 104/09/25', \
          '收盤價': '174.00', '開盤價': '181.00', '最高價': '181.00'}]
    fetch_price_test(['9914', '2015/10/1-2015/10/5', 2, 'stock price'],
                     ex[::-1])

    # period date steps across month, addition
    expect = ['180.50', '182.50', '180.00', '177.00', '174.00', '178.50', \
               '179.50', '187.50']
    fetch_price_test(['9914', '2015/9/25-2015/10/5', 3, 'stock price'],
                     expect[::-1], '收盤價')

    # period date steps across month, addition, full data
    ex = [{'成交筆數': '386', '日期': ' 104/10/05', '成交股數': '409,897', \
           '最高價': '184.00', '成交金額': '74,278,754', '漲跌價差': '-2.00', \
           '開盤價': '184.00', '收盤價': '180.50', '最低價': '180.00'}, \
          {'成交筆數': '630', '日期': ' 104/10/02', '成交股數': '962,273', \
           '最高價': '183.00', '成交金額': '174,530,819', '漲跌價差': '+2.50', \
           '開盤價': '179.50', '收盤價': '182.50', '最低價': '178.00'}, \
          {'成交筆數': '1,075', '日期': ' 104/10/01', '成交股數': '1,217,096', \
           '最高價': '183.00', '成交金額': '219,720,184', '漲跌價差': '+3.00', \
           '開盤價': '177.00', '收盤價': '180.00', '最低價': '176.50'}, \
          {'成交筆數': '1,601', '日期': ' 104/09/30', '成交股數': '2,593,029', \
           '最高價': '177.50', '成交金額': '455,027,604', '漲跌價差': '+3.00', \
           '開盤價': '172.00', '收盤價': '177.00', '最低價': '171.50'}, \
          {'成交筆數': '683', '日期': ' 104/09/25', '成交股數': '805,838', \
           '最高價': '181.00', '成交金額': '142,120,650', '漲跌價差': '-4.50', \
           '開盤價': '181.00', '收盤價': '174.00', '最低價': '174.00'}, \
          {'成交筆數': '654', '日期': ' 104/09/24', '成交股數': '720,705', \
           '最高價': '183.00', '成交金額': '129,004,285', '漲跌價差': '-1.00', \
           '開盤價': '180.00', '收盤價': '178.50', '最低價': '176.00'}, \
          {'成交筆數': '805', '日期': ' 104/09/23', '成交股數': '895,266', \
           '最高價': '186.00', '成交金額': '162,593,880', '漲跌價差': '-8.00', \
           '開盤價': '186.00', '收盤價': '179.50', '最低價': '179.50'}, \
          {'成交筆數': '675', '日期': ' 104/09/22', '成交股數': '714,183', \
           '最高價': '187.50', '成交金額': '132,046,221', '漲跌價差': '+4.50', \
           '開盤價': '183.00', '收盤價': '187.50', '最低價': '181.00'}]
    fetch_price_test(['9914', '2015/9/25-2015/10/5', 3, 'stock price'],
                     ex[::-1])

    # period date steps across month
    expect = ['180.50', '182.50', '180.00', '177.00', '174.00']
    fetch_price_test(['9914', '2015/9/25-2015/10/5', 0, 'stock price'],
                     expect[::-1], '收盤價')

    # period date steps across month, full data
    ex = [{'最低價': '180.00', '成交股數': '409,897', '成交筆數': '386', \
           '漲跌價差': '-2.00', '成交金額': '74,278,754', '日期': ' 104/10/05', \
           '收盤價': '180.50', '開盤價': '184.00', '最高價': '184.00'}, \
          {'最低價': '178.00', '成交股數': '962,273', '成交筆數': '630', \
           '漲跌價差': '+2.50', '成交金額': '174,530,819', '日期': ' 104/10/02', \
           '收盤價': '182.50', '開盤價': '179.50', '最高價': '183.00'}, \
          {'最低價': '176.50', '成交股數': '1,217,096', '成交筆數': '1,075', \
           '漲跌價差': '+3.00', '成交金額': '219,720,184', '日期': ' 104/10/01', \
           '收盤價': '180.00', '開盤價': '177.00', '最高價': '183.00'}, \
          {'最低價': '171.50', '成交股數': '2,593,029', '成交筆數': '1,601', \
           '漲跌價差': '+3.00', '成交金額': '455,027,604', '日期': ' 104/09/30', \
           '收盤價': '177.00', '開盤價': '172.00', '最高價': '177.50'}, \
          {'最低價': '174.00', '成交股數': '805,838', '成交筆數': '683', \
           '漲跌價差': '-4.50', '成交金額': '142,120,650', '日期': ' 104/09/25', \
           '收盤價': '174.00', '開盤價': '181.00', '最高價': '181.00'}]
    fetch_price_test(['9914', '2015/9/25-2015/10/5', 0, 'stock price'],
                     ex[::-1])

    # period date
    expect = ['180.50', '182.50', '180.00']
    fetch_price_test(['9914', '2015/10/1-2015/10/5', 0, 'stock price'],
                     expect[::-1], '收盤價')

    # period date, full data
    expect = [{'成交金額': '74,278,754', '漲跌價差': '-2.00', '開盤價': '184.00', \
               '成交股數': '409,897', '最低價': '180.00', '收盤價': '180.50', \
               '成交筆數': '386', '最高價': '184.00', '日期': ' 104/10/05'}, \
              {'成交金額': '174,530,819', '漲跌價差': '+2.50', '開盤價': '179.50', \
               '成交股數': '962,273', '最低價': '178.00', '收盤價': '182.50', \
               '成交筆數': '630', '最高價': '183.00', '日期': ' 104/10/02'}, \
              {'成交金額': '219,720,184', '漲跌價差': '+3.00', '開盤價': '177.00', \
               '成交股數': '1,217,096', '最低價': '176.50', '收盤價': '180.00', \
               '成交筆數': '1,075', '最高價': '183.00', '日期': ' 104/10/01'}]
    fetch_price_test(['9914', '2015/10/1-2015/10/5', 0, 'stock price'],
                     expect[::-1])



def fetch_price_from_url(stock, idate, filename):
    """
    fetch stock price of date from url, and save to filename
    """
    print('update price', stock, idate.year, idate.month)
    if stock == 'index':
        url = ('http://www.twse.com.tw' +
               '/ch/trading/exchange/FMTQIK/FMTQIK2.php' +
               '?STK_NO=&myear=%(year)d&mmon=%(month)2d&type=csv') % \
               {'year': idate.year, 'month': idate.month}
    else:
        url = ('http://www.twse.com.tw' +
               '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' +
               '?genpage=genpage/Report%(year)d%(month)02d/' +
               '%(year)d%(month)02d_F3_1_8_%(stock)s.php&type=csv') % \
               {'year': idate.year, 'month': idate.month, 'stock': stock}

    # write file after decoding
    try:
        with request.urlopen(url) as response, \
                open(filename, 'w') as out_file:
            out_file.write(response.read().decode('big5hkscs')) # for '恒', '碁'
    except UnicodeDecodeError as inst:
        print(inst.args)
        print(stock, inst)

def fetch_revenue_from_url(stock, filename):
    print('update revenue', stock)
    url = ('http://ps01.megatime.com.tw/asp/Basic/GetReportJs.asp?m=&table_name=html\Wsale\&StockID=%(stock)s') % {'stock': stock}
    
    # write file after decoding
    with request.urlopen(url) as response, \
            open(filename, 'w') as out_file:
        soup = BeautifulSoup(response.read().decode('big5hkscs'), 'lxml')
        table = soup.find('table', attrs = {'cellpadding':'1', 'width':'85%'})
        if not table: # FIXME: is there better way to solve this?
            return
        rows = []
        for row in table.find_all('tr'):
            rows.append([val.text for val in row.find_all('td')])

        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
            

    
    

import filecmp
def fetch_price_from_url_test(input_param, expect_url, expect_filename):
    """
    test module for fech_price_from_url()
    """

    stock, year, month, filename = input_param

    # output
    if os.path.exists(filename):
        os.remove(filename)
    tmp_dt = datetime(year, month, day=1) # dont't mind, day won't be used
    fetch_price_from_url(stock, tmp_dt, filename)

    # expect
    if os.path.exists(expect_filename):
        os.remove(expect_filename)
    with request.urlopen(expect_url) as response, \
            open(expect_filename, 'w') as expect_file:
        expect_file.write(response.read().decode('big5hkscs'))

    if filecmp.cmp(filename, expect_filename): # same
        print('pass')
    else:
        print('fail')


def fetch_price_from_url_tests():
    """
    unit test cases for fetch_price_from_url()
    """
    print('fetch_price_from_url_tests:')

    # temp test
    if 1:
        url = 'http://www.twse.com.tw' + \
                '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' + \
                '?genpage=genpage/Report201511/201511_F3_1_8_2415.php&type=csv'
        fetch_price_from_url_test(['6203', 2015, 11, '/tmp/2415.output'],
                                  url, '/tmp/2415.expect')

    # trivial test
    url = 'http://www.twse.com.tw' + \
            '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' + \
            '?genpage=genpage/Report201511/201511_F3_1_8_2415.php&type=csv'
    fetch_price_from_url_test(['2415', 2015, 11, '/tmp/2415.output'],
                              url, '/tmp/2415.expect')

    # test for index
    url = 'http://www.twse.com.tw' + \
            '/ch/trading/exchange/FMTQIK/FMTQIK2.php' + \
            '?STK_NO=&myear=2015&mmon=11&type=csv'
    fetch_price_from_url_test(['index', 2015, 11, '/tmp/index.output'],
                              url, '/tmp/index.expect')

    # test for 'T' in '01002T'
    url = 'http://www.twse.com.tw' + \
            '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' + \
            '?genpage=genpage/Report201511/201511_F3_1_8_01002T.php&type=csv'
    fetch_price_from_url_test(['01002T', 2015, 11, '/tmp/01002T.output'],
                              url, '/tmp/01002T.expect')

    # test for six numbers in '911616'
    url = 'http://www.twse.com.tw' + \
            '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' + \
            '?genpage=genpage/Report201511/201511_F3_1_8_911616.php&type=csv'
    fetch_price_from_url_test([911616, 2015, 11, '/tmp/911616.output'],
                              url, '/tmp/911616.expect')

    # test for '恒', '碁' in content
    url = 'http://www.twse.com.tw' + \
            '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' + \
            '?genpage=genpage/Report201511/201511_F3_1_8_910708.php&type=csv'
    fetch_price_from_url_test([910708, 2015, 11, '/tmp/910708.output'],
                              url, '/tmp/910708.expect')

if __name__ == '__main__':
    fetch_price_tests()
    fetch_price_from_url_tests()
