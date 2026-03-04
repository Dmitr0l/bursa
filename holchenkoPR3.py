class Character: #батьківський клас
    def __init__(self, name, hp): # init konstrucktor
        self.name = name
        self.hp = hp

    def attack(self): #funkciya ataki
        print(self.name, "атакує")

    def take_damage(self, damage): #funkciya damaga
        self.hp = self.hp - damage
        print(self.name, "отримав", damage, "шкоди. HP:", self.hp)

class Player(Character): #дочірній клас з наслідування всастивостей батькіського класу
    def __init__(self, name, hp, level):
        super().__init__(name, hp) # тут вже йде виклик батькіського класу
        self.level = level

    def level_up(self):
        self.level = self.level + 1
        print(self.name, "підвищив рівень до", self.level)

class Enemy(Character):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp)
        self.damage = damage

    def attack(self):
        print(self.name, "атакує і завдає", self.damage, "шкоди")

class Item:
    def __init__(self, name, item_type):
        self.name = name
        self.item_type = item_type

    def use(self):
        print(self.name, "використаний")

player = Player("Герой", 100, 1)
enemy = Enemy("Гоблін", 50, 10)
item = Item("Зілля", "зілля")

print("Гра почалась")

while True: #цикл буде виконуватись до тих пір поки ми не введемо 0, а щоб він сам закінчувався мало б бути while player.hp > 0
    print("1 - Атакувати")
    print("2 - Використати предмет")
    print("3 - Підвищити рівень")
    print("0 - Вийти")

    choice = input("Виберіть дію: ")

    if choice == "1":
        player.attack()
        enemy.take_damage(10)

        if enemy.hp > 0:
            enemy.attack()
            player.take_damage(enemy.damage)

    elif choice == "2":
        item.use()

    elif choice == "3":
        player.level_up()

    elif choice == "0":
        print("Кінець гри")
        break #break означає, що ми виходимо з циклом незалежно від результату, а в цій програмі це просто вихід з "гри"

    else:
        print("Невірний вибір")