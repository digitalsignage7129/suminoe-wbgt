import requests
from bs4 import BeautifulSoup
import json
import datetime

def get_site_data():
    url = "https://www2.edam.ne.jp/Public/00642/Sokutei/SSC/RN?LoId=738"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # サイト内のID「cur_souon」と「cur_shindou」から数値を取得
        noise = soup.find(id="cur_souon").text.strip()
        vib = soup.find(id="cur_shindou").text.strip()
        
        return noise, vib
    except Exception as e:
        print(f"Error fetching site data: {e}")
        return "--", "--"

# --- 既存のWBGT取得ロジックの後に以下のように統合 ---
noise, vib = get_site_data()

data = {
    "status": "ok",
    "wbgt": "17.0", # ここは既存の変数を入れてください
    "temp": "20",   # ここは既存の変数を入れてください
    "noise": noise, # 抽出した騒音値
    "vib": vib,     # 抽出した振動値
    "updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
