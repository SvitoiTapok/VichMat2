import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np

# Функция для обновления графика
def update_plot():
    ax.clear()  # Очищаем предыдущий график
    x = np.linspace(0, 10, 100)
    y = np.sin(np.exp(x) + float(scale.get())) # Динамически изменяем график
    ax.plot(x, y, label=f"sin(exp(x) + {scale.get()}")
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_title("Динамический график")
    ax.set_xlabel("Ось X")
    ax.set_ylabel("Ось Y")
    ax.legend()
    canvas.draw_idle()  # Обновляем график

# Создаем главное окно Tkinter
root = tk.Tk()
root.title("Динамический график с сеткой")

# Создаем фигуру и оси
fig, ax = plt.subplots()

# Создаем холст для встраивания графика в Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Добавляем слайдер для изменения параметра
scale = ttk.Scale(root, from_=-5, to=5, orient="horizontal", command=lambda _: update_plot())
scale.set(0)  # Начальное значение
scale.pack()

# Первоначальная отрисовка графика
update_plot()

# Запуск главного цикла Tkinter
root.mainloop()