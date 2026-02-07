import json
import os


def save_state(path: str, state: dict) -> bool:
    # це функція з шляхом до файлу як у завданні
    tmp = path + ".tmp"

    try:
        # Записуємо дані у тимчасовий JSON-файл
        with open(tmp, "w",) as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

        # Якщо запис успішний змінюється осн файл
        os.replace(tmp, path)
        return True

    except:
        # При помилці повертається фолс без ламання файлу
        return False


def load_state(path: str, default: dict) -> dict:
    # Якщо файлу збереження немає повертаємо default
    if not os.path.exists(path):
        return default.copy()

    try:
        # тут йде спроба зчитування файлу
        with open(path, "r") as f:
            data = json.load(f)
    except:
        #При пошкодженному чи непрвлильному файлі повернемо дефолтне значення
        return default.copy()

    # Якщо дані не є словникомб еремо default
    if not isinstance(data, dict):
        return default.copy()

    result = default.copy()

    #якщо ключ є у файлі беремо його, а якщо нема беремо дефолт
    for key in default:
        if key in data:
            result[key] = data[key]

    # level має бути цілим і не від’ємним
    if not isinstance(result["level"], int) or result["level"] < 0:
        result["level"] = default["level"]

    # coins так жеж
    if not isinstance(result["coins"], int) or result["coins"] < 0:
        result["coins"] = default["coins"]

    # inventory має бути словником, а не масивом
    if not isinstance(result["inventory"], dict):
        result["inventory"] = default["inventory"]

    # settings не є масивом, а є словником
    if not isinstance(result["settings"], dict):
        result["settings"] = default["settings"]

    # поверне нормальний стан гри
    return result
