class Character:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def attack(self):
        print(f"{self.name} нападає!")

    def take_damage(self, dmg):
        self.hp -= dmg
        print(f"{self.name} отримав {dmg} урона!")
        print(f"Поточне HP: {self.hp}")
    
    def __str__(self):
        return f"Персонаж: {self.name}, HP: {self.hp}"
    

class Player(Character):
    def __init__(self, name, hp, lvl):
        super().__init__(name, hp)
        self.lvl = lvl


class Enemy(Character):
    def __init__(self, name, hp, dmg):
        super().__init__(name, hp)
        self.dmg = dmg

    def attack(self, target):
        print(f"{self.name} нападає і завдає {self.dmg} урона!")
        target.take_damage(self.dmg)


class Item:
    def __init__(self, name, item_type):
        self.name = name
        self.item_type = item_type

    def use(self, target):
        pass


class Heal(Item):
    def __init__(self, name, heal_amount):
        super().__init__(name, "heal")
        self.heal_amount = heal_amount

    def use(self, target):
        target.hp += self.heal_amount
        print(f"{target.name} використав {self.name} і відновив {self.heal_amount} HP")
        print(f"Поточне HP: {target.hp}")


player = Player("Ухилянт", 100, 12)
enemy = Enemy("ТеЦеКашник", 50, 20)

heal = Heal("Аптечка", 46)

print(player)
print(enemy)

heal.use(player)
enemy.attack(player)

player.attack()

print(player)
print(enemy)
