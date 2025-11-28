import sys
import os
import pandas as pd
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.eda_visualizer import EDAVisualizer

def run_eda():
    print("Starting Exploratory Data Analysis...")
    
    # Load processed data
    input_path = os.path.join('data', 'processed', 'retail_sales_cleaned.csv')
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Run run_pipeline.py first.")
        return
        
    df = pd.read_csv(input_path)
    # Convert dates back to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    # Initialize visualizer
    viz = EDAVisualizer(df)
    
    # Create figures directory
    figures_dir = os.path.join('reports', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # Generate and save plots
    print("Generating plots...")
    
    # 1. Sales Trend
    fig_trend = viz.plot_sales_trend(period='Month')
    fig_trend.write_html(os.path.join(figures_dir, 'sales_trend_monthly.html'))
    
    # 2. Category Performance
    fig_cat = viz.plot_category_performance(metric='Total Sales')
    fig_cat.write_html(os.path.join(figures_dir, 'category_sales.html'))
    
    fig_profit = viz.plot_category_performance(metric='Profit')
    fig_profit.write_html(os.path.join(figures_dir, 'category_profit.html'))
    
    # 3. Regional Heatmap
    fig_map = viz.plot_regional_heatmap()
    fig_map.write_html(os.path.join(figures_dir, 'regional_sales_map.html'))
    
    # 4. Profit vs Discount
    fig_scatter = viz.plot_profit_vs_discount()
    fig_scatter.write_html(os.path.join(figures_dir, 'profit_vs_discount.html'))
    
    # 5. Correlation Heatmap (Static)
    viz.plot_correlation_heatmap(save_path=os.path.join(figures_dir, 'correlation_heatmap.png'))
    
    # Generate Summary Stats
    stats = viz.generate_summary_stats()
    
    # Save insights to JSON
    insights_path = os.path.join('reports', 'eda_insights.json')
    with open(insights_path, 'w') as f:
        json.dump(stats, f, indent=4)
        
    print(f"EDA complete. Plots saved to {figures_dir}")
    print(f"Insights saved to {insights_path}")
    print("Summary Stats:")
    print(json.dumps(stats, indent=4))

if __name__ == "__main__":
    run_eda()
