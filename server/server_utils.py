import pandas as pd
import pickle
import numpy as np
from fastapi import HTTPException
import os
# from server_util_functions import create_features
# from . import server_util_functions
import server_util_functions


current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
project_path = os.path.dirname(current_directory)


def load_model(product_name : str):

    file_path = os.path.join(current_directory, "server_models", f"lgbm_{product_name}.pkl")
    with open(file_path, "rb") as f:
        lgbm_model = pickle.load(f)

    return lgbm_model


def load_dataset(product_name : str):

    # file_path = os.path.join(current_directory, "products_df", f"{product_name}_weekly_sale.csv")
    file_path = os.path.join(project_path, "model", "products_df", f"{product_name}_weekly_sale.csv")
    sales_df = pd.read_csv(file_path)
    sales_df["date"] = [pd.Timestamp(i) for i in sales_df["date"]]
    sales_df.set_index("date", inplace=True)
    return sales_df


def get_prediction(product_name : str, forward_weeks : int):
    
    lgbm_model = load_model(product_name)
    sales_df = load_dataset(product_name)

    for _ in range(forward_weeks):
        
        sales_df_input = server_util_functions.create_features(sales_df).drop("demand", axis=1).tail(1)
        next_pred = lgbm_model.predict(sales_df_input)
        next_pred = int(next_pred[0])

        next_ts = sales_df.index[-1] + pd.offsets.Week(1)
        new_entry = pd.DataFrame({'demand': [next_pred]}, 
                                index=pd.DatetimeIndex([next_ts])
                            )

        sales_df = pd.concat([sales_df, new_entry])
    
    predictions = list(sales_df["demand"][-forward_weeks:])
    predictions_ts = list(sales_df.index[-forward_weeks:])
    
    output = server_util_functions.make_dict_format_result(predictions, predictions_ts)

    return output


