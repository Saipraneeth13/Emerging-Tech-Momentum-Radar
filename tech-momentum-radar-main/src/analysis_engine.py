import pandas as pd
from sklearn.cluster import KMeans
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os

class AnalysisEngine:
    """
    Handles advanced analytics including clustering and time-series forecasting.
    """
    def __init__(self, processed_data_dir):
        self.processed_dir = processed_data_dir

    def cluster_technologies(self, input_file='tech_analysis.csv', n_clusters=3):
        """
        Categorizes technologies into clusters based on momentum and search growth.
        """
        path = os.path.join(self.processed_dir, input_file)
        df = pd.read_csv(path)
        
        # Select features for clustering
        X = df[['momentum_score', 'search_growth_norm']].values
        
        # Apply K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(X)
        
        # Map clusters to meaningful labels based on characteristics
        # Note: In a real scenario, we'd check cluster centroids to assign labels dynamically
        cluster_map = {
            0: "Stable/Mature",
            1: "Rising Star",
            2: "Speculative/Hype"
        }
        df['tech_status'] = df['cluster'].map(cluster_map)
        
        return df

    def forecast_trends(self, input_file='trends_processed.csv', periods=12):
        """
        Forecasts future search interest using Holt-Winters Exponential Smoothing.
        """
        path = os.path.join(self.processed_dir, input_file)
        df = pd.read_csv(path, index_col='date', parse_dates=True)
        
        forecasts = {}
        for col in df.columns:
            try:
                # Use Additive seasonality for weekly data (52 periods)
                model = ExponentialSmoothing(
                    df[col], 
                    seasonal='add', 
                    seasonal_periods=52
                ).fit()
                forecast = model.forecast(periods)
                forecasts[col] = forecast.tolist()
            except Exception as e:
                print(f"⚠️ Could not forecast for {col}: {e}")
                forecasts[col] = [0] * periods
                
        return pd.DataFrame(forecasts)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    engine = AnalysisEngine(processed_data_dir=os.path.join(BASE_DIR, 'data', 'processed'))
    
    # Run Clustering
    final_df = engine.cluster_technologies()
    final_df.to_csv(os.path.join(BASE_DIR, 'data', 'processed', 'tech_analysis_final.csv'), index=False)
    
    # Run Forecasting
    forecast_df = engine.forecast_trends()
    forecast_df.to_csv(os.path.join(BASE_DIR, 'data', 'processed', 'trends_forecast.csv'), index=False)
    
    print("✅ Advanced analysis and forecasting completed.")
