import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

class AdvancedAnalytics:
    def __init__(self, df):
        self.df = df.copy()
        
    def detect_anomalies(self, contamination=0.01):
        """Detects anomalies in sales using Isolation Forest."""
        # Prepare data (Sales and Profit)
        X = self.df[['Total Sales', 'Profit']].fillna(0)
        
        # Train model
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        self.df['Anomaly'] = iso_forest.fit_predict(X)
        self.df['Anomaly'] = self.df['Anomaly'].map({1: 0, -1: 1}) # 1 for anomaly, 0 for normal
        
        num_anomalies = self.df['Anomaly'].sum()
        print(f"Detected {num_anomalies} anomalies.")
        
        return self.df
        
    def calculate_price_elasticity(self):
        """Calculates price elasticity of demand."""
        # Elasticity = % Change in Quantity / % Change in Price
        # We'll do this by Category
        elasticity_data = []
        
        for category in self.df['Category'].unique():
            cat_df = self.df[self.df['Category'] == category]
            
            # Log-log regression to find elasticity
            # ln(Quantity) = a + b * ln(Price)
            # b is the elasticity
            
            # Filter out zero or negative prices/quantities
            cat_df = cat_df[(cat_df['Unit Price'] > 0) & (cat_df['Quantity'] > 0)]
            
            if len(cat_df) > 10:
                x = np.log(cat_df['Unit Price'])
                y = np.log(cat_df['Quantity'])
                
                slope, intercept = np.polyfit(x, y, 1)
                elasticity_data.append({
                    'Category': category,
                    'Price Elasticity': slope,
                    'Interpretation': 'Elastic' if abs(slope) > 1 else 'Inelastic'
                })
                
        return pd.DataFrame(elasticity_data)
        
    def perform_customer_segmentation(self, n_clusters=3):
        """Segments customers using RFM analysis and K-Means."""
        # RFM Analysis
        # Recency: Days since last order
        # Frequency: Total number of orders
        # Monetary: Total sales value
        
        current_date = self.df['Order Date'].max() + pd.Timedelta(days=1)
        
        rfm = self.df.groupby('Customer ID').agg({
            'Order Date': lambda x: (current_date - x.max()).days,
            'Order ID': 'count',
            'Total Sales': 'sum'
        }).reset_index()
        
        rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']
        
        # Normalize
        X = rfm[['Recency', 'Frequency', 'Monetary']]
        X_norm = (X - X.mean()) / X.std()
        
        # K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        rfm['Cluster'] = kmeans.fit_predict(X_norm)
        
        # Label clusters (simple logic based on Monetary)
        cluster_avg = rfm.groupby('Cluster')['Monetary'].mean().sort_values()
        cluster_map = {
            cluster_avg.index[0]: 'Low Value',
            cluster_avg.index[1]: 'Mid Value',
            cluster_avg.index[2]: 'High Value'
        }
        if n_clusters > 3: # Fallback if more clusters
             cluster_map = {i: f'Cluster {i}' for i in range(n_clusters)}
             
        rfm['Segment'] = rfm['Cluster'].map(cluster_map)
        
        return rfm
        
    def plot_anomalies(self, save_path=None):
        """Plots anomalies."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='Total Sales', y='Profit', hue='Anomaly', palette={0: 'blue', 1: 'red'})
        plt.title('Anomaly Detection: Sales vs Profit')
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
