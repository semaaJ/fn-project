import os 
import numpy as np 
import pandas as pd

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


def create_df_from_json(path):
    """ Used to extract all neccessary data from the stock JSON files and say them to a DataFrame
    Args:
        json_path (String) : A string representing the file path to the JSON file to be mutated
    """
    json_files = os.listdir(path)
    for file in json_files:
        json_path = path + file
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
                    key_result = day_results[key_name]
                    data_map[key_name].append(key_result)

        # Populate DF with values
        for col_name, vals in data_map.items():
            df[col_name] = vals

        stock_name = json_path.split("/")[2].replace(".json", ".csv")
        create_csv(df, stock_name)

    return


def create_csv(df, name):
    print("Creating ", name)
    file_path = "data/csv/" + name
    df.to_csv(file_path)
    return



def feature_engineering_main():

    # display_graph(close_list)
    create_df_from_json("data/json/")

    linear_regression(date_list, close_list)

if __name__ == "__main__":
    feature_engineering_main()