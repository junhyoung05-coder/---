def get_ai_response(message):
    if message == "안녕":
        return "안녕하세요!"
    elif message == "뭐해?":
        return "당신 생각을 하고 있었어요."
    else:
        return "냠냠... (이해하지 못했어요)"

while True:
    user_message = input("나: ")
    
    if user_message == "종료":
        print("종료합니다")
        break
    ai_reply = get_ai_response(user_message)
    print(f"ai: {ai_reply}")