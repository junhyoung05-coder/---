ai_status = {
    "name": "오구리",
    "favor": 50
}
def get_ai_response(message, status):
    if message == "안녕":
        status["level"] += 1
        return f"안녕하세요! (현재 호감도: {status['favor']})", status
    elif message == "내 이름이 뭐야?":
        return f"당신의 이름은 .... {status['name']} 아닌가요?", status
    elif message == "호감도":
        return f"현재 호감도는 {status['favor']}입니다.", status
    else:
        return "냠냠...(이해하지 못했어요.)", status

while True:
    user_message = input("나: ")
    if user_message == "종료":
        print("AI: 대화를 종료합니다.")
        break
    ai_reply, ai_status = get_ai_response(user_message, ai_status)
    print(f"AI: {ai_reply}")

    