import os

class GameAction:
    def __init__(self, name):
        self.name = name

    def run(self):
        raise NotImplementedError("помилка")

    def log(self, mes):
        with open("actions.log", "a") as file:
            file.write(mes)


class HealAction(GameAction):
    def __init__(self):
        super().__init__("HEAL")

    def run(self, amount):
        result_message = f"HEAL: відновлено {amount} HP"
        self.log(result_message)


class BuyAction(GameAction):
    def __init__(self):
        super().__init__("BUY")

    def run(self, item, price):
        result_message = f"BUY: куплено {item} за {price} монет"
        self.log(result_message)

heal = HealAction()
buy = BuyAction()

heal.run(15)
buy.run("меч", 10)

with open("actions.log", "a", encoding="utf-8") as f:
    f.write("Тестовий запис\n")
print("Файл записаний у:", os.getcwd())
