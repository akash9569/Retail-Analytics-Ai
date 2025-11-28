import pandas as pd
import numpy as np
from scipy import stats

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        
    def fix_date_formats(self, date_cols):
        """Converts columns to datetime objects."""
        for col in date_cols:
            self.df[col] = pd.to_datetime(self.df[col])
        return self.df
        
    def handle_missing_values(self):
        """Handles missing values in the dataset."""
        # For numeric columns, fill with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())
            
        # For categorical columns, fill with mode
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
            
        return self.df
    
    def remove_duplicates(self):
        """Removes duplicate rows."""
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        print(f"Removed {removed} duplicate rows.")
        return self.df
        
    def detect_outliers_zscore(self, col, threshold=3):
        """Detects outliers using Z-score."""
        z_scores = np.abs(stats.zscore(self.df[col]))
        return z_scores > threshold
        
    def detect_outliers_iqr(self, col):
        """Detects outliers using IQR method."""
        Q1 = self.df[col].quantile(0.25)
        Q3 = self.df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
    
    def cap_outliers(self, col, method='iqr'):
        """Caps outliers instead of removing them."""
        if method == 'iqr':
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            self.df[col] = np.where(self.df[col] < lower_bound, lower_bound, self.df[col])
            self.df[col] = np.where(self.df[col] > upper_bound, upper_bound, self.df[col])
            
        return self.df
        
    def create_time_features(self, date_col='Order Date'):
        """Creates time-based features from a date column."""
        self.df['Year'] = self.df[date_col].dt.year
        self.df['Quarter'] = self.df[date_col].dt.quarter
        self.df['Month'] = self.df[date_col].dt.month
        self.df['Week'] = self.df[date_col].dt.isocalendar().week
        self.df['Day'] = self.df[date_col].dt.day
        self.df['DayOfWeek'] = self.df[date_col].dt.dayofweek
        self.df['IsWeekend'] = self.df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
        self.df['MonthName'] = self.df[date_col].dt.month_name()
        self.df['DayName'] = self.df[date_col].dt.day_name()
        return self.df
        
    def get_cleaned_data(self):
        return self.df
