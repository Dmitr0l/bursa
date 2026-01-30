inventory = {"меч": 1, "зілля": 2}

store = {"щит": 150, "зілля": 75, "Кайло": 80}

balance = int(input("Введіть ваш баланс: "))
def view_inventory(inventory):
    if not inventory:
        print("Бомжара, твій інвентар пустий")
        return

    print("Інвентарь:")
    for item, count in inventory.items():
        print(f"{item}: {count}")

def buy_item(item_name, store, balance, inventory):
    if item_name not in store:
        raise ValueError("Такого предмету немає в магазині")
    
    price = store[item_name]
    
    if balance < price:
        raise ValueError("недостатньо коштів")

    balance -= price
    
    if item_name in inventory:
        inventory[item_name] += 1
    else:
        inventory[item_name] = 1

    print("Куплено: ", item_name)
    return balance

try:
    buy_item("щит", store, balance, inventory)
except ValueError as e:
    print("Помилка:", e)