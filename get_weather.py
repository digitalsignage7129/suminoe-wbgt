import requests
import json
import os
import csv
from io import StringIO

def fetch_wbgt():
    # 近畿地方のデータ (p8.csv は近畿地方)
    url = "https://www.wbgt.env.go.jp/prev15_mail/csv/p8.csv"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=15)
        res.encoding = 'shift_jis'
        
        f = StringIO(res.text)
        reader = csv.reader(f)
        
        wbgt_val = None
        
        for row in reader:
            # 行の中に「大阪」という文字が含まれているかチェック
            if len(row) > 2 and "大阪" in row[1]:
                # 行の右側（最新時刻）から順に、有効な数値を探す
                for val in reversed(row):
                    val = val.strip()
                    # 空白でなく、かつ数字（小数含む）である場合
                    if val and val.replace('.', '', 1).isdigit():
                        wbgt_val = val
                        break
                if wbgt_val: break

        # 気象庁予報
        w_res = requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json", headers=headers)
        w_data = w_res.json()
        
        # 数値が見つからなかった時のための予備計算（気温から推計）
        temp_raw = w_data[0]['timeSeries'][2]['areas'][0]['temps'][0]
        if not wbgt_val:
            wbgt_val = str(round(float(temp_raw) * 0.73 + 2.4, 1))

        result = {
            "status": "ok",
            "wbgt": wbgt_val,
            "temp": temp_raw,
            "weather": data_get(w_data, 0, 'weathers'),
            "wind": data_get(w_data, 0, 'winds'),
            "updated": os.getenv('GITHUB_RUN_ID', 'manual')
        }

    except Exception as e:
        result = {"status": "err", "msg": str(e)}

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def data_get(data, index, key):
    try:
        return data[0]['timeSeries'][index]['areas'][0][key][0]
    except:
        return "---"

if __name__ == "__main__":
    fetch_wbgt()
