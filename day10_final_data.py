import requests
from bs4 import BeautifulSoup
import pandas as pd 

url = "https://ko.wikipedia.org/wiki/비디오_게임_인공지능" 

try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, "html.parser")
    
    data_list = [] 
    
    # [최종 수정] 주소를 더 간단하고 확실하게 변경!
    toc_items = soup.select("span.vector-toc-text")
    
    if not toc_items:
        # (디버깅을 위해 print문도 수정)
        print("오류: 'span.vector-toc-text' 주소에서 목차를 찾지 못했습니다.")
    
    for index, item in enumerate(toc_items):
        data_list.append({
            "id": index + 1,
            "category": "비디오 게임",
            "title": item.text.strip()
        })
        
    df = pd.DataFrame(data_list)
    
    print("--- [최종 데이터프레임 (비디오 게임)] ---")
    print(df)

except requests.exceptions.RequestException as e:
    print(f"오류: 웹사이트에 접속할 수 없습니다. ({e})")
except Exception as e:
    printf(f"오류: 데이터를 추출하는 중 문제가 발생했습니다. ({e})")