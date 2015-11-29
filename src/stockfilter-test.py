import stockfilter


def process_filters_test(stock, period, filters_params, expect, multi=False):
    """ test module """
    res  = stockfilter.process_filters(stock, period, filters_params, multi=multi)
    if multi and res.values.tolist() == expect: # multi and match case
        print('pass')
    elif multi: # multi and not match case
        print('fail')
        print(res.values.tolist())
        print(expect)
    elif res == expect: # normal and match case
        print('pass')
    else: # normal and not match case
        print('fail')
        print(res)
        print(expect)


def dummy_true_filter(stock, period, params):
    """ dummy filter, always returns true """
    _ = stock
    _ = period
    _ = params
    return True


def dummy_false_filter(stock, period, params):
    """ dummy filter, always returns false """
    _ = stock
    _ = period
    _ = params
    return False


def process_filters_tests():
    """ test cases """    
    print('process_filters_tests:')    

    # trivial tests
    process_filters_test('9914', 'today', [[dummy_true_filter]], '9914')
    process_filters_test('9914', 'today', [[dummy_false_filter]], False)
    process_filters_test('9914', 'today', [[dummy_true_filter], [dummy_false_filter]], False)

    # test multi
    process_filters_test('2454', '2015/11/18', [[stockfilter.new_price_in_n_days_multi, [10, 20, 30], 'low']], [[False, True, False, False, False, False]], multi=True)


def process_stocks_test(stock, period, filters_params, expect, show_msg_box=False, multi=False):
    """ test module """
    res = stockfilter.process_stocks(stock, period, filters_params, 
                                   show_msg_box=show_msg_box, multi=multi)
    if multi:
        if res.values.tolist() == expect:
            print('pass')
        else:
            print('fail')
            print(res.values.tolist())
            print(expect)
    else:
        if res == expect:
            print('pass')
        else:
            print('fail')
            print(res)
            print(expect)
        

def process_stocks_tests():
    """ test cases """
    print('process_stocks_tests:')    
    # trival error tests
    process_stocks_test(None, 'aaa', 'bbb', -1)
    process_stocks_test('aaa', None, 'bbb', -1)
    process_stocks_test('aaa', 'bbb', None, -1)

    # stocks == 'all' test
    with open('data/stock-table.csv') as f:
        lines_num = sum(1 for line in f)
        process_stocks_test('all', 'aaa', [[dummy_true_filter]], lines_num)

    # specified stocks test, 4444 is not real
    process_stocks_test('2454,2330,4444', 'aaa', [[dummy_true_filter]], 2)

    # test for multi
    process_stocks_test('2454', '2015/11/18', [[stockfilter.new_price_in_n_days_multi, [10, 20, 30]]], [[0, 1, 0, 0, 0, 0]], multi=True)

def is_high_test(param, expect):
    """ test module """
    if stockfilter.is_high(param) == expect:
        print('pass')
    else:
        print('fail')


def is_high_tests():
    """ test cases """
    print('is_high_tests:')

    # trivial tests
    is_high_test('high', True) 
    is_high_test('hi', True) 
    is_high_test('h', True) 
    is_high_test('low', False) 
    is_high_test('l', False) 


def new_price_in_n_days_test(stock, period, params, expect):
    """ test module """
    res = stockfilter.new_price_in_n_days(stock, period, params)
    if res == expect:
        print('pass')
    else:
        print('fail')
        print(res)
        print(expect)


def new_price_in_n_days_tests():
    """ test cases """

    # trivial tests
    new_price_in_n_days_test('9914', '2015/9/30', ['5', 'high'], False)
    new_price_in_n_days_test('9914', '2015/9/25', ['5', 'high'], False)
    new_price_in_n_days_test('9914', '2015/9/10', ['5', 'high'], True)
    new_price_in_n_days_test('9914', '2015/9/25', ['5', 'low'], True)

    # test for closed date
    new_price_in_n_days_test('9914', '2015/9/26', ['5', 'high'], False)
    new_price_in_n_days_test('9914', '2015/9/26', ['5', 'low'], True)

    # test for data with '--', can't convert to float
    new_price_in_n_days_test('1225', '2015/11/16', ['5', 'low'], True)

    # test for data with comma, e.g '2,505.00'
    new_price_in_n_days_test('3008', '2015/11/16', ['5', 'low'], False)
    
    # test for otc
    new_price_in_n_days_test('1256', '2015/11/16', ['5', 'low'], True)

def new_revenue_in_n_months_test(stock, period, params, expect):
    """ test module """
    if stockfilter.new_revenue_in_n_months(stock, period, params) == expect:
        print('pass')
    else:
        print('fail')


def new_revenue_in_n_months_tests():
    """ test cases """
    print('new_revenue_in_n_months_tests:')

    # trivial tests
    new_revenue_in_n_months_test('9914', '2015/10/1', ['5', 'low'], True)
    new_revenue_in_n_months_test('9914', '2015/10/2', ['6', 'low'], False)
    new_revenue_in_n_months_test('9914', '2014/7/3', ['7', 'high'], True)
    new_revenue_in_n_months_test('9914', '2014/7/4', ['8', 'high'], True)
    new_revenue_in_n_months_test('2454', '2015/10/4', ['5', 'high'], True)

    # test for empty file
    new_revenue_in_n_months_test('0056', '2015/11/4', ['12', 'high'], False)


def new_price_in_n_days_multi_test(stock, period, params, expect):
    res = stockfilter.new_price_in_n_days_multi(stock, period, params)
    if res.values.tolist() == expect:
        print('pass')
    else:
        print('fail')
        print(res.values.tolist())
        print(expect)


def new_price_in_n_days_multi_tests():
    print('new_price_in_n_days_multi_tests:')
    #new_price_in_n_days_multi_test('2454', '2015/11/18', [[10, 20, 30], 'low'], [False, True, False, False, False, False])
    new_price_in_n_days_multi_test('2545', '2015/11/5-2015/11/6', 
                                   [[5, 10, 20], 'low'], [[True, False, True, False, False, False],[True, False, True, False, False, False]])


if __name__ == '__main__':
    process_filters_tests()
    process_stocks_tests()
    is_high_tests()
    new_price_in_n_days_tests()
    new_revenue_in_n_months_tests()
    new_price_in_n_days_multi_tests()


