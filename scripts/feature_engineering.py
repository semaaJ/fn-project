import os 
import numpy as np 
import pandas as pd
import datetime
import pandas_datareader as web
# import numpy_financial as npf

from helpers import *


def SortinoRatio(df, T):
    """Calculates the Sortino ratio from univariate excess returns.

    Args:
        df ([float]): The dataframe or pandas series of univariate excess returns.
        T ([integer]): The targeted return. 
    """

    #downside deviation:

    temp = np.minimum(0, df - T)**2
    temp_expectation = np.mean(temp)
    downside_dev = np.sqrt(temp_expectation)

    sortino_ratio = np.mean(df - T) / downside_dev

    return(sortino_ratio)


def outer(df, window_length):
    # Read in visual results and extract all participant ID's
    spy_df = pd.read_csv("data/csv/SPY.csv", delimiter=',', sep=r', ') 
    spy_df.set_index(["date"], inplace = True)
    bench_return = spy_df["daily_returns"]
    bench_return_prod = np.prod(spy_df["daily_returns"] + 1) - 1

    df['{}d_information_ratio'.format(window_length)] = df['daily_returns'].rolling(window_length).apply(get_information_ratio, args=(bench_return, bench_return_prod, window_length))

    return df

def get_information_ratio(returns, bench_return, bench_return_prod, window_length):
    """ Information ration = (stock return - benchmark return) / tracking)

    """
    # print("Window length", window_length)
    print("SPY_DF", bench_return)
    # print("HERE", returns)

    df_return_prod = np.prod(returns + 1) - 1

    print("df prod", df_return_prod)
    print("spy prod",bench_return_prod)
    print("len df", len(returns))
    print("len spy_df", len(bench_return))

    tracking_error = (returns - bench_return).std() * np.sqrt(window_length)

    information_ratio = (df_return - bench_return_prod) / tracking_error
    print("Information Ratio:", information_ratio)

    return information_ratio

    # print("Window length", window_length)
    # print("SPY_DF", spy_df.head())
    # print("HERE", df.head())
    # # print(df["daily_returns"])
    # df_return = np.prod(df["daily_returns"] + 1) - 1
    # bench_return = np.prod(spy_df["daily_returns"] + 1) - 1

    # # print(df)
    # # tracking_error = (df["daily_returns"].sub(spy_df["daily_returns"], fill_value = 0)).std() * np.sqrt(window_length)
    # tracking_error = (df["daily_returns"] - spy_df["daily_returns"]).std() * np.sqrt(window_length)

    # information_ratio = (df_return - bench_return) / tracking_error
    # print("Information Ratio:", information_ratio)


def create_df_from_json(json_path):
    """ Used to extract all neccessary data from the stock JSON files and say them to a DataFrame
    
    Args:
        json_path (String) : A string representing the file path to the JSON file to be mutated

    """
    data = import_json(json_path)
    historical_data = data["historicalData"]

    data_map = {}
        
    # Collect col_names for DF
    keys_list = list(historical_data[0].keys())
    for col_name in keys_list:
        data_map[col_name] = []

    # Iterate through JSOn and collect data
    df = pd.DataFrame(columns = keys_list)
    for day_results in historical_data:
            # Extract info and save to the appropriate list in data_map
        for key_name in keys_list:
            if key_name == "date":
                data_map[key_name].append(day_results[key_name].split(" ")[0])
            else:
                data_map[key_name].append(day_results[key_name])

        # Populate DF with values
    for col_name, vals in data_map.items():
        df[col_name] = vals

    # Numpy Financial: https://numpy.org/numpy-financial/
    # df["internal_rate_of_return"] = npf.irr(np.array(df["close"]))

    df.columns = [i if i != "price" else i.replace("price", "close") for i in df.columns]

    df.set_index(["date"], inplace = True)
    stock_name = json_path.split("/")[2].replace(".json", ".csv")

    return df


