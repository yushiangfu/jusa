import stockfilter
import fetch

def plot_new_price_in_n_days(index_period, stocks_period, filename):

    if 1:
        df = stockfilter.process_stocks('all', index_period, [[stockfilter.new_price_in_n_days_multi, stocks_period]], show_msg_box=False, multi=True)
    else:
        res = [336, 111, 190, 214, 261, 242, 213, 219, 175, 75, 81, 128, 166, 216, 208, 175, 198, 184, 125, 124]
    df.to_csv(filename)

if __name__ == '__main__':
    #plot_new_price_in_n_days('2015/1/1-2015/11/27', 240, 'high', ' 240日新高', '240high.csv')
    #plot_new_price_in_n_days('2015/1/1-2015/11/27', 120, 'high', ' 120日新高', '120high.csv')
    #plot_new_price_in_n_days('2015/1/1-2015/11/27', 60, 'high', ' 60日新高', '60high.csv')
    #plot_new_price_in_n_days('2015/1/1-2015/11/27', 20, 'high', ' 20日新高', '20high.csv')
    plot_new_price_in_n_days('2015/1/5-2015/11/27', [20, 60, 120, 240], 'total.csv')
