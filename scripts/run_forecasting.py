import sys
import os
import pandas as pd
import json
import matplotlib.pyplot as plt

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.forecasting_models import Forecaster

def run_forecasting():
    print("Starting Forecasting...")
    
    # Load feature data (Daily Sales)
    input_path = os.path.join('data', 'processed', 'daily_sales_features.csv')
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run run_features.py first.")
        return
        
    df = pd.read_csv(input_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df = df.set_index('Order Date')
    
    # Initialize forecaster
    forecaster = Forecaster(df)
    
    # Create figures directory
    figures_dir = os.path.join('reports', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # 1. SARIMA Model
    print("\n--- Running SARIMA ---")
    arima_model, arima_pred, arima_conf, arima_metrics = forecaster.run_arima(forecast_days=90)
    print("SARIMA Metrics:", arima_metrics)
    
    # Plot SARIMA
    train, test = forecaster.train_test_split(test_days=90)
    forecaster.plot_forecast(train, test, arima_pred, 'SARIMA Forecast vs Actual', 
                             save_path=os.path.join(figures_dir, 'sarima_forecast.png'))
    
    # 2. Prophet Model
    print("\n--- Running Prophet ---")
    prophet_model, prophet_forecast, prophet_metrics = forecaster.run_prophet(forecast_days=90)
    print("Prophet Metrics:", prophet_metrics)
    
    # Plot Prophet
    # Prophet has its own plot method
    fig1 = prophet_model.plot(prophet_forecast)
    fig1.savefig(os.path.join(figures_dir, 'prophet_forecast_full.png'))
    
    # Custom plot for comparison
    prophet_pred = prophet_forecast.tail(90)['yhat'].values
    forecaster.plot_forecast(train, test, prophet_pred, 'Prophet Forecast vs Actual',
                             save_path=os.path.join(figures_dir, 'prophet_forecast_comparison.png'))
    
    # Save metrics
    metrics = {
        'SARIMA': arima_metrics,
        'Prophet': prophet_metrics
    }
    
    metrics_path = os.path.join('reports', 'model_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"\nForecasting complete. Plots saved to {figures_dir}")
    print(f"Metrics saved to {metrics_path}")

if __name__ == "__main__":
    run_forecasting()
