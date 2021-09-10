import os
import pandas as pd
import numpy as np
import argparse
import datetime
import copy

from backtest_framework import trade_process



parser = argparse.ArgumentParser(description='Backtest.')

parser.add_argument('--start_date', default='', type=str,
                        help='start_date: %Y/%m/%d')
parser.add_argument('--end_date', default='', type=str,
                        help='end_date: %Y/%m/%d')
parser.add_argument('--input_file_path', default="BTCUSDT_Binance_futures_data_minute.csv", type=str,
                        help="file path of crypto data")
parser.add_argument('--output_file_name', default="log_for_draw.csv", type=str,
                        help='output_file_name')
parser.add_argument('--init_cash', default=100000, type=int,
                        help='cash we have at the start')
parser.add_argument('--lever_rate', default=1, type=int,
                        help='lever_rate')
parser.add_argument('--max_allowable_dropdown_percentage', default=0.05, type=float,
                        help='max_allowable_dropdown_percentage')
parser.add_argument('--th_ub', default=0.1, type=float,
                        help='upper boundary of threshold')
parser.add_argument('--cycle', default=12, type=int,
                        help='cycle of schedule (in hour)')
parser.add_argument('--train_look_back_period', default=24*5, type=int,
                        help='lookback period for optimal threshold training (in hour)')
parser.add_argument('--test_look_back_period', default=12, type=int,
                        help='lookback period for optimal threshold testing (in hour)')
parser.add_argument('--calm_down_period', default=15, type=int,
                        help='calm down period (in minute)')
parser.add_argument('--train_look_back_period_calmdown', default=24, type=int,
                        help='lookback period for optimal threshold training after calm down (in hour)')
parser.add_argument('--test_look_back_period_calmdown', default=6, type=int,
                        help='lookback period for optimal threshold testing after calm down (in hour)')
args = parser.parse_args()



# load btc min data csv file
BTC_min_data = pd.read_csv(args.input_file_path)
BTC_min_data = BTC_min_data.dropna()
BTC_min_data = BTC_min_data[::-1]
BTC_min_data = BTC_min_data.reset_index()
BTC_min_data = BTC_min_data.drop(columns=["index"])
min_time_list = []
for i in range(0,len(BTC_min_data["date"])):
    print("preprocessing crypto data: "+str(int(i/len(BTC_min_data["date"])*100))+"%", end="\r")
    min_time_list.append(datetime.datetime.strptime(BTC_min_data["date"][i], "%Y/%m/%d %H:%M"))
min_time_list = np.array(min_time_list)
BTC_min_data.loc[:,"time"] = min_time_list
print(BTC_min_data)



# init backtest obj
Backtest = trade_process(init_cash = args.init_cash,
                         lever_rate = args.lever_rate,
                         max_allowable_dropdown_percentage = args.max_allowable_dropdown_percentage,
                         upper_bound_of_threshold = args.th_ub,
                         cycle_of_schedule_hours = args.cycle,
                         train_look_back_period_hours = args.train_look_back_period,
                         test_look_back_period_hours = args.test_look_back_period,
                         calm_down_period_minutes = args.calm_down_period,
                         train_look_back_period_hours_calmdown = args.train_look_back_period_calmdown,
                         test_look_back_period_hours_calmdown = args.test_look_back_period_calmdown)

# set crypto data for the backtest obj
start_date = datetime.datetime.strptime(args.start_date, "%Y/%m/%d")
end_date = datetime.datetime.strptime(args.end_date, "%Y/%m/%d")
period_locs = np.where(np.logical_and(BTC_min_data.loc[:,"time"] >= start_date,
                                              BTC_min_data.loc[:,"time"] <= end_date))[0]
start_loc = period_locs[0]+BTC_min_data.index[0]
end_loc = period_locs[-1]+BTC_min_data.index[0]
Backtest.set_crypto_data(copy.deepcopy(BTC_min_data.loc[start_loc:end_loc, :]))

# run backtest
Backtest.backtest(Backtest.crypto_syms[0])

# print the logs
print(Backtest.trading_data.log) # log of actions
print(Backtest.log_for_draw["BTC"]) # log for draw

# save backtest results
Backtest.log_for_draw["BTC"].to_csv(args.output_file_name, index=False)
