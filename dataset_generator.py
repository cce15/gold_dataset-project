from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import talib as ta


# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the raw_datasets directory
raw_datasets_dir = os.path.join(current_dir, 'raw_datasets')
full_generated_datasets= os.path.join(os.getcwd(),"full_datasets")
training_generated_datasets= os.path.join(os.getcwd(),"training_datasets")


if not os.path.exists(full_generated_datasets):
    os.makedirs(full_generated_datasets)
if not os.path.exists(training_generated_datasets):
    os.makedirs(training_generated_datasets)

def check_fill_missing_dayes(dataset):
    ## Checking missing day
    #Initial process to find any  missing days like weekends and others.

    # Generate a complete date range for the period
    start_date = dataset.index.min()
    today = datetime.today()
    end_date = pd.to_datetime(today)

    full_date_range = pd.date_range(start=start_date, end=end_date)

    # Identify missing dates
    missing_dates = full_date_range.difference(dataset.index)

    print(f'Starting Date: {start_date}')
    print(f'Ending Date: {end_date}')

    if missing_dates.empty:
        print('No missing days')
    else:
        print(f'Missing days: {len(missing_dates)} days \n')
        print(missing_dates)

    # Fill the gap of missing days

    # Resample the dataset to have an entry for each day
    df_daily = dataset.resample('D').asfreq()

    # Forward fill the missing data
    dataset = df_daily.fillna(method='ffill')

    return dataset

def traning_dataset(dataset):
    #Pricing targets
    periods = [1, 3, 7, 30, 60]  # next 1 day , next 3 days, next 7 days and next 30 days
    for i in periods:
        dataset[f'target_next_{i}_day_price'] = dataset['close'].shift(-i)
    #Direction dataset
    for i in periods:
        # Determine if the next day's closing price is up or down compared to the current day
        dataset[f'taget_next_{i}_day_direction'] = dataset.apply(
            lambda row: 2 if row[f'target_next_{i}_day_price'] > row['close'] else (
                1 if row[f'target_next_{i}_day_price'] < row['close'] else 0), axis=1)
    # Price Change targets
    for i in periods:
        # Calculate the percentage price change.
        dataset[f'target_next_{i}_day_Price_Change'] = (
                    (dataset['close'].shift(-i) - dataset['close']) / dataset['close'])
    # Drop the last 60 rows
    dataset = dataset[:-62]
    output_file_name = str(datetime.today().date()).replace("-", "_") + ".csv"
    # 6 months sample dataset for website display
    cutoff_date = datetime.now() - pd.DateOffset(months=6)
    sample=dataset[dataset.index >= cutoff_date]
    sample.to_csv(os.path.join(training_generated_datasets, "sample_"+output_file_name))
    dataset.to_csv(os.path.join(training_generated_datasets, output_file_name))

