import requests
import json
import os
import csv
from io import StringIO

def fetch_wbgt():
    # 環境省の近畿地方データCSV
    url = "https://www.wbgt.env.go.jp/prev15_mail/csv/p8.csv"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'shift_jis'
        
        f = StringIO(res.text)
        reader = csv.reader(f)
        
        wbgt_val = "0.0"
        for row in reader:
            # 地点番号 62078 (大阪) を探す
            if "62078" in row:
                # 行の右側（最新時刻）から順に、数字が入っている列を探す
                for val in reversed(row):
                    clean_val = val.strip()
                    if clean_val and clean_val.replace('.', '', 1).isdigit():
                        wbgt_val = clean_val
                        break
                break

        # 気象庁予報（天気・風・気温用）
        w_res = requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json", headers=headers)
        w_data = w_res.json()
        
        result = {
            "status": "ok",
            "wbgt": wbgt_val,
            "temp": w_data[0]['timeSeries'][2]['areas'][0]['temps'][0],
            "weather": w_data[0]['timeSeries'][0]['areas'][0]['weathers'][0],
            "wind": w_data[0]['timeSeries'][0]['areas'][0]['winds'][0],
            "updated": os.getenv('GITHUB_RUN_ID', 'manual')
        }

    except Exception as e:
        result = {"status": "err", "msg": str(e)}

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_wbgt()
