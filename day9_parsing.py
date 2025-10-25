import requests
from bs4 import BeautifulSoup
url = "https://www.naver.com"
print(f"{url}에 접속을 시도합니다...")

try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    print("n--- [네이버 '오늘 읽을만한 글' 헤드라인 추출] ---")
    headlines = soup.select("ul.list_rank li a.title_link")
    for index, headline in enumerate(headlines):
        print(f"{index + 1}. {headline.text.strip()}")
except requests.exceptions.RequestException as e:
    print(f"오류: 웹사이트에 접속할 수 없습니다. ({e})")
except Exception as e:
    print(f"오류: 데이터를 추출하는 중 문제가 발생했습니다. ({e})")