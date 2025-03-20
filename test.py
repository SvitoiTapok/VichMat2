import tkinter as tk
from tkinter import ttk

def show_fields(event):
    # Функция для отображения нужного набора полей
    selected_option = combobox.get()  # Получаем выбранное значение

    # Скрываем все поля
    for widget in field_set_1 + field_set_2:
        widget.pack_forget()

    # Отображаем нужный набор полей
    if selected_option == "Набор 1":
        for widget in field_set_1:
            widget.pack(pady=5)
    elif selected_option == "Набор 2":
        for widget in field_set_2:
            widget.pack(pady=5)

# Создаем главное окно
root = tk.Tk()
root.title("Переключение между наборами полей")

# Создаем выпадающий список для переключения между наборами полей
options = ["Набор 1", "Набор 2"]
combobox = ttk.Combobox(root, values=options)
combobox.set("Выберите набор полей")  # Устанавливаем текст по умолчанию
combobox.pack(pady=10)

# Привязываем обработчик события к изменению значения в combobox
combobox.bind("<<ComboboxSelected>>", show_fields)

# Создаем первый набор полей
field_set_1 = [
    tk.Label(root, text="Поле 1.1"),
    tk.Entry(root),
    tk.Label(root, text="Поле 1.2"),
    tk.Entry(root),
]

# Создаем второй набор полей
field_set_2 = [
    tk.Label(root, text="Поле 2.1"),
    tk.Entry(root),
    tk.Label(root, text="Поле 2.2"),
    tk.Entry(root),
    tk.Label(root, text="Поле 2.3"),
    tk.Entry(root),
]

# По умолчанию отображаем первый набор полей
for widget in field_set_1:
    widget.pack(pady=5)

# Запускаем главный цикл обработки событий
root.mainloop()