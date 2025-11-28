import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class EDAVisualizer:
    def __init__(self, df):
        self.df = df.copy()
        # Set style
        sns.set(style="whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
    def plot_sales_trend(self, period='Month', save_path=None):
        """Plots sales trend over time."""
        if period == 'Month':
            data = self.df.groupby(['Year', 'Month'])['Total Sales'].sum().reset_index()
            data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(DAY=1))
        elif period == 'Year':
            data = self.df.groupby('Year')['Total Sales'].sum().reset_index()
            data['Date'] = pd.to_datetime(data['Year'], format='%Y')
        
        fig = px.line(data, x='Date', y='Total Sales', title=f'Total Sales Trend by {period}')
        if save_path:
            fig.write_image(save_path)
        return fig
        
    def plot_category_performance(self, metric='Total Sales', save_path=None):
        """Plots performance by category."""
        data = self.df.groupby('Category')[metric].sum().sort_values(ascending=False).reset_index()
        
        fig = px.bar(data, x='Category', y=metric, color='Category', title=f'{metric} by Category')
        if save_path:
            fig.write_image(save_path)
        return fig
        
    def plot_regional_heatmap(self, save_path=None):
        """Plots a heatmap of sales by State."""
        data = self.df.groupby('State')['Total Sales'].sum().reset_index()
        
        fig = px.choropleth(data, 
                            locations='State', 
                            locationmode="USA-states", 
                            color='Total Sales',
                            scope="usa",
                            title='Sales by State')
        if save_path:
            fig.write_image(save_path)
        return fig
    
    def plot_correlation_heatmap(self, save_path=None):
        """Plots correlation heatmap for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr = self.df[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap')
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
            
    def plot_profit_vs_discount(self, save_path=None):
        """Plots profit vs discount relationship."""
        fig = px.scatter(self.df, x='Discount', y='Profit', color='Category', 
                         trendline="ols", title='Profit vs Discount Impact')
        if save_path:
            fig.write_image(save_path)
        return fig
        
    def generate_summary_stats(self):
        """Generates summary statistics."""
        summary = {
            'Total Sales': self.df['Total Sales'].sum(),
            'Total Profit': self.df['Profit'].sum(),
            'Total Orders': len(self.df),
            'Avg Order Value': self.df['Total Sales'].mean(),
            'Profit Margin': (self.df['Profit'].sum() / self.df['Total Sales'].sum()) * 100
        }
        return summary