def calculate_inflation_rates(path, name):
    """ Calculate the CPI multiplier for each row in the CSV 
    
    Args: 
        path (String) : A string file path to the folder containing the inflation CSV's 
        name (String) : The name of the of the CSV file containin the inflation info
    """
    inflation_df = pd.read_csv(path + name, delimiter=',', sep=r', ')
    # create index multiplier
    inflation_df["cpiaucns_multiplier"] = inflation_df["cpiaucns"].iloc[-1] / inflation_df["cpiaucns"]

    # Rename column names to lowercase to keep consistency
    col_names = [i.lower() for i in inflation_df.columns]
    inflation_df.columns = col_names

    inflation_df.set_index(["date"], inplace = True)
    create_csv(inflation_df, path, name)

    return


def get_inflation_price_adjustments(df, inflation_df):
    """ Used to calculate the percentage agreement for each row in the agreement_df 
    
    Args: 
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation
        inflation_df (DataFrame) : DataFrame containing the inflation data
    """
    date_vals = list(df.index)
    inf_date_vals = list(inflation_df.index)
    df = pd.merge(df, inflation_df, how='left', on='date')
    # df["CPI_ADJ_PRICE"] = df["CLOSE"] * df["CPIAUCNS_MULTIPLIER"]
    df["cpi_adj_price"] = df["close"] * df["cpiaucns_multiplier"]
    df = df.ffill()

    return df


def calc_volume_and_gain_loss_avgs(df):
    """ Calculates:
            The 20 & 100 day  volume averages
            The daily gain/loss
            The average gain/loss over 7, 14, 50 & 200 day periods
    
    Args: 
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation

    Returns:
        df (DataFrame) : DataFrame with the new columns added
    """
    df["20d_vol_avg"] = df['volume'].rolling(20).mean()
    df["100d_vol_avg"] = df['volume'].rolling(100).mean()

    df['daily_diff'] = df['close'].diff(1)
    df['daily_returns'] = df['close'].pct_change()
    # df['daily_diff_pc_change'] = df['daily_diff'].pct_change()

    df['daily_volume_diff'] = df['volume'].diff(1)
    df['daily_volume_pc_change'] = df['daily_volume_diff'].pct_change()

    # Calculate Avg. Gains/Losses
    df['gain'] = df['daily_diff'].clip(lower=0).round(2)
    df['loss'] = df['daily_diff'].clip(upper=0).abs().round(2)
    
    # Calculate average gain losse for a period of time 
    df = calculate_average_gain_loss(df,7)
    df = calculate_average_gain_loss(df, 14)
    df = calculate_average_gain_loss(df, 50)
    df = calculate_average_gain_loss(df, 200)
    
    return df


def calculate_average_gain_loss(df, window_length):
    """ Calculates the average gain and loss over a given time period as well as the RS and RSI values
    
    Args: 
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation
        window_length (Integer) : The rolling time period we want to calculate the Shapre ratio for

    Returns:
        df (DataFrame) : DataFrame with the new columns added
    """
    df['{}d_avg_gain'.format(window_length)] = df['gain'].rolling(window_length).mean()
    df['{}d_avg_loss'.format(window_length)] = df['loss'].rolling(window_length).mean()

    # Calculate the percentage gain and loss over the specified time period  -- WASNT USEFUL --
    # df['{}d_avg_gain_pc_change'.format(window_length)] = df['gain'].pct_change(periods=window_length)
    # df['{}d_avg_loss_pc_change'.format(window_length)] = df['loss'].pct_change(periods=window_length)
    
    # Calculate RS & RSI Values
    df['{}d_rs'.format(window_length)] = df['{}d_avg_gain'.format(window_length)] / df['{}d_avg_loss'.format(window_length)]
    df['{}d_rsi'.format(window_length)] = 100 - (100 / (1.0 + df['{}d_rs'.format(window_length)]))

    return df


def calculate_sharpe_ratio(df, window_length):
    """ Calculates the Sharpe Ratio over a given time period. That is, the average return of the investment ddivided by the standard deviation

    Args:
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation
        window_length (Integer) : The rolling time period we want to calculate the Shapre ratio for
    Returns:
        df (DataFrame) : DataFrame with the Sharpe ratio added for that time period
    """
    df['{}d_sharpe_ratio'.format(window_length)] = df['daily_returns'].rolling(window_length).apply(sharpe_ratio)

    return df


