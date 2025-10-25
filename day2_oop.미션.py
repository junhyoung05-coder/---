class AI_Agent:
    def __init__(self, ai_name, start_favor, initial_state):
        self.name = ai_name
        self.favor = start_favor
        self.state = initial_state
oguri = AI_Agent("오구리", 70, "배고픔")
gemini = AI_Agent("제미나이", 69, "활성화")

print(f"{oguri.name}의 초기 호감도:{oguri.favor} 상태:{oguri.state}")
print(f"{gemini.name}의 초기 호감도:{gemini.favor} 상태:{gemini.state}")


