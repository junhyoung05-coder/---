class character:
    def __init__(self, name, level):
        self.name = name
        self.level = level
    def introduce(self):
        print(f"안녕하세요, 저는 {self.name}입니다")
        print(f"레벨은 {self.level}입니다.")
    
    
hero = character("아이언맨", 50)
    
hero.introduce()
