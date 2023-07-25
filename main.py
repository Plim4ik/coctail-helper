import tkinter as tk
import json
import random

# Загрузка данных из JSON файла
with open('cocktails.json', 'r', encoding='utf-8') as file:
    cocktails_data = json.load(file)

# Функция для формирования отдельного JSON файла с ингредиентами
def create_ingredients_json():
    ingredients_list = []
    for cocktail in cocktails_data["cocktails"]:
        for ingredient in cocktail["ingredients"]:
            if ingredient not in ingredients_list:
                ingredients_list.append(ingredient)

    ingredients_json = {
        "ingredients": ingredients_list
    }

    with open('ingredients.json', 'w', encoding='utf-8') as outfile:
        json.dump(ingredients_json, outfile, ensure_ascii=False, indent=4)

# Проверяем наличие файла с ингредиентами, и если его нет, создаем и заполняем
try:
    with open('ingredients.json', 'r', encoding='utf-8') as file:
        # Проверяем, если файл пустой или не содержит JSON данных
        file_data = file.read()
        if not file_data.strip():
            create_ingredients_json()
    with open('ingredients.json', 'r', encoding='utf-8') as file:
        ingredients_data = json.load(file)
except FileNotFoundError:
    create_ingredients_json()
    with open('ingredients.json', 'r', encoding='utf-8') as file:
        ingredients_data = json.load(file)

# Функция для поиска коктейлей по выбранным ингредиентам
def find_cocktails():
    selected_ingredients = list(ingredients_var.get())
    found_cocktails = []

    for cocktail in cocktails_data["cocktails"]:
        if all(ingredient.lower().strip() in [ing.lower().strip() for ing in selected_ingredients] for ingredient in cocktail["ingredients"]):
            found_cocktails.append(cocktail)

    if found_cocktails:
        # Вывод подробной информации о найденных коктейлях
        result_text.delete(1.0, tk.END)
        for cocktail in found_cocktails:
            result_text.insert(tk.END, f"{cocktail['name']}:\n")
            result_text.insert(tk.END, f"Ингредиенты: {', '.join(cocktail['ingredients'])}\n")
            result_text.insert(tk.END, f"Дозировки: {', '.join(str(amount) for amount in cocktail['ingredients_amounts'])}\n")
            result_text.insert(tk.END, f"Инструкции: {', '.join(cocktail['recipe_steps'])}\n")
            result_text.insert(tk.END, "-"*50 + "\n")
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Коктейль с выбранными ингредиентами не найден.")

# Функция для вывода случайного коктейля с полным рецептом
def random_cocktail():
    random_cocktail = random.choice(cocktails_data["cocktails"])

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"{random_cocktail['name']}:\n")
    result_text.insert(tk.END, f"Ингредиенты: {', '.join(random_cocktail['ingredients'])}\n")
    result_text.insert(tk.END, f"Дозировки: {', '.join(str(amount) for amount in random_cocktail['ingredients_amounts'])}\n")
    result_text.insert(tk.END, f"Инструкции: {', '.join(random_cocktail['recipe_steps'])}\n")

# Создание графического интерфейса
root = tk.Tk()
root.title("Коктейльный помощник")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

ingredients_var = tk.StringVar(value=ingredients_data["ingredients"])

label_ingredients = tk.Label(frame, text="Выберите ингредиенты:")
label_ingredients.grid(row=0, column=0, padx=5, pady=5)

# Создание выпадающего списка с множественным выбором
ingredients_listbox = tk.Listbox(frame, listvariable=ingredients_var, selectmode=tk.MULTIPLE, width=40, height=6)
ingredients_listbox.grid(row=0, column=1, padx=5, pady=5)

search_button = tk.Button(frame, text="Поиск коктейлей", command=find_cocktails)
search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

random_button = tk.Button(frame, text="Рандомный коктейль", command=random_cocktail)
random_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

result_text = tk.Text(frame, width=60, height=15, wrap=tk.WORD)
result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
