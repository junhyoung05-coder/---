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
        # [수정 1] 쉼표 추가
        return {"name": "오구리", "favor": 70, "state": "배고픔"} 

class AI_Agent:
    def __init__(self, ai_name, start_favor, initial_state):
        self.name = ai_name
        self.favor = start_favor
        self.state = initial_state
        
    def get_response(self, message):
        if message == "안녕":
            self.favor += 1
            return f"안녕하세요! 호감도가 1 올랐습니다. (현재 호감도: {self.favor})"
        elif message == "호감도":
            return f"현재 호감도:{self.favor}"
        else:
            return "냠냠...(이해하지못했습니다)"
            
    def get_status_dict(self):
        # [수정 2] 쉼표 추가
        return {
            "name": self.name,
            "favor": self.favor,
            "state": self.state
        }

# --- [메인 루프] ---
    
loaded_data = load_data()

# [수정 3] 쉼표 추가
oguri = AI_Agent(
    ai_name=loaded_data["name"],
    start_favor=loaded_data["favor"],
    initial_state=loaded_data["state"]
)

print(f"[시스템: ai 친구 '{oguri.name}'가 온라인 상태입니다. (호감도: {oguri.favor})]")

while True:
    user_message = input("나: ")
    
    if user_message == "종료":
        save_data(oguri.get_status_dict())
        print("종료합니다")
        break
        
    ai_reply = oguri.get_response(user_message)
    print(f"ai: {ai_reply}")