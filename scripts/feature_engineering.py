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
        print
    for col_name, vals in data_map.items():
        df[col_name] = vals

    # Numpy Financial: https://numpy.org/numpy-financial/
    # df["internal_rate_of_return"] = npf.irr(np.array(df["close"]))

    # df.set_index(["date"], inplace = True)
    stock_name = json_path.split("/")[2].replace(".json", ".csv")

    return df

def calculate_inflation_rates(path, name):
    """ Used to calculate the percentage agreement for each row in the agreement_df 
    Args: 
        csv_folder_path (String) : A string file path to the folder containing the inflation CSV's 

    """
    name 
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

    date_vals = list(df["date"])
    inf_date_vals = list(inflation_df["date"])

    df = pd.merge(df, inflation_df, how='left', on='date')
    # df["CPI_ADJ_PRICE"] = df["CLOSE"] * df["CPIAUCNS_MULTIPLIER"]
    df["cpi_adj_price"] = df["close"] * df["cpiaucns_multiplier"]
    df = df.ffill()

    return df

def calculate_treasury_yield_to_maturity(df):
    """
        create row of 6mo, 1year, 2year etc whatever treasury bond lengths are

    """

    return df


def calculate_rolling_avg_volume(df):
    df["20d_vol_avg"] = df['volume'].rolling(20).mean()
    df["100d_vol_avg"] = df['volume'].rolling(100).mean()

    df['daily_diff'] = df['close'].diff(1)

    return df



def feature_engineering_main():
    # Only needs to be ran if new Inflation CSV is added 
    # calculate_inflation_rates("data/us_inflation_rates/", "CPIAUCNS.csv")
    inflation_df = pd.read_csv("data/us_inflation_rates/CPIAUCNS.csv", delimiter=',', sep=r', ')

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
        df = calculate_rolling_avg_volume(df)

        # Next look at volatility scores
        
        print(df)

        # display_graph_two(list(df["volume"]), list(df["20d_vol_avg"]))

        # create_csv(df, csv_path, file.replace(".json", ".csv"))

if __name__ == "__main__":
    feature_engineering_main()