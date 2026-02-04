from prakt5 import load_state, save_state

default_state = {
    "player_name": "Влад",
    "level": 1,
    "coins": 100,
    "inventory": {"меч", "щит", "повістка"},
    "settings": {"Volume", "Graphics"}
}

game_state = load_state("save.json", default_state)

while True:
    print("""
1) Показати стан
2) Додати монети
3) Додати предмет
4) Зберегти
5) Вийти
""")

    choice = input("Вибір: ")

    if choice == "1":
        print(game_state)

    elif choice == "2":
        game_state["coins"] += int(input("Скільки монет: "))

    elif choice == "3":
        name = input("Назва предмета: ")
        qty = int(input("Кількість: "))
        inv = game_state["inventory"]
        inv[name] = inv.get(name, 0) + qty

    elif choice == "4":
        save_state("save.json", game_state)
        print("Збережено")

    elif choice == "5":
        if input("Зберегти? (т/н): ") == "т":
            save_state("save.json", game_state)
        break