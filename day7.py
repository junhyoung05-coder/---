import json

def save_data(data, filename="ai_data.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"\n[시스템: 데이터가 {filename}에 저장되었습니다.]")

def load_data(filename="ai_data.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"\n[시스템: {filename} 파일을 찾을 수 없습니다. 새 파일을 생성합니다.]")
        return {"name": "오구리", "favor": 50}
def get_ai_response(message, status):
    if message == "안녕":
        status["favor"] += 1
        return f"안녕하세요! (현재 호감도: {status['favor']})", status
    elif message == "내 이름이 뭐야?":
        return f"당신의 이름은 .... {status['name']} 아닌가요?", status
    elif message == "호감도":
        return f"현재 호감도는 {status['favor']}입니다.", status
    else:
        return "냠냠....(이해하지 못했어요.)", status
ai_status = load_data()
print("[시스템: AI 친구가 온라인 상태입니다..]")
while True:
    user_message = input("나:  ")
    if user_message == "종료":
        save_data(ai_status)
        print("ai: 대화를 종료합니다.")
        break
    ai_reply, ai_status = get_ai_response(user_message, ai_status)
    print(f"AI: {ai_reply}")



