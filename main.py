import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Функция для обновления графика
def update_plot():
    ax.clear()
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x * float(frequency.get())) * float(amplitude.get())
    ax.plot(x, y)
    ax.set_title("График синуса")
    canvas.draw()

# Создание основного окна
root = tk.Tk()
root.title("Динамическое построение графиков")

# Создание фрейма для параметров
frame = ttk.Frame(root)
frame.pack(pady=10)

# Поле для ввода амплитуды
ttk.Label(frame, text="Амплитуда:").grid(row=11, column=0, padx=5, pady=50)
amplitude = ttk.Entry(frame)
amplitude.insert(0, "1.0")
amplitude.grid(row=0, column=1, padx=5, pady=5)

# Поле для ввода частоты
ttk.Label(frame, text="Частота:").grid(row=1, column=0, padx=5, pady=5)
frequency = ttk.Entry(frame)
frequency.insert(0, "1.0")
frequency.grid(row=1, column=1, padx=5, pady=5)

# Кнопка для обновления графика
update_button = ttk.Button(frame, text="Обновить график", command=update_plot)
update_button.grid(row=2, column=0, columnspan=2, pady=10)

# Создание графика
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Инициализация графика
update_plot()

# Запуск основного цикла
root.mainloop()