import sys
import os
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_cleaner import DataCleaner

def run_cleaning_pipeline():
    print("Starting data cleaning pipeline...")
    
    # Load raw data
    input_path = os.path.join('data', 'raw', 'retail_sales_dataset.csv')
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run generate_data.py first.")
        return
        
    df = pd.read_csv(input_path)
    print(f"Loaded raw data: {df.shape}")
    
    # Initialize cleaner
    cleaner = DataCleaner(df)
    
    # Fix date formats
    cleaner.fix_date_formats(['Order Date', 'Ship Date'])
    
    # Handle missing values
    cleaner.handle_missing_values()
    
    # Remove duplicates
    cleaner.remove_duplicates()
    
    # Handle outliers in Sales and Profit
    # We cap them to avoid extreme values affecting models too much, 
    # but we keep them as they might be real high-value orders
    print("Handling outliers...")
    cleaner.cap_outliers('Total Sales', method='iqr')
    cleaner.cap_outliers('Profit', method='iqr')
    
    # Create time features
    cleaner.create_time_features('Order Date')
    
    # Get cleaned data
    df_cleaned = cleaner.get_cleaned_data()
    
    # Save processed data
    output_path = os.path.join('data', 'processed', 'retail_sales_cleaned.csv')
    df_cleaned.to_csv(output_path, index=False)
    print(f"Saved cleaned data to: {output_path}")
    print(f"Final shape: {df_cleaned.shape}")
    
    return df_cleaned

if __name__ == "__main__":
    run_cleaning_pipeline()
