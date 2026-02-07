from storage import save_state, load_state

default_state = {
    "player_name": "Дядюшка Епштейн",
    "level": 67,
    "coins": 100,
    "inventory": {"Ключ від підвалу": 1},
    "settings": {"Режим гри", "Звук", "Відео"}
}

#з файлу storage.py беремо збереження чи дефолтні значення
game_state = load_state("save.json", default_state)

# Цикл гри
while True:
    print("1) Показати стан")
    print("2) Додати монети")
    print("3) Додати предмет")
    print("4) Зберегти")
    print("5) Вийти")

    choice = input("Оберіть: ")

    if choice == "1":
        print(game_state)

    elif choice == "2":
        game_state["coins"] += int(input("Монети: "))

    elif choice == "3":
        item = input("Назва: ")
        count = int(input("Кількість: "))
        game_state["inventory"][item] = game_state["inventory"].get(item, 0) + count

    elif choice == "4":
        save_state("save.json", game_state)
        print("Збережено")

    elif choice == "5":
        if input("Зберегти? (так/ні): ") == "так":
            save_state("save.json", game_state)
        break