def full_dataset():
    today = datetime.today()
    # Daily OHLC Gold historical prices

    primary_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'TVC_GOLD, 1D.csv'))


    # ========== Economy historical data ===========
    # US Dollar Index
    dxy_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'ICEUS_DLY_DXY, 1D.csv'))
    # Effective Federal Funds Rate
    fred__fedfunds_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'FRED_FEDFUNDS, 1D.csv'))
    # United States Interest Rate
    usintr_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'ECONOMICS_USINTR, 1D.csv'))
    # United States Inflation Rate
    usiryy_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'ECONOMICS_USIRYY, 1D.csv'))
    # United States Consumer Confidence Index
    uscons_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'ECONOMICS_USCCI, 1D.csv'))
    # United States Unemployment Rate
    usunemp_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'ECONOMICS_USUR, 1D.csv'))
    # ======== Stock Market Performance ============
    # NASDAQ
    nasdaq_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'NASDAQ_DLY_NDX, 1D.csv'))
    # NYA_dataset
    nya_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'TVC_NYA, 1D.csv'))
    # S&P500
    sp500_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'SP_SPX, 1D.csv'))
    # ====== Oil Price =======
    # Light Crude Oil Futuires
    light_crude_oil_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'NYMEX_DL_CL1!, 1D.csv'))
    # ====== Crypto Market =======
    # Bitcoin price
    btc_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'INDEX_BTCUSD, 1D.csv'))
    # Crypto marketcap
    total_crypto_cap_dataset = pd.read_csv(os.path.join(raw_datasets_dir, 'CRYPTOCAP_TOTAL, 1D.csv'))


    # Convert the time data from unix timestamp to a DateTime opject and make it as the index of the dataset
    primary_dataset['time'] = pd.to_datetime(primary_dataset['time'], unit='s').dt.date
    # Increment the DateTime column by one day to fix the synchronization issue.
    primary_dataset['time'] += pd.Timedelta(days=1)
    primary_dataset.set_index('time', inplace=True)
    # Ensure the index is a DatetimeIndex
    primary_dataset.index = pd.DatetimeIndex(primary_dataset.index)

    print(primary_dataset)

    # Checking and filling missing day
    primary_dataset=check_fill_missing_dayes(primary_dataset)

    is_weekend = today.weekday() >= 5  # 5 is Saturday, 6 is Sunday

    if is_weekend:
        print("is weekend")
        # Get the previous day's data
        # Duplicate the last row and update the index to today's date
        last_row = primary_dataset.iloc[-1].copy()
        primary_dataset.loc[datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)] = last_row

    # Checking and filling missing day
    primary_dataset=check_fill_missing_dayes(primary_dataset)

    print(primary_dataset.tail(10))
    # Convert the time data from unix timestamp to a DateTime opject for all subdatasets
    dxy_dataset['time'] = pd.to_datetime(dxy_dataset['time'], unit='s').dt.date
    dxy_dataset.set_index('time', inplace=True)
    dxy_dataset.index = pd.DatetimeIndex(dxy_dataset.index)
    print("DXY")
    print(dxy_dataset)

    fred__fedfunds_dataset['time'] = pd.to_datetime(fred__fedfunds_dataset['time'], unit='s').dt.date
    fred__fedfunds_dataset.set_index('time', inplace=True)
    fred__fedfunds_dataset.index = pd.DatetimeIndex(fred__fedfunds_dataset.index)
    print("fred__fedfunds")
    print(fred__fedfunds_dataset)

    usintr_dataset['time'] = pd.to_datetime(usintr_dataset['time'], unit='s').dt.date
    usintr_dataset.set_index('time', inplace=True)
    usintr_dataset.index = pd.DatetimeIndex(usintr_dataset.index)
    print("usintr_dataset")
    print(usintr_dataset)

    usiryy_dataset['time'] = pd.to_datetime(usiryy_dataset['time'], unit='s').dt.date
    usiryy_dataset.set_index('time', inplace=True)
    usiryy_dataset.index = pd.DatetimeIndex(usiryy_dataset.index)
    print("usiryy_dataset")
    print(usiryy_dataset)

    uscons_dataset['time'] = pd.to_datetime(uscons_dataset['time'], unit='s').dt.date
    uscons_dataset.set_index('time', inplace=True)
    uscons_dataset.index = pd.DatetimeIndex(uscons_dataset.index)
    print("uscons_dataset")
    print(uscons_dataset)

    usunemp_dataset['time'] = pd.to_datetime(usunemp_dataset['time'], unit='s').dt.date
    usunemp_dataset.set_index('time', inplace=True)
    usunemp_dataset.index = pd.DatetimeIndex(usunemp_dataset.index)
    print("usunemp_dataset")
    print(usunemp_dataset)


    nasdaq_dataset['time'] = pd.to_datetime(nasdaq_dataset['time'], unit='s').dt.date
    nasdaq_dataset.set_index('time', inplace=True)
    nasdaq_dataset.index = pd.DatetimeIndex(nasdaq_dataset.index)
    print("nasdaq_dataset")
    print(nasdaq_dataset)

    nya_dataset['time'] = pd.to_datetime(nya_dataset['time'], unit='s').dt.date
    nya_dataset.set_index('time', inplace=True)
    nya_dataset.index = pd.DatetimeIndex(nya_dataset.index)
    print("nya_dataset")
    print(nya_dataset)

    sp500_dataset['time'] = pd.to_datetime(sp500_dataset['time'], unit='s').dt.date
    sp500_dataset.set_index('time', inplace=True)
    sp500_dataset.index = pd.DatetimeIndex(sp500_dataset.index)
    print("sp500_dataset")
    print(sp500_dataset)

    light_crude_oil_dataset['time'] = pd.to_datetime(light_crude_oil_dataset['time'], unit='s').dt.date
    light_crude_oil_dataset.set_index('time', inplace=True)
    light_crude_oil_dataset.index = pd.DatetimeIndex(light_crude_oil_dataset.index)
    print("light_crude_oil_dataset")
    print(light_crude_oil_dataset)

    btc_dataset['time'] = pd.to_datetime(btc_dataset['time'], unit='s').dt.date
    btc_dataset.set_index('time', inplace=True)
    btc_dataset.index = pd.DatetimeIndex(btc_dataset.index)
    print("btc_dataset")
    print(btc_dataset)

    total_crypto_cap_dataset['time'] = pd.to_datetime(total_crypto_cap_dataset['time'], unit='s').dt.date
    total_crypto_cap_dataset.set_index('time', inplace=True)
    total_crypto_cap_dataset.index = pd.DatetimeIndex(total_crypto_cap_dataset.index)
    print("total_crypto_cap_dataset")
    print(total_crypto_cap_dataset)

    # It is better to rename the columns of the sub-datasets before merging to avoid any conflicts in the column names among all the datasets
    dxy_dataset = dxy_dataset.rename(
        columns={'open': 'dxy_open', 'close': 'dxy_close', 'high': 'dxy_high', 'low': 'dxy_low'})
    fred_fedfunds_dataset = fred__fedfunds_dataset.rename(columns={'close': 'fred_fedfunds_close'})
    usintr_dataset = usintr_dataset.rename(columns={'close': 'usintr_close'})
    usiryy_dataset = usiryy_dataset.rename(columns={'close': 'usiryy_close'})
    uscons_dataset = uscons_dataset.rename(columns={'close': 'uscons_close'})
    usunemp_dataset = usunemp_dataset.rename(columns={'close': 'usunemp_close'})
    nasdaq_dataset = nasdaq_dataset.rename(
        columns={'open': 'nasdaq_open', 'close': 'nasdaq_close', 'high': 'nasdaq_high', 'low': 'nasdaq_low'})
    nya_dataset = nya_dataset.rename(
        columns={'open': 'nya_open', 'close': 'nya_close', 'high': 'nya_high', 'low': 'nya_low'})
    sp500_dataset = sp500_dataset.rename(
        columns={'open': 'sp500_open', 'close': 'sp500_close', 'high': 'sp500_high', 'low': 'sp500_low'})
    light_crude_oil_dataset = light_crude_oil_dataset.rename(
        columns={'open': 'light_crude_oil_open', 'close': 'light_crude_oil_close', 'high': 'light_crude_oil_high',
                 'low': 'light_crude_oil_low'})
    btc_dataset = btc_dataset.rename(
        columns={'open': 'btc_open', 'close': 'btc_close', 'high': 'btc_high', 'low': 'btc_low'})
    total_crypto_cap_dataset = total_crypto_cap_dataset.rename(
        columns={'open': 'total_crypto_cap_open', 'close': 'total_crypto_cap_close', 'high': 'total_crypto_cap_high',
                 'low': 'total_crypto_cap_low'})

    # Merging the sub-datasets to the primary dataset.
    primary_dataset = pd.merge(primary_dataset, dxy_dataset[['dxy_open', 'dxy_close', 'dxy_high', 'dxy_low']],
                               on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, fred_fedfunds_dataset[['fred_fedfunds_close']], on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, usintr_dataset[['usintr_close']], on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, usiryy_dataset[['usiryy_close']], on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, uscons_dataset[['uscons_close']], on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, usunemp_dataset[['usunemp_close']], on='time', how='left')
    primary_dataset = pd.merge(primary_dataset,
                               nasdaq_dataset[['nasdaq_open', 'nasdaq_close', 'nasdaq_high', 'nasdaq_low']], on='time',
                               how='left')
    primary_dataset = pd.merge(primary_dataset, nya_dataset[['nya_open', 'nya_close', 'nya_high', 'nya_low']],
                               on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, sp500_dataset[['sp500_open', 'sp500_close', 'sp500_high', 'sp500_low']],
                               on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, light_crude_oil_dataset[
        ['light_crude_oil_open', 'light_crude_oil_close', 'light_crude_oil_high', 'light_crude_oil_low']], on='time',
                               how='left')
    primary_dataset = pd.merge(primary_dataset, btc_dataset[['btc_open', 'btc_close', 'btc_high', 'btc_low']],
                               on='time', how='left')
    primary_dataset = pd.merge(primary_dataset, total_crypto_cap_dataset[
        ['total_crypto_cap_open', 'total_crypto_cap_close', 'total_crypto_cap_high', 'total_crypto_cap_low']],
                               on='time', how='left')

    print(primary_dataset.info())
    print('Total Number of Duplicates:', len(primary_dataset[primary_dataset.duplicated(keep=False)]))
    primary_dataset[primary_dataset.duplicated(keep=False)]
    # Check for missing values
    print("Missing values per column:")
    print(primary_dataset.isna().sum())
    print(primary_dataset.info())
    primary_dataset = primary_dataset.fillna(method='ffill')
    # Check for missing values
    print("Missing values per column:")
    print(primary_dataset.isna().sum())
    start_date = pd.to_datetime(
        '1995-01-01')  # I keep more data at the beginning for the long averages to be calculated for the required starting point.

    end_date = pd.to_datetime(today)

    primary_dataset = primary_dataset.loc[start_date:end_date]
    print(primary_dataset)
    # Check for missing values
    print("Missing values per column:")
    print(primary_dataset.isna().sum())
    # Replace all NaN values with 0
    primary_dataset.fillna(0, inplace=True)
    # Check for missing values
    print("Missing values per column:")
    print(primary_dataset.isna().sum())
    print(primary_dataset.tail(10))

    # Technical indicators
    # ===================================== Gold =========================================

    # Common technical indicators
    primary_dataset['gold_RSI']= ta.RSI(primary_dataset['close'], timeperiod=14)
    primary_dataset['gold_MACD']= ta.MACD(primary_dataset['close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['gold_MACD_signal']= ta.MACD(primary_dataset['close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['gold_MACD_hist']= ta.MACD(primary_dataset['close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['gold_ADX']= ta.ADX(primary_dataset['high'], primary_dataset['low'], primary_dataset['close'], timeperiod=14)
    primary_dataset['gold_CCI']= ta.CCI(primary_dataset['high'], primary_dataset['low'], primary_dataset['close'], timeperiod=14)
    primary_dataset['gold_ROC']= ta.ROC(primary_dataset['close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['gold_SMA_10']= ta.SMA(primary_dataset['close'], timeperiod=10)
    primary_dataset['gold_SMA_20']= ta.SMA(primary_dataset['close'], timeperiod=20)
    primary_dataset['gold_EMA_10']= ta.EMA(primary_dataset['close'], timeperiod=10)
    primary_dataset['gold_EMA_20']= ta.EMA(primary_dataset['close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['gold_SMA_50']= ta.SMA(primary_dataset['close'], timeperiod=50)
    primary_dataset['gold_EMA_50']= ta.EMA(primary_dataset['close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['gold_SMA_100']= ta.SMA(primary_dataset['close'], timeperiod=100)
    primary_dataset['gold_SMA_200']= ta.SMA(primary_dataset['close'], timeperiod=200)
    primary_dataset['gold_EMA_100']= ta.EMA(primary_dataset['close'], timeperiod=100)
    primary_dataset['gold_EMA_200']= ta.EMA(primary_dataset['close'], timeperiod=200)


    # ===================================== DXY =========================================

    # Common technical indicators
    primary_dataset['dxy_RSI']= ta.RSI(primary_dataset['dxy_close'], timeperiod=14)
    primary_dataset['dxy_MACD']= ta.MACD(primary_dataset['dxy_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['dxy_MACD_signal']= ta.MACD(primary_dataset['dxy_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['dxy_MACD_hist']= ta.MACD(primary_dataset['dxy_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['dxy_ADX']= ta.ADX(primary_dataset['dxy_high'], primary_dataset['dxy_low'], primary_dataset['dxy_close'], timeperiod=14)
    primary_dataset['dxy_CCI']= ta.CCI(primary_dataset['dxy_high'], primary_dataset['dxy_low'], primary_dataset['dxy_close'], timeperiod=14)
    primary_dataset['dxy_ROC']= ta.ROC(primary_dataset['dxy_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['dxy_SMA_10']= ta.SMA(primary_dataset['dxy_close'], timeperiod=10)
    primary_dataset['dxy_SMA_20']= ta.SMA(primary_dataset['dxy_close'], timeperiod=20)
    primary_dataset['dxy_EMA_10']= ta.EMA(primary_dataset['dxy_close'], timeperiod=10)
    primary_dataset['dxy_EMA_20']= ta.EMA(primary_dataset['dxy_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['dxy_SMA_50']= ta.SMA(primary_dataset['dxy_close'], timeperiod=50)
    primary_dataset['dxy_EMA_50']= ta.EMA(primary_dataset['dxy_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['dxy_SMA_100']= ta.SMA(primary_dataset['dxy_close'], timeperiod=100)
    primary_dataset['dxy_SMA_200']= ta.SMA(primary_dataset['dxy_close'], timeperiod=200)
    primary_dataset['dxy_EMA_100']= ta.EMA(primary_dataset['dxy_close'], timeperiod=100)
    primary_dataset['dxy_EMA_200']= ta.EMA(primary_dataset['dxy_close'], timeperiod=200)



    # ===================================== nasdaq =========================================

    # Common technical indicators
    primary_dataset['nasdaq_RSI']= ta.RSI(primary_dataset['nasdaq_close'], timeperiod=14)
    primary_dataset['nasdaq_MACD']= ta.MACD(primary_dataset['nasdaq_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['nasdaq_MACD_signal']= ta.MACD(primary_dataset['nasdaq_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['nasdaq_MACD_hist']= ta.MACD(primary_dataset['nasdaq_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['nasdaq_ADX']= ta.ADX(primary_dataset['nasdaq_high'], primary_dataset['nasdaq_low'], primary_dataset['nasdaq_close'], timeperiod=14)
    primary_dataset['nasdaq_CCI']= ta.CCI(primary_dataset['nasdaq_high'], primary_dataset['nasdaq_low'], primary_dataset['nasdaq_close'], timeperiod=14)
    primary_dataset['nasdaq_ROC']= ta.ROC(primary_dataset['nasdaq_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['nasdaq_SMA_10']= ta.SMA(primary_dataset['nasdaq_close'], timeperiod=10)
    primary_dataset['nasdaq_SMA_20']= ta.SMA(primary_dataset['nasdaq_close'], timeperiod=20)
    primary_dataset['nasdaq_EMA_10']= ta.EMA(primary_dataset['nasdaq_close'], timeperiod=10)
    primary_dataset['nasdaq_EMA_20']= ta.EMA(primary_dataset['nasdaq_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['nasdaq_SMA_50']= ta.SMA(primary_dataset['nasdaq_close'], timeperiod=50)
    primary_dataset['nasdaq_EMA_50']= ta.EMA(primary_dataset['nasdaq_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['nasdaq_SMA_100']= ta.SMA(primary_dataset['nasdaq_close'], timeperiod=100)
    primary_dataset['nasdaq_SMA_200']= ta.SMA(primary_dataset['nasdaq_close'], timeperiod=200)
    primary_dataset['nasdaq_EMA_100']= ta.EMA(primary_dataset['nasdaq_close'], timeperiod=100)
    primary_dataset['nasdaq_EMA_200']= ta.EMA(primary_dataset['nasdaq_close'], timeperiod=200)



    # ===================================== nya =========================================

    # Common technical indicators
    primary_dataset['nya_RSI']= ta.RSI(primary_dataset['nya_close'], timeperiod=14)
    primary_dataset['nya_MACD']= ta.MACD(primary_dataset['nya_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['nya_MACD_signal']= ta.MACD(primary_dataset['nya_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['nya_MACD_hist']= ta.MACD(primary_dataset['nya_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['nya_ADX']= ta.ADX(primary_dataset['nya_high'], primary_dataset['nya_low'], primary_dataset['nya_close'], timeperiod=14)
    primary_dataset['nya_CCI']= ta.CCI(primary_dataset['nya_high'], primary_dataset['nya_low'], primary_dataset['nya_close'], timeperiod=14)
    primary_dataset['nya_ROC']= ta.ROC(primary_dataset['nya_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['nya_SMA_10']= ta.SMA(primary_dataset['nya_close'], timeperiod=10)
    primary_dataset['nya_SMA_20']= ta.SMA(primary_dataset['nya_close'], timeperiod=20)
    primary_dataset['nya_EMA_10']= ta.EMA(primary_dataset['nya_close'], timeperiod=10)
    primary_dataset['nya_EMA_20']= ta.EMA(primary_dataset['nya_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['nya_SMA_50']= ta.SMA(primary_dataset['nya_close'], timeperiod=50)
    primary_dataset['nya_EMA_50']= ta.EMA(primary_dataset['nya_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['nya_SMA_100']= ta.SMA(primary_dataset['nya_close'], timeperiod=100)
    primary_dataset['nya_SMA_200']= ta.SMA(primary_dataset['nya_close'], timeperiod=200)
    primary_dataset['nya_EMA_100']= ta.EMA(primary_dataset['nya_close'], timeperiod=100)
    primary_dataset['nya_EMA_200']= ta.EMA(primary_dataset['nya_close'], timeperiod=200)



    # ===================================== sp500 =========================================

    # Common technical indicators
    primary_dataset['sp500_RSI']= ta.RSI(primary_dataset['sp500_close'], timeperiod=14)
    primary_dataset['sp500_MACD']= ta.MACD(primary_dataset['sp500_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['sp500_MACD_signal']= ta.MACD(primary_dataset['sp500_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['sp500_MACD_hist']= ta.MACD(primary_dataset['sp500_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['sp500_ADX']= ta.ADX(primary_dataset['sp500_high'], primary_dataset['sp500_low'], primary_dataset['sp500_close'], timeperiod=14)
    primary_dataset['sp500_CCI']= ta.CCI(primary_dataset['sp500_high'], primary_dataset['sp500_low'], primary_dataset['sp500_close'], timeperiod=14)
    primary_dataset['sp500_ROC']= ta.ROC(primary_dataset['sp500_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['sp500_SMA_10']= ta.SMA(primary_dataset['sp500_close'], timeperiod=10)
    primary_dataset['sp500_SMA_20']= ta.SMA(primary_dataset['sp500_close'], timeperiod=20)
    primary_dataset['sp500_EMA_10']= ta.EMA(primary_dataset['sp500_close'], timeperiod=10)
    primary_dataset['sp500_EMA_20']= ta.EMA(primary_dataset['sp500_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['sp500_SMA_50']= ta.SMA(primary_dataset['sp500_close'], timeperiod=50)
    primary_dataset['sp500_EMA_50']= ta.EMA(primary_dataset['sp500_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['sp500_SMA_100']= ta.SMA(primary_dataset['sp500_close'], timeperiod=100)
    primary_dataset['sp500_SMA_200']= ta.SMA(primary_dataset['sp500_close'], timeperiod=200)
    primary_dataset['sp500_EMA_100']= ta.EMA(primary_dataset['sp500_close'], timeperiod=100)
    primary_dataset['sp500_EMA_200']= ta.EMA(primary_dataset['sp500_close'], timeperiod=200)


    # ===================================== light_crude_oil =========================================

    # Common technical indicators
    primary_dataset['light_crude_oil_RSI']= ta.RSI(primary_dataset['light_crude_oil_close'], timeperiod=14)
    primary_dataset['light_crude_oil_MACD']= ta.MACD(primary_dataset['light_crude_oil_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['light_crude_oil_MACD_signal']= ta.MACD(primary_dataset['light_crude_oil_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['light_crude_oil_MACD_hist']= ta.MACD(primary_dataset['light_crude_oil_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['light_crude_oil_ADX']= ta.ADX(primary_dataset['light_crude_oil_high'], primary_dataset['light_crude_oil_low'], primary_dataset['light_crude_oil_close'], timeperiod=14)
    primary_dataset['light_crude_oil_CCI']= ta.CCI(primary_dataset['light_crude_oil_high'], primary_dataset['light_crude_oil_low'], primary_dataset['light_crude_oil_close'], timeperiod=14)
    primary_dataset['light_crude_oil_ROC']= ta.ROC(primary_dataset['light_crude_oil_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['light_crude_oil_SMA_10']= ta.SMA(primary_dataset['light_crude_oil_close'], timeperiod=10)
    primary_dataset['light_crude_oil_SMA_20']= ta.SMA(primary_dataset['light_crude_oil_close'], timeperiod=20)
    primary_dataset['light_crude_oil_EMA_10']= ta.EMA(primary_dataset['light_crude_oil_close'], timeperiod=10)
    primary_dataset['light_crude_oil_EMA_20']= ta.EMA(primary_dataset['light_crude_oil_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['light_crude_oil_SMA_50']= ta.SMA(primary_dataset['light_crude_oil_close'], timeperiod=50)
    primary_dataset['light_crude_oil_EMA_50']= ta.EMA(primary_dataset['light_crude_oil_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['light_crude_oil_SMA_100']= ta.SMA(primary_dataset['light_crude_oil_close'], timeperiod=100)
    primary_dataset['light_crude_oil_SMA_200']= ta.SMA(primary_dataset['light_crude_oil_close'], timeperiod=200)
    primary_dataset['light_crude_oil_EMA_100']= ta.EMA(primary_dataset['light_crude_oil_close'], timeperiod=100)
    primary_dataset['light_crude_oil_EMA_200']= ta.EMA(primary_dataset['light_crude_oil_close'], timeperiod=200)



    # ===================================== btc =========================================

    # Common technical indicators
    primary_dataset['btc_RSI']= ta.RSI(primary_dataset['btc_close'], timeperiod=14)
    primary_dataset['btc_MACD']= ta.MACD(primary_dataset['btc_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['btc_MACD_signal']= ta.MACD(primary_dataset['btc_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['btc_MACD_hist']= ta.MACD(primary_dataset['btc_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['btc_ADX']= ta.ADX(primary_dataset['btc_high'], primary_dataset['btc_low'], primary_dataset['btc_close'], timeperiod=14)
    primary_dataset['btc_CCI']= ta.CCI(primary_dataset['btc_high'], primary_dataset['btc_low'], primary_dataset['btc_close'], timeperiod=14)
    primary_dataset['btc_ROC']= ta.ROC(primary_dataset['btc_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['btc_SMA_10']= ta.SMA(primary_dataset['btc_close'], timeperiod=10)
    primary_dataset['btc_SMA_20']= ta.SMA(primary_dataset['btc_close'], timeperiod=20)
    primary_dataset['btc_EMA_10']= ta.EMA(primary_dataset['btc_close'], timeperiod=10)
    primary_dataset['btc_EMA_20']= ta.EMA(primary_dataset['btc_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['btc_SMA_50']= ta.SMA(primary_dataset['btc_close'], timeperiod=50)
    primary_dataset['btc_EMA_50']= ta.EMA(primary_dataset['btc_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['btc_SMA_100']= ta.SMA(primary_dataset['btc_close'], timeperiod=100)
    primary_dataset['btc_SMA_200']= ta.SMA(primary_dataset['btc_close'], timeperiod=200)
    primary_dataset['btc_EMA_100']= ta.EMA(primary_dataset['btc_close'], timeperiod=100)
    primary_dataset['btc_EMA_200']= ta.EMA(primary_dataset['btc_close'], timeperiod=200)


    # ===================================== total_crypto_cap =========================================

    # Common technical indicators
    primary_dataset['total_crypto_cap_RSI']= ta.RSI(primary_dataset['total_crypto_cap_close'], timeperiod=14)
    primary_dataset['total_crypto_cap_MACD']= ta.MACD(primary_dataset['total_crypto_cap_close'], fastperiod=12, slowperiod=26, signalperiod=9)[0]
    primary_dataset['total_crypto_cap_MACD_signal']= ta.MACD(primary_dataset['total_crypto_cap_close'], fastperiod=12, slowperiod=26, signalperiod=9)[1]
    primary_dataset['total_crypto_cap_MACD_hist']= ta.MACD(primary_dataset['total_crypto_cap_close'], fastperiod=12, slowperiod=26, signalperiod=9)[2]
    primary_dataset['total_crypto_cap_ADX']= ta.ADX(primary_dataset['total_crypto_cap_high'], primary_dataset['total_crypto_cap_low'], primary_dataset['total_crypto_cap_close'], timeperiod=14)
    primary_dataset['total_crypto_cap_CCI']= ta.CCI(primary_dataset['total_crypto_cap_high'], primary_dataset['total_crypto_cap_low'], primary_dataset['total_crypto_cap_close'], timeperiod=14)
    primary_dataset['total_crypto_cap_ROC']= ta.ROC(primary_dataset['total_crypto_cap_close'], timeperiod=10)

    # Common moving averages

    # Short-term moving averages
    primary_dataset['total_crypto_cap_SMA_10']= ta.SMA(primary_dataset['total_crypto_cap_close'], timeperiod=10)
    primary_dataset['total_crypto_cap_SMA_20']= ta.SMA(primary_dataset['total_crypto_cap_close'], timeperiod=20)
    primary_dataset['total_crypto_cap_EMA_10']= ta.EMA(primary_dataset['total_crypto_cap_close'], timeperiod=10)
    primary_dataset['total_crypto_cap_EMA_20']= ta.EMA(primary_dataset['total_crypto_cap_close'], timeperiod=20)

    # Mid-term moving averages
    primary_dataset['total_crypto_cap_SMA_50']= ta.SMA(primary_dataset['total_crypto_cap_close'], timeperiod=50)
    primary_dataset['total_crypto_cap_EMA_50']= ta.EMA(primary_dataset['total_crypto_cap_close'], timeperiod=50)

    # Long-term moving averages
    primary_dataset['total_crypto_cap_SMA_100']= ta.SMA(primary_dataset['total_crypto_cap_close'], timeperiod=100)
    primary_dataset['total_crypto_cap_SMA_200']= ta.SMA(primary_dataset['total_crypto_cap_close'], timeperiod=200)
    primary_dataset['total_crypto_cap_EMA_100']= ta.EMA(primary_dataset['total_crypto_cap_close'], timeperiod=100)
    primary_dataset['total_crypto_cap_EMA_200']= ta.EMA(primary_dataset['total_crypto_cap_close'], timeperiod=200)

    print(primary_dataset.info())
    # Now it is possible to trim the required period after the averages of the starting point are calculated.
    start_date = pd.to_datetime('2000-01-01')
    end_date = pd.to_datetime(today)
    primary_dataset = primary_dataset.loc[start_date:end_date]
    print(primary_dataset)
    # Check for missing values
    print("Missing values per column:")
    print(primary_dataset.isna().sum())
    output_file_name=str(today.date()).replace("-","_")+".csv"
    # 6 months sample dataset for website display
    cutoff_date = datetime.now() - pd.DateOffset(months=1)
    sample=primary_dataset[primary_dataset.index >= cutoff_date]
    sample.to_csv(os.path.join(full_generated_datasets, "sample_"+output_file_name))
    primary_dataset.to_csv(os.path.join(full_generated_datasets, output_file_name))
    return primary_dataset




traning_dataset(full_dataset())