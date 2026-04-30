import requests
import json
import os
import csv
from io import StringIO

def fetch_wbgt():
    # 環境省の大阪（地点番号：62078）の最新データURL
    # ※CSV形式で公開されているものを取得します
    url = "https://www.wbgt.env.go.jp/prev15_mail/csv/p8.csv" # 近畿地方のデータ
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'shift_jis' # 環境省のCSVはShift-JISが多いです
        
        # CSVを解析して「大阪」のデータを探す
        f = StringIO(res.text)
        reader = csv.reader(f)
        
        wbgt_val = "---"
        for row in reader:
            # 「大阪」という地点名が含まれる行を探す（地点番号 62078）
            if "62078" in row or "大阪" in row:
                # 最新のWBGT値を取得（列の位置はデータ形式に依存するため、安全に抽出）
                # 通常、最新値は末尾の方に含まれます
                wbgt_val = row[-1] 
                break

        # 気象庁から天気と風もついでに取得（環境省データには無いため）
        weather_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
        w_res = requests.get(weather_url, headers=headers)
        w_data = w_res.json()
        
        result = {
            "status": "ok",
            "wbgt": wbgt_val, # 環境省の公式値
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
