import requests
import json
import datetime
import urllib3
import re

# 証明書警告を無視
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_data():
    # --- 1. 騒音・振動の取得 (正規表現による強制抽出) ---
    extra_url = "https://www2.edam.ne.jp/Public/00642/Sokutei/SSC/RN?LoId=738"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    noise, vib = "--", "--"
    try:
        res = requests.get(extra_url, headers=headers, timeout=20, verify=False)
        res.encoding = 'utf-8'
        html_text = res.text

        # ID「cur_souon」の直後にある数値を抽出する正規表現
        noise_match = re.search(r'id="cur_souon"[^>]*>([\d\.]+)', html_text)
        vib_match = re.search(r'id="cur_shindou"[^>]*>([\d\.]+)', html_text)

        if noise_match:
            noise = noise_match.group(1)
        if vib_match:
            vib = vib_match.group(1)

    except Exception as e:
        print(f"Error: {e}")

    # --- 2. WBGT・気象データの取得 (現状のまま) ---
    # ※ここは既存の取得ロジックを入れてください
    wbgt_val = "17.0" 
    temp_val = "20"
    weather_text = "くもり"
    wind_text = "西の風"

    # --- 3. データの書き出し ---
    data = {
        "status": "ok",
        "wbgt": wbgt_val,
        "temp": temp_val,
        "weather": weather_text,
        "wind": wind_text,
        "noise": noise,
        "vib": vib,
        "updated": datetime.datetime.now().strftime('%Y%m%d%H%M')
    }

    with open('weather_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_data()
