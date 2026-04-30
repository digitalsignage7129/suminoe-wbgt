import requests
import json
import os

def fetch_weather():
    # 気象庁（大阪府）
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 大阪市の気温データを抽出
        temp_series = next(s for s in data[0]['timeSeries'] if 'temps' in s['areas'][0])
        osaka_data = next(a for a in temp_series['areas'] if a['area']['name'] == "大阪市")
        # 空のデータを除外して数値のみにする
        temps = [t for t in osaka_data['temps'] if t != ""]

        if not temps:
            raise ValueError("気温データが空です")

        # ★ここが重要：辞書形式を正しく閉じる
        result = {
            "status": "ok",
            "temps": temps,
            "updated": os.getenv('GITHUB_RUN_ID', 'manual-run')
        }

    except Exception as e:
        result = {
            "status": "err",
            "msg": str(e)
        }

    # ファイルに書き出す
    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_weather()
