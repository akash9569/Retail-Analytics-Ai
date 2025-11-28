import sys
import os
import pandas as pd
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.advanced_analytics import AdvancedAnalytics

def run_advanced_analytics():
    print("Starting Advanced Analytics...")
    
    # Load processed data
    input_path = os.path.join('data', 'processed', 'retail_sales_cleaned.csv')
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run run_pipeline.py first.")
        return
        
    df = pd.read_csv(input_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    # Initialize analytics
    analytics = AdvancedAnalytics(df)
    
    # Create figures directory
    figures_dir = os.path.join('reports', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # 1. Anomaly Detection
    print("Running Anomaly Detection...")
    df_anomalies = analytics.detect_anomalies(contamination=0.01)
    analytics.plot_anomalies(save_path=os.path.join(figures_dir, 'anomalies_scatter.png'))
    
    # Save anomalies to CSV
    anomalies_path = os.path.join('data', 'processed', 'anomalies.csv')
    df_anomalies[df_anomalies['Anomaly'] == 1].to_csv(anomalies_path, index=False)
    
    # 2. Price Elasticity
    print("Calculating Price Elasticity...")
    elasticity_df = analytics.calculate_price_elasticity()
    elasticity_path = os.path.join('reports', 'price_elasticity.csv')
    elasticity_df.to_csv(elasticity_path, index=False)
    print("Price Elasticity:")
    print(elasticity_df)
    
    # 3. Customer Segmentation
    print("Performing Customer Segmentation...")
    rfm_df = analytics.perform_customer_segmentation()
    rfm_path = os.path.join('data', 'processed', 'customer_segments.csv')
    rfm_df.to_csv(rfm_path, index=False)
    
    # Summary of segments
    segment_summary = rfm_df.groupby('Segment').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Customer ID': 'count'
    }).to_dict()
    
    # Save insights
    insights = {
        'anomalies_detected': int(df_anomalies['Anomaly'].sum()),
        'price_elasticity': elasticity_df.to_dict(orient='records'),
        'customer_segments': segment_summary
    }
    
    insights_path = os.path.join('reports', 'advanced_insights.json')
    with open(insights_path, 'w') as f:
        json.dump(insights, f, indent=4)
        
    print(f"Advanced analytics complete. Insights saved to {insights_path}")

if __name__ == "__main__":
    run_advanced_analytics()
