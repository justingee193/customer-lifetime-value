from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases
from lifetimes.plotting import plot_period_transactions

def future_prediction_plot(model, holdout, n=50):
    return plot_calibration_purchases_vs_holdout_purchases(model, holdout, n=50)

def transaction_plot(model):
    return plot_period_transactions(model)
