import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import warnings
warnings.filterwarnings('ignore')

class Forecaster:
    def __init__(self, df):
        self.df = df.copy()
        # Ensure index is datetime
        if not isinstance(self.df.index, pd.DatetimeIndex):
            self.df.index = pd.to_datetime(self.df.index)
            
    def train_test_split(self, test_days=90):
        """Splits data into train and test sets."""
        train = self.df.iloc[:-test_days]
        test = self.df.iloc[-test_days:]
        return train, test
        
    def evaluate_model(self, y_true, y_pred, model_name):
        """Evaluates model performance."""
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
        
        return {
            'Model': model_name,
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }
        
    def run_arima(self, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7), forecast_days=90):
        """Runs SARIMA model."""
        train, test = self.train_test_split(test_days=forecast_days)
        
        print(f"Training SARIMA{order}x{seasonal_order}...")
        model = SARIMAX(train['Total Sales'], 
                        order=order, 
                        seasonal_order=seasonal_order,
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        
        results = model.fit(disp=False)
        
        # Forecast
        forecast = results.get_forecast(steps=forecast_days)
        y_pred = forecast.predicted_mean
        conf_int = forecast.conf_int()
        
        # Evaluate
        metrics = self.evaluate_model(test['Total Sales'], y_pred, 'SARIMA')
        
        return results, y_pred, conf_int, metrics
        
    def run_prophet(self, forecast_days=90):
        """Runs Facebook Prophet model."""
        train, test = self.train_test_split(test_days=forecast_days)
        
        # Prepare data for Prophet
        prophet_df = train.reset_index()[['Order Date', 'Total Sales']]
        prophet_df.columns = ['ds', 'y']
        
        print("Training Prophet model...")
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        model.add_country_holidays(country_name='US')
        model.fit(prophet_df)
        
        # Forecast
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)
        
        # Extract predictions for test period
        y_pred = forecast.tail(forecast_days)['yhat'].values
        
        # Evaluate
        metrics = self.evaluate_model(test['Total Sales'], y_pred, 'Prophet')
        
        return model, forecast, metrics
        
    def plot_forecast(self, train, test, y_pred, title, save_path=None):
        """Plots the forecast against actuals."""
        plt.figure(figsize=(14, 7))
        plt.plot(train.index[-180:], train['Total Sales'][-180:], label='Train (Last 6 Months)')
        plt.plot(test.index, test['Total Sales'], label='Actual Test')
        plt.plot(test.index, y_pred, label='Forecast', color='red')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
