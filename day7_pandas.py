import pandas as pd
df = pd.read_csv("dirty_dialog.csv")
print("--- [원본 데이터] ---")
print(df)

df_cleaned = df.dropna(subset=['dialog'])
print("\n--- [청소 1: 빈칸 제거 후] ---")
print(df)
df_cleaned['dialog'] = df_cleaned['dialog'].str.replace(r'\[.*?\]|<.*?>', '', regex=True)
print("\nm---청소 2: 태그 제거 후 (최종)] ---")
print(df_cleanmed)
print("\n--- [AI 학습용 데이터셋으로 변환] ---")
for index, row in df_cleaned.iterrows():
    if row['character'] == 'Orc':
        print(f'{{"prompt": "{row["dialog"]}"}}')
    elif row['character'] == 'Human':
        print(f'{{"respinse": "{row["dialog]}"}}')
