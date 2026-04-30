import requests
import json
import os

# 気象庁のURL（大阪府）
JMA_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
# 保存するファイル名
OUTPUT_FILE = "weather_data.json"

def fetch_weather():
    try:
        response = requests.get(JMA_URL)
        response.raise_for_status() # エラーなら例外を出す
        
        # 必要なのは「大阪市」の気温だけ
        data = response.json()
        temp_series = next(s for s in data[0]['timeSeries'] if 'temps' in s['areas'][0])
        osaka_data = next(a for a in temp_series['areas'] if a['area']['name'] == "大阪市")
        temps = [t for t in osaka_data['temps'] if t != ""]

        # 保存するデータ
        result = {
            "status": "ok",
            "temps": temps,
            "updated": os.getenv('GITHUB_RUN_ID') # 更新ID
        }

        # JSONファイルとして保存
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Error: {e}")
        # エラー時はstatusをerrにする
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump({"status": "err", "msg": str(e)}, f)

if __name__ == "__main__":
    fetch_weather()
