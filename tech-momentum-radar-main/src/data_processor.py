import pandas as pd
import time
import requests
import os
from pytrends.request import TrendReq
from datetime import datetime

class DataProcessor:
    """
    Handles data collection from external APIs, cleaning, feature engineering, 
    and momentum score calculation.
    """
    def __init__(self, raw_data_dir, processed_data_dir, tech_list=None):
        self.raw_dir = raw_data_dir
        self.processed_dir = processed_data_dir
        self.tech_list = tech_list or ["Large Language Models", "Rust Programming", "WebAssembly", "Vector Databases", "Edge Computing"]
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    # --- Data Collection Methods (Original Functionality) ---

    def fetch_google_trends(self, filename='google_trends.csv'):
        """
        Fetches 5-year historical search interest data from Google Trends.
        """
        print(f"🌐 Collecting Google Trends data for: {self.tech_list}")
        try:
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload(self.tech_list, cat=0, timeframe='today 5-y', geo='', gprop='')
            df = pytrends.interest_over_time()
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            
            path = os.path.join(self.raw_dir, filename)
            df.to_csv(path)
            print(f"✅ Google Trends data saved to {path}")
            return df
        except Exception as e:
            print(f"❌ Error fetching Google Trends: {e}")
            return None

    def fetch_github_stats(self, tech_name):
        """
        Fetches repository statistics (stars, forks) from GitHub API.
        """
        print(f"🐙 Collecting GitHub data for {tech_name}...")
        query = tech_name.replace(" ", "+")
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
        try:
            response = requests.get(url)
            data = response.json()
            if 'items' in data:
                top_repos = data['items'][:5]
                total_stars = sum(repo['stargazers_count'] for repo in top_repos)
                total_forks = sum(repo['forks_count'] for repo in top_repos)
                return {"stars": total_stars, "forks": total_forks, "count": data['total_count']}
        except Exception as e:
            print(f"⚠️ Error fetching GitHub data for {tech_name}: {e}")
        return {"stars": 0, "forks": 0, "count": 0}

    def fetch_stack_exchange_stats(self, tag):
        """
        Fetches question counts from StackOverflow API.
        """
        print(f"💬 Collecting StackOverflow data for {tag}...")
        tag_encoded = tag.lower().replace(" ", "-")
        url = f"https://api.stackexchange.com/2.3/tags/{tag_encoded}/info?site=stackoverflow"
        try:
            response = requests.get(url)
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                item = data['items'][0]
                return {"questions": item['count']}
        except Exception as e:
            print(f"⚠️ Error fetching Stack Exchange data for {tag}: {e}")
        return {"questions": 0}

    def run_full_collection(self, snapshot_file='tech_snapshot.csv'):
        """
        Runs the complete data collection pipeline for all technologies.
        """
        # 1. Fetch Trends
        self.fetch_google_trends()

        # 2. Fetch GitHub & StackOverflow
        snapshot_data = []
        for tech in self.tech_list:
            gh = self.fetch_github_stats(tech)
            so = self.fetch_stack_exchange_stats(tech)
            snapshot_data.append({
                "technology": tech,
                "github_stars": gh['stars'],
                "github_forks": gh['forks'],
                "github_repo_count": gh['count'],
                "so_questions": so['questions'],
                "timestamp": datetime.now().strftime("%Y-%m-%d")
            })
            time.sleep(1) # Rate limiting protection
            
        snapshot_df = pd.DataFrame(snapshot_data)
        path = os.path.join(self.raw_dir, snapshot_file)
        snapshot_df.to_csv(path, index=False)
        print(f"✅ Tech snapshot saved to {path}")
        return snapshot_df

    # --- Data Processing Methods ---

    def process_trends(self, filename='google_trends.csv'):
        """
        Processes search trends data and calculates year-over-year growth rates.
        """
        path = os.path.join(self.raw_dir, filename)
        if not os.path.exists(path):
            print(f"⚠️ {filename} not found. Running collection first...")
            self.fetch_google_trends(filename)
            
        df = pd.read_csv(path, index_col='date', parse_dates=True)
        rolling_df = df.rolling(window=12).mean()
        
        growth_rates = {}
        for col in df.columns:
            last_year_avg = df[col].tail(52).mean()
            prev_year_avg = df[col].iloc[-104:-52].mean()
            growth_rates[col] = (last_year_avg - prev_year_avg) / prev_year_avg if prev_year_avg > 0 else 0
            
        return rolling_df, growth_rates

    def calculate_momentum(self, snapshot_file='tech_snapshot.csv', growth_rates=None):
        """
        Calculates a composite momentum score based on search growth and GitHub metrics.
        """
        path = os.path.join(self.raw_dir, snapshot_file)
        if not os.path.exists(path):
            print(f"⚠️ {snapshot_file} not found. Running collection first...")
            self.run_full_collection(snapshot_file)
            
        df = pd.read_csv(path)
        df['search_growth'] = df['technology'].map(growth_rates)
        
        metrics = ['github_stars', 'github_forks', 'so_questions', 'search_growth']
        for metric in metrics:
            min_val = df[metric].min()
            max_val = df[metric].max()
            df[f'{metric}_norm'] = (df[metric] - min_val) / (max_val - min_val) if max_val > min_val else 0
        
        df['momentum_score'] = (
            df['search_growth_norm'] * 0.4 +
            df['github_stars_norm'] * 0.3 +
            df['so_questions_norm'] * 0.2 +
            df['github_forks_norm'] * 0.1
        ) * 100
        
        df['search_to_code_ratio'] = df['search_growth'] / (df['github_stars'] + 1)
        return df

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processor = DataProcessor(
        raw_data_dir=os.path.join(BASE_DIR, 'data', 'raw'),
        processed_data_dir=os.path.join(BASE_DIR, 'data', 'processed')
    )
    
    # 1. Run Data Collection (Original Logic)
    print("🚀 Starting full data collection pipeline...")
    processor.run_full_collection()
    
    # 2. Run Processing
    print("🧹 Processing data and calculating momentum...")
    trends_df, growth = processor.process_trends()
    trends_df.to_csv(os.path.join(BASE_DIR, 'data', 'processed', 'trends_processed.csv'))
    
    analysis_df = processor.calculate_momentum(growth_rates=growth)
    analysis_df.to_csv(os.path.join(BASE_DIR, 'data', 'processed', 'tech_analysis.csv'), index=False)
    
    print("✅ All tasks completed successfully.")
