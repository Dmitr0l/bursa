inventory = {
    "зілля": 1
}

store = {
    "меч": 100,
    "щит": 80,
    "зілля": 30
}
#^ cписки інвентаря та магазина
balance = 10


#функція перегляду інвентаря
def view_inventory(inventory):
    print("Інвентар:")
    if not inventory:
        print("Порожній")
    else:
        for item in inventory:
            print(item, "-", inventory[item])


# основна функція в якій іде механізм покупка предметів
def buy_item(item_name, inventory, store, balance):
    #перевірка наявності предмету
    if item_name not in store:
        raise ValueError("Такого предмета немає в магазині")

    price = store[item_name]

    # перевірка на "бідність"
    if balance < price:
        raise ValueError("Недостатньо монет")

    # при покупці предмета зміншується баланс
    balance = balance - price

    # Якщо такий предмет є в інвентарі ми добавляємо його значення кількості
    if item_name in inventory:
        inventory[item_name] = inventory[item_name] + 1
    else:
        inventory[item_name] = 1

    print("Ви купили:", item_name)
    return balance #як би на балансі не було return, то у нас постійно був би баланс 150, а при ньому він повертає нове значення балансу

print("Магазин")

while True:
    print("Меню:")
    print("1 - Переглянути інвентар")
    print("2 - Купити предмет")
    print("3 - Перевірити баланс")
    print("0 - Вийти")

    choice = input("Ваш вибір: ")

    if choice == "1":
        view_inventory(inventory)

    elif choice == "2":
        print("Доступні пропозиції:", store)
        item = input("Введіть назву предмета: ")

        try:
            balance = buy_item(item, inventory, store, balance)
        except ValueError as e:
            print("Помилка:", e)

    elif choice == "3":
        print("Баланс:", balance, "монет")

    elif choice == "0":
        print("Програма завершена")
        break #при виклику вийде з циклу

    else:
        print("Невірний вибір")
