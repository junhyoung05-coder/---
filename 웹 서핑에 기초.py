import requests
url = "https://www.naver.com"
print(f"{url}에 접속을 시도합니다...")
try:
    response = requests.get(url)

    response.raise_for_status()

    print("\n--- [접속 성공] HTML 코드 ---")
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"오류: 웹사이트에 접속할 수 없습니다. ({e})")
    