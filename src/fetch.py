import urllib.request
def fetch_stock(stock, year, month, filename):
    if stock == 'index':
        url = ('http://www.twse.com.tw' +
                '/ch/trading/exchange/FMTQIK/FMTQIK2.php' +
                '?STK_NO=&myear=%(year)d&mmon=%(month)2d&type=csv') % {
                'year': year,
                'month': month}
    else:
        url = ('http://www.twse.com.tw' +
                '/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php' +
                '?genpage=genpage/Report%(year)d%(month)2d/' + 
                '%(year)d%(month)2d_F3_1_8_%(stock)s.php&type=csv') % {
                'year': year,
                'month': month,
                'stock': stock}

    # write file after decoding
    with urllib.request.urlopen(url) as response, open(filename, 'w') as out_file:
        out_file.write(response.read().decode('big5hkscs')) # for '恒', '碁'
        

import os
import filecmp
def test(stock, year, month, filename, expect_url, expect_filename):

    # output
    if os.path.exists(filename):
        os.remove(filename)
    fetch_stock(stock, year, month, filename)

    # expect
    if os.path.exists(expect_filename):
        os.remove(expect_filename)
    with urllib.request.urlopen(expect_url) as response, open(expect_filename, 'w') as expect_file:
        expect_file.write(response.read().decode('big5hkscs')) 

    if filecmp.cmp(filename, expect_filename): # same
        print('pass')
    else:
        print('fail')


def tests():
    # trivial test
    test('2415', 2015, 11, '/tmp/2415.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_2415.php&type=csv',
        '/tmp/2415.expect')

    # test for index
    test('index', 2015, 11, '/tmp/index.output', 
        'http://www.twse.com.tw/ch/trading/exchange/FMTQIK/FMTQIK2.php?STK_NO=&myear=2015&mmon=11&type=csv',
        '/tmp/index.expect')

    # test for 'T' in '01002T'
    test('01002T', 2015, 11, '/tmp/01002T.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_01002T.php&type=csv',
        '/tmp/01002T.expect')

    # test for six numbers in '911616'
    test(911616, 2015, 11, '/tmp/911616.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_911616.php&type=csv',
        '/tmp/911616.expect')

    # test for '恒', '碁' in content
    test(910708, 2015, 11, '/tmp/910708.output', 
        'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/Report201511/201511_F3_1_8_910708.php&type=csv',
        '/tmp/910708.expect')
    
if __name__ == '__main__':
    tests()
