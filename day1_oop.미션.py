class GameCHaracter:
    health = 100
    attack_power = 10

my_hero = GameCHaracter()
enemy_orc = GameCHaracter()

enemy_orc.attack_power = 20
my_hero.health = 55

print(f"나의 영웅 체력: {my_hero.health}")
print(f"나의 영웅 공격력: {my_hero.attack_power}")
print(f"오크 체력: {enemy_orc.health}")
print(f"오크 공격력: {enemy_orc.attack_power}")
