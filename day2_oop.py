class character:
    def __init__(self, name, start_level):
        self.name = name
        self.level = start_level
        self.is_alive = True
hero = character("아이언맨", 50)
enemy = character("타노스", 100)

print(f"{hero.name}의 레벨: {hero.level}")
print(f"{enemy.name}의 레벨: {enemy.level}")