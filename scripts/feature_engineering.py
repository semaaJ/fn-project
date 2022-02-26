import os 
import numpy as np 
import pandas as pd
import numpy_financial as npf

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

    col_names = df.columns

    new_col_names = [i if i != "price" else i.replace("price", "close") for i in col_names]
    df.columns = new_col_names

    df.set_index(["date"], inplace = True)
    stock_name = json_path.split("/")[2].replace(".json", ".csv")

    return df

def calculate_inflation_rates(path, name):
    """ Used to calculate the percentage agreement for each row in the agreement_df 
    Args: 
        csv_folder_path (String) : A string file path to the folder containing the inflation CSV's 

    """
    inflation_df = pd.read_csv(path + name, delimiter=',', sep=r', ')
    # create index multiplier
    inflation_df["cpiaucns_multiplier"] = inflation_df["cpiaucns"].iloc[-1] / inflation_df["cpiaucns"]

    # Rename column names to lowercase to keep consistency
    col_names = [i.lower() for i in inflation_df.columns]

    inflation_df.columns = col_names

    inflation_df.set_index(["date"], inplace = True)
    # print(inflation_df)
    print(inflation_df)
    print(path)
    print(name)
    create_csv(inflation_df, path, name)

    return


def get_inflation_price_adjustments(df, inflation_df):

    date_vals = list(df.index)
    inf_date_vals = list(inflation_df.index)
    # print(inflation_df)
    df = pd.merge(df, inflation_df, how='left', on='date')
    # df["CPI_ADJ_PRICE"] = df["CLOSE"] * df["CPIAUCNS_MULTIPLIER"]
    df["cpi_adj_price"] = df["close"] * df["cpiaucns_multiplier"]
    df = df.ffill()
    # print(df)
    return df

def calculate_treasury_yield_to_maturity(df):
    """
        create row of 6mo, 1year, 2year etc whatever treasury bond lengths are

    """

    return df


def calc_volume_and_gain_loss_avgs(df):
    df["20d_vol_avg"] = df['volume'].rolling(20).mean()
    df["100d_vol_avg"] = df['volume'].rolling(100).mean()

    df['daily_diff'] = df['close'].diff(1)

    # Calculate Avg. Gains/Losses
    df['gain'] = df['daily_diff'].clip(lower=0).round(2)
    df['loss'] = df['daily_diff'].clip(upper=0).abs().round(2)
    
    # Calculate average gain losse for a period of time 
    df = calculate_average_gain_loss(df,7)
    df = calculate_average_gain_loss(df, 14)
    

    return df


def my_rolling_sharpe(y):
    
    return np.sqrt(126) * (y.mean() / y.std()) # 21 days per month X 6 months = 126




def calculate_average_gain_loss(df, window_length):

    df['{}d_avg_gain'.format(window_length)] = df['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
    df['{}d_avg_loss'.format(window_length)] = df['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]

    for i, row in enumerate(df['{}d_avg_gain'.format(window_length)].iloc[window_length+1:]):
        df['{}d_avg_gain'.format(window_length)].iloc[i + window_length + 1] = (df['{}d_avg_gain'.format(window_length)].iloc[i + window_length] * (window_length - 1) + df['gain'].iloc[i + window_length + 1]) / window_length

    # Average Losses
    for i, row in enumerate(df['{}d_avg_loss'.format(window_length)].iloc[window_length+1:]):
        df['{}d_avg_loss'.format(window_length)].iloc[i + window_length + 1] = (df['{}d_avg_loss'.format(window_length)].iloc[i + window_length] * (window_length - 1) + df['loss'].iloc[i + window_length + 1]) / window_length

    # Calculate RS Values
    df['{}d_rs'.format(window_length)] = df['{}d_avg_gain'.format(window_length)] / df['{}d_avg_loss'.format(window_length)]
    # Calculate RSI
    df['{}d_rsi'.format(window_length)] = 100 - (100 / (1.0 + df['{}d_rs'.format(window_length)]))

    return df


def sharpe_ratio(df, time_period):
    """ Calculates daily Sharpe Ratio. That is, the average return of the investment. And divided by the standard deviation

    """
    df['{}d_sharpe_ratio'.format(time_period)] = df['close'].rolling(time_period).apply(my_rolling_sharpe)

    return df


def get_volatility_scores(df):

    df = sharpe_ratio(df, 7)
    df = sharpe_ratio(df, 14)

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

        # df = calculate_treasury_yield_to_maturity(df)
    
        # calculate the volume and 29 avg vol total
        df = calc_volume_and_gain_loss_avgs(df)

        # Next look at volatility scores
        df = get_volatility_scores(df)
        
        print(df)

        # display_graph_two(list(df["volume"]), list(df["20d_vol_avg"]))

        create_csv(df, csv_path, file.replace(".json", ".csv"))

if __name__ == "__main__":
    feature_engineering_main()