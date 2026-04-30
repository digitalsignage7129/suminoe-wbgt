import requests
import json
import os

def fetch_weather():
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
    
    try:
        # 気象庁へのアクセス
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        res.raise_for_status()
        data = res.json()
        
        # 気温データを総当たりで探す（エラー防止）
        temps = []
        for series in data[0]['timeSeries']:
            if 'temps' in series['areas'][0]:
                for area in series['areas']:
                    if "大阪" in area['area']['name']:
                        temps = [t for t in area['temps'] if t]
                        break
            if temps: break

        if not temps:
            raise ValueError("気温データが見つかりませんでした")

        # 保存するデータの作成
        result = {
            "status": "ok",
            "temps": temps,
            "updated": os.getenv('GITHUB_RUN_ID', 'manual')
        }

    except Exception as e:
        result = {
            "status": "err",
            "msg": str(e)
        }

    # 上書き保存
    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_weather()