def sharpe_ratio(data, risk_free_rate=0.0):
    """ Sharpe ratio calculation from: https://medium.datadriveninvestor.com/the-sharpe-ratio-with-python-from-scratch-fbb1d5e490b9
    
    Args:
        data (DataFrame) : A rolling window of values over a given timer period
        risk_free_rate (integer) : Assume no trade is risk free

    Returns:
        Sharpe ratio for that given window of time
    """
    mean_daily_returns = sum(data) / len(data)
    std = data.std()
    daily_sharpe_ratio = (mean_daily_returns - risk_free_rate) / std
    # divide by the length of time we are looking at
    sharpe_ratio = len(data)**(1/2) * daily_sharpe_ratio
    
    return sharpe_ratio


def calculate_maximum_drowdown(df):
    """ Calculates the maximum dropdown over a given period of time

    Args:
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation
        window_length (Integer) : The rolling time period we want to calculate the Shapre ratio for
    Returns:
        df (DataFrame) : DataFrame with the Sharpe ratio added for that time period
    """
    # df = maximum_dropdown(df, 7)
    return df


def maximum_dropdown(df, window_length):
    """ Main function for calculating various volatility metric scores over a rolling range of time periods

    Args:
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation

    Returns:
        df (DataFrame) : DataFrame with all newly created columns addded
    """
    rolling_max = df['close'].rolling(window_length, min_periods=1).max()
    daily_dropdown = df['close'] / rolling_max - 1.0
    Max_Daily_Drawdown = daily_dropdown.rolling(window_length, min_periods=1).min()

    return df


def get_volatility_scores(df):
    """ Main function for calculating various volatility metric scores over a rolling range of time periods

    Args:
        df (DataFrame) : DataFrame containing the stock data with prices to be adjusted for inflation

    Returns:
        df (DataFrame) : DataFrame with all newly created columns addded
    """
    # Calculates the historic volatility over a given time period
    df = calculate_historic_volatility(df, 7)
    df = calculate_historic_volatility(df, 14)
    df = calculate_historic_volatility(df, 252)

    # Calculate the Sharpe Ratio over a given time period
    df = calculate_sharpe_ratio(df, 7)
    df = calculate_sharpe_ratio(df, 14)
    df = calculate_sharpe_ratio(df, 50)
    df = calculate_sharpe_ratio(df, 200)

    return df

def calculate_historic_volatility(df, window_length):
    """ Calculates the volatility of a stock over aa given time period

    """
    df['log_ret'] = np.log(df.close) - np.log(df.close.shift(1))
    # Compute Volatility using the pandas rolling standard deviation function
    df['{}d_historic_volatility_of_risk-adjusted_return'.format(window_length)] = df['log_ret'].rolling(window=window_length).std() * np.sqrt(window_length)

    return df


def feature_engineering_main():
    # Only needs to be ran if new Inflation CSV is added 
    # calculate_inflation_rates("data/us_inflation_rates/", "CPIAUCNS.csv")
    inflation_df = pd.read_csv("data/us_inflation_rates/CPIAUCNS.csv", delimiter=',', sep=r', ')
    inflation_df.set_index(["date"], inplace = True)
    # Might move this into non-main function for general feature engineering
    json_folder_path = "data/json/"
    json_files = os.listdir(json_folder_path)
    for file in json_files:
        csv_path = json_folder_path.replace("json", "csv")
        json_path = json_folder_path + file

        # Convert JSON data to DF format
        df = create_df_from_json(json_path)

        # Apply Inflation rates to get objective price 
        df = get_inflation_price_adjustments(df, inflation_df)
    
        # calculate the volume and 29 avg vol total
        df = calc_volume_and_gain_loss_avgs(df)

        df = calculate_maximum_drowdown(df)

        # Next look at volatility scores
        df = get_volatility_scores(df)

        df = outer(df, 7)
        
        print(df)

        # display_graph_two(list(df["volume"]), list(df["20d_vol_avg"]))

        create_csv(df, csv_path, file.replace(".json", ".csv"))

if __name__ == "__main__":
    feature_engineering_main()