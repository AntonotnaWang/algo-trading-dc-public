# algo-trading-dc-public
Algo trading using Directional Change.

Set the crypto data csv file following the format shown in ```BTCUSDT_Binance_futures_data_minute.csv```.

Run backtest with ```run_backtest.py```.

E.g. backtest from 2020-12-1 to 2021-2-1 with lever rate 1, look back period for training 120 hours, and training cycle 6 hours. (See ```run_backtest.py``` for more options.)
```
python run_backtest.py --start_date 2020/12/1 --end_date 2021/2/1 --input_file_path "BTCUSDT_Binance_futures_data_minute.csv"  --output_file_name "log.csv" --lever_rate 1 --cycle 6 --train_look_back_period 120
```
