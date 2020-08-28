import reformat
import model
import visuals

def main():
    import pandas as pd
    
    df = pd.read_csv("customer-data.csv")
    
    summary, holdout = reformat.reformat(df)
    print(summary.head())
    
    pareto, mbg = model.model(holdout)
    print(pareto.params_)
    print(mbg.summary['coef'])
    
    pred_purchases_pareto, pred_purchases_mbg = model.predictions(pareto, mbg, summary)
    
    pred_clv_pareto, pred_clv_mbg = model.clv(pareto, mbg, summary)
    
    model.simulate(pareto, mbg)
    
    visuals.future_prediction_plot(pareto, holdout, n=50)
    visuals.future_prediction_plot(mbg, holdout, n=50)
    
    visuals.transaction_plot(pareto)
    visuals.transaction_plot(mbg)
    
if __name__ == "__main__":
    main()
