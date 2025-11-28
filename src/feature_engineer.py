import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()
        
    def create_lag_features(self, target_col='Total Sales', lags=[1, 3, 7, 14, 30]):
        """Creates lag features for the target column."""
        # We need to aggregate by date first if we have multiple entries per date
        # But for the main dataset, we might want to forecast daily sales
        daily_sales = self.df.groupby('Order Date')[target_col].sum().reset_index()
        daily_sales = daily_sales.set_index('Order Date')
        
        for lag in lags:
            daily_sales[f'lag_{lag}'] = daily_sales[target_col].shift(lag)
            
        return daily_sales
        
    def create_rolling_features(self, df, target_col='Total Sales', windows=[7, 30, 90]):
        """Creates rolling mean and std features."""
        for window in windows:
            df[f'rolling_mean_{window}'] = df[target_col].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df[target_col].rolling(window=window).std()
        return df
        
    def create_ema_features(self, df, target_col='Total Sales', alphas=[0.1, 0.3, 0.5]):
        """Creates exponential moving average features."""
        for alpha in alphas:
            df[f'ema_{alpha}'] = df[target_col].ewm(alpha=alpha, adjust=False).mean()
        return df
        
    def add_holiday_flags(self, df):
        """Adds holiday flags."""
        import holidays
        us_holidays = holidays.US()
        
        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
            
        df['IsHoliday'] = df.index.map(lambda x: 1 if x in us_holidays else 0)
        return df
        
    def prepare_modeling_data(self, target_col='Total Sales'):
        """Prepares the final dataset for modeling."""
        # Aggregate to daily level
        daily_df = self.create_lag_features(target_col)
        
        # Add rolling features
        daily_df = self.create_rolling_features(daily_df, target_col)
        
        # Add EMA features
        daily_df = self.create_ema_features(daily_df, target_col)
        
        # Add holiday flags
        daily_df = self.add_holiday_flags(daily_df)
        
        # Add time features again since we aggregated
        daily_df['DayOfWeek'] = daily_df.index.dayofweek
        daily_df['Month'] = daily_df.index.month
        daily_df['Quarter'] = daily_df.index.quarter
        daily_df['Year'] = daily_df.index.year
        
        # Drop NaN values created by lags
        daily_df = daily_df.dropna()
        
        return daily_df
