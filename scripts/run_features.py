import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.feature_engineer import FeatureEngineer

def run_feature_engineering():
    print("Starting Feature Engineering...")
    
    # Load processed data
    input_path = os.path.join('data', 'processed', 'retail_sales_cleaned.csv')
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run run_pipeline.py first.")
        return
        
    df = pd.read_csv(input_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    # Initialize engineer
    engineer = FeatureEngineer(df)
    
    # Prepare data for modeling (Daily Sales)
    print("Preparing daily sales data with features...")
    df_features = engineer.prepare_modeling_data(target_col='Total Sales')
    
    # Save feature-rich data
    output_path = os.path.join('data', 'processed', 'daily_sales_features.csv')
    df_features.to_csv(output_path)
    print(f"Saved modeling data to: {output_path}")
    print(f"Shape: {df_features.shape}")
    print("Features created:", list(df_features.columns))

if __name__ == "__main__":
    run_feature_engineering()
