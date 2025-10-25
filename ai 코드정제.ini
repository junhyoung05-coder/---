import pandas as pd

try:
    # 1. 지저분한 CSV 파일 읽기
    df = pd.read_csv("dirty_dialog.csv")
    print("--- [원본 데이터] ---")
    print(df)

    # 2. [청소 1] 빈칸(결측치)이 있는 행 제거하기
    # [수정 1] 'subset'으로 오타 수정
    df_cleaned = df.dropna(subset=['dialog']) 
    print("\n--- [청소 1: 빈칸 제거 후] ---")
    # [수정 2] 원본 'df'가 아닌 'df_cleaned'를 출력
    print(df_cleaned) 

    # 3. [청소 2] 불필요한 태그([TAG], <TAG>) 제거하기
    # (팁: .copy()를 사용하면 SettingWithCopyWarning 경고가 뜨지 않습니다.)
    df_cleaned = df_cleaned.copy() 
    df_cleaned['dialog'] = df_cleaned['dialog'].str.replace(r'\[.*?\]|<.*?>', '', regex=True)
    
    # [수정 3, 4] print문 오타 및 변수 이름 오타 수정
    print("\n--- [청소 2: 태그 제거 후 (최종)] ---")
    print(df_cleaned)

    # 4. (선택) 청소된 데이터를 JSONL 파일로 저장하기
    print("\n--- [AI 학습용 데이터셋으로 변환] ---")
    for index, row in df_cleaned.iterrows():
        
        # [수정 5] 'orc' -> 'Orc' (대소문자 구분)
        if row['character'] == 'Orc':
            print(f'{{"prompt": "{row["dialog"]}"}}')
            
        elif row['character'] == 'Human':
            # [수정 6, 7] 'respinse' -> 'response', 'fialog' -> 'dialog'
            print(f'{{"response": "{row["dialog"]}"}}')

except FileNotFoundError:
    print("오류: dirty_dialog.csv 파일을 찾을 수 없습니다.")
    print("day7_pandas.py와 같은 폴더에 파일이 있는지 확인하세요.")