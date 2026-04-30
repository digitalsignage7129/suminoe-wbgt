import requests
import json
import os
import traceback

def fetch_weather():
    # 気象庁（大阪府）
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
    
    try:
        # ユーザーエージェント（ブラウザのふりをする設定）を追加
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # データの抽出をより確実にする
        try:
            area_data = data[0]['timeSeries'][2]['areas']
            osaka = next(a for a in area_data if a['area']['name'] == "大阪市")
            temps = [t for t in osaka['temps'] if t]
        except:
            # 抽出に失敗した場合は別の場所を探す
            temp_series = next(s for s in data[0]['timeSeries'] if 'temps' in s['areas'][0])
            osaka = next(a for a in temp_series['areas'] if a['area']['name'] == "大阪市")
            temps = [t for t in osaka['temps'] if t]

        if not temps:
            raise ValueError("気温データが見つかりませんでした")

        result = {
            "status": "ok",
            "temps": temps,
            "updated": os.getenv('GITHUB_RUN_ID', 'manual-run')
        }

    except Exception as e:
        # ★エラーの詳細を msg に書き出す
        error_detail = traceback.format_exc()
        result = {
            "status": "err",
            "msg": f"{str(e)} | Detail: {error_detail[:100]}"
        }

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_weather()
