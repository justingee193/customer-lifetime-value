from lifetimes import ParetoNBDFitter
from lifetimes import ModifiedBetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.generate_data import modified_beta_geometric_nbd_model
from lifetimes.generate_data import pareto_nbd_model

def model(data):
    
    pareto = ParetoNBDFitter(penalizer_coef=0.0)
    pareto.fit(frequency=data['frequency_cal'],
               recency=data['recency_cal'], 
               T=data['T_cal'])
    
    mbg = ModifiedBetaGeoFitter(penalizer_coef=0.0)
    mbg.fit(frequency=data['frequency_cal'],
            recency=data['recency_cal'], 
            T=data['T_cal'])
    
    return pareto, mbg

def predictions(pareto, mbg, summary):
    
    pred_purchases_pareto = pareto.conditional_expected_number_of_purchases_up_to_time(
            t=365,
            frequency=summary['frequency'],
            recency=summary['recency'],
            T=summary['T'])
    
    pred_purchases_mbg = mbg.conditional_expected_number_of_purchases_up_to_time(
            t=365,
            frequency=summary['frequency'],
            recency=summary['recency'],
            T=summary['T'])
    
    return pred_purchases_pareto, pred_purchases_mbg
    
def clv(pareto, mbg, summary):
    
    returning_customers_summary = summary[summary['frequency']>0]
    
    ggf = GammaGammaFitter(penalizer_coef=0.0)
    ggf.fit(frequency=returning_customers_summary['frequency'],
            monetary_value=returning_customers_summary['monetary_value'])
    
    pred_clv_pareto = ggf.customer_lifetime_value(
            transaction_prediction_model=pareto,
            frequency=summary['frequency'], 
            recency=summary['recency'],
            T=summary['T'],
            monetary_value=summary['monetary_value'],
            time=12,
            freq="D")
    
    pred_clv_mbg = ggf.customer_lifetime_value(
            transaction_prediction_model=mbg, 
            frequency=summary['frequency'], 
            recency=summary['recency'],
            T=summary['T'], 
            monetary_value=summary['monetary_value'],
            time=12,
            freq="D")
    
    return pred_clv_pareto, pred_clv_mbg

def simulate(pareto, mbg):
    
    times = [10, 365, 3650, 36500]
    r_par, alpha_par, s, beta = pareto.params_
    r_mbg, alpha_mbg, a, b = mbg.summary['coef']
    size = 100
    
    for duration in times:
        generated_customers_par = pareto_nbd_model(
                T=duration,
                r=r_par,
                alpha=alpha_par,
                s=s,
                beta=beta,
                size=size)
        
        generated_customers_mbg = modified_beta_geometric_nbd_model(
                T=duration, 
                r=r_mbg, 
                alpha=alpha_mbg,
                a=a,
                b=b,
                size=size)
    
        print("Duration: {}".format(duration))
        print("Pareto/NBD : Modified BG/NBD")
        print("Number of Purchases: {} : Number of Purchases: {}".format(
                generated_customers_par['frequency'].sum(),
                generated_customers_mbg['frequency'].sum()))
    
        print("Number of Customers Alive: {} : Number of Customers Alive: {}".format(
                generated_customers_par['alive'].sum(),
                generated_customers_mbg['alive'].sum()))
        print("-----------------------------------------------------------------")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    