import pandas as pd

def create_features(df: pd.DataFrame):

    df_new = df.copy()
    df_new['lag1'] = df_new['demand'].shift(1)
    df_new['lag2'] = df_new['demand'].shift(2)
    df_new['rolling_mean'] = df_new['demand'].rolling(4).mean()
    df_new['month'] = df_new.index.month
    df_new['week'] = df_new.index.isocalendar().week
    return df_new.dropna()


def make_dict_format_result(predictions, prediction_ts):
    
    output = []

    for pred_value, pred_ts in zip(predictions, prediction_ts):
        tmp = {
            "ts": pred_ts.isoformat(),
            "prediction": pred_value
        }
        output.append(tmp)
    
    return output
    
    


