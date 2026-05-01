import requests
from bs4 import BeautifulSoup
import json
import datetime
import urllib3

# 証明書警告を無視
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_data():
    # --- 1. 騒音・振動の取得 (強化版) ---
    extra_url = "https://www2.edam.ne.jp/Public/00642/Sokutei/SSC/RN?LoId=738"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    noise, vib = "--", "--"
    try:
        res = requests.get(extra_url, headers=headers, timeout=20, verify=False)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        # ターゲットのIDから取得を試みる
        n_elem = soup.find(id="cur_souon")
        v_elem = soup.find(id="cur_shindou")

        if n_elem:
            noise = n_elem.get_text(strip=True)
        if v_elem:
            vib = v_elem.get_text(strip=True)
            
        # 万が一IDで取れなかった場合の予備（class名などで探す）
        if noise == "--":
            # サイト内の「db」という文字の直前にある数字を探す等の処理
            cells = soup.find_all("td")
            for i, cell in enumerate(cells):
                if "騒音" in cell.text:
                    noise = cells[i+1].get_text(strip=True).replace("dB", "")
                if "振動" in cell.text:
                    vib = cells[i+1].get_text(strip=True).replace("dB", "")

    except Exception as e:
        print(f"Error: {e}")

    # --- 2. WBGT・気象データの取得 (現状のまま) ---
    # ※ここはあなたの既存の取得コードをそのまま入れてください
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
