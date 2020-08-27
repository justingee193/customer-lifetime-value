import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes.utils import calibration_and_holdout_data

def reformat(data):
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], 
                                       format='%Y/%m/%d %H:%M').dt.date
        
    summary = summary_data_from_transaction_data(
            transactions=data,
            customer_id_col='CustomerID', 
            datetime_col='Timestamp', 
            monetary_value_col='PurchaseValue',
            observation_period_end='2017-12-06',
            freq='D').reset_index()
    
    summary_cal_holdout = calibration_and_holdout_data(
            transactions=data,
            customer_id_col='CustomerID', 
            datetime_col='Timestamp',
            calibration_period_end='2017-07-12',
            observation_period_end='2017-12-06',
            freq='D',
            monetary_value_col='PurchaseValue').reset_index()
    
    return summary, summary_cal_holdout
    