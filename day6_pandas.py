import pandas as pd
try:
    df = pd.read_csv("game_items.csv")
    print("--- 전체 아이템 목록 (DataGrame) ---")
    print(df)

    print("\n--- 아이템 이름(name)만 보기 ---")
    print(df["name"])
    print("\n--- 가격(price)이 100 이상인 아이템 ---")
    print(df[df["price"] >= 100])
except FileNotFoundError:
    print("오류: game_items.csv 파일을 찾을 수 없습니다.")
    print("day6_pandas.py와 같은 폴더에 파일이 있는지 확인하세요.")
        