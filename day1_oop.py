class AI_Agent:
    pass
ai_friend1 = AI_Agent()
ai_friend2 = AI_Agent()

print(ai_friend1)
print(ai_friend2)

class player:
    is_alive = True
    level = 1

Player1 = player()
Player2 = player()
print(f"플레이어 1의 레벨: {Player1.level}")

Player2.level = 10
Player2.is_alive = False

print(f"플레이어 2의 레벨: {Player2.level}")
