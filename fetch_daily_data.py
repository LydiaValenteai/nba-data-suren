import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

# 清除代理，防止被 Cloudflare 拦截
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

print("Status: Starting data ingestion for NBA Season 2025-26...")

try:
    log = leaguegamelog.LeagueGameLog(
        season="2025-26", 
        player_or_team_abbreviation="P",
        timeout=100
    )
    df = log.get_data_frames()[0]
    df.columns = df.columns.str.lower()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "nba_daily_live.csv")
    
    df.to_csv(file_path, index=False)
    print("Success: Data saved.")

except Exception as e:
    print(f"Error: {e}")