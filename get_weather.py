import requests
from bs4 import BeautifulSoup
import json
import datetime
import urllib3

# 証明書警告を非表示
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_data():
    # --- 1. 騒音・振動の取得 (指定サイトから切り抜き) ---
    extra_url = "https://www2.edam.ne.jp/Public/00642/Sokutei/SSC/RN?LoId=738"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(extra_url, headers=headers, timeout=15, verify=False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        noise = soup.find(id="cur_souon").text.strip()
        vib = soup.find(id="cur_shindou").text.strip()
    except:
        noise, vib = "--", "--"

    # --- 2. WBGT・気象データの取得 (既存ロジックをここに集約) ---
    # ※ここは現在動作しているWBGT取得コードを反映させてください
    # 今回は例として固定値ですが、実際には既存の取得処理が入ります
    wbgt_val = "17.0" 
    temp_val = "20"
    weather_text = "くもり"
    wind_text = "西の風"

    # --- 3. データの統合と保存 ---
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
