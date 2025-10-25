game_items = ["포션", "골드", "지도", "검"]
print("보유 아이템:", game_items)

print("첫 번째 아이템:", game_items[0])
print("세 번쨰 아이템:", game_items[2])

game_items.append("방패")
print("아이템 추가 후:", game_items)

game_items[1] = "골드 100개"
print("아이템 수정 후", game_items)

player_level = 99
plater_exp = 55
required_exp = 100
current_money = 12500
item_price = 3000
print("필요 경험치:", required_exp - plater_exp)
print("아이템을 최대 몇 개 상 수 있나?:", current_money // item_price)
print("구매 후 남는 돋:", current_money % item_price)
print("레벨이 99 레벨과 같나요?:", player_level == 99)
print("경험치가 100 이상인가요?:", plater_exp >= 100)
for item in game_items:
    print(item + "을(를) 확인했습니다.")
for i in range(5):
    print(f"[{i + 1}번쨰 공격] 몬스터에게 10 데미지를 입혔습니다.")
player_hp = 5
while player_hp > 0:
    print(f"현재 체력: {player_hp}")
    player_hp = player_hp - 1
print("체력이 모두 소진되어 게임 오버!")
