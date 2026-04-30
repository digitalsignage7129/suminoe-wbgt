import requests
import json
import os

def fetch_weather():
    # 大阪府の詳細予報URL
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
    
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        res.raise_for_status()
        data = res.json()
        
        # 必要な情報の初期化
        temp = 0
        humidity = 60 # 取得できない場合の標準値
        wind = "---"
        weather = "不明"

        # データの抽出（大阪市をターゲット）
        # [0]は短期予報
        time_series = data[0]['timeSeries']
        
        # 天気と風の取得
        weather = time_series[0]['areas'][0]['weathers'][0]
        wind = time_series[0]['areas'][0]['winds'][0]
        
        # 気温の取得
        temp = float(time_series[2]['areas'][0]['temps'][0])

        result = {
            "status": "ok",
            "temp": temp,
            "humidity": humidity, # ※気象庁のこのAPIでは湿度が取れないため現在は固定値
            "wind": wind,
            "weather": weather,
            "updated": os.getenv('GITHUB_RUN_ID', 'manual')
        }

    except Exception as e:
        result = {"status": "err", "msg": str(e)}

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_weather()            "msg": str(e)
        }

    # 上書き保存
    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_weather()
