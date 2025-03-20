import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
from numpy.lib.format import read_magic


def find_root(func, left, right):
    n = 1000000
    step = (right - left) / n
    root_count = 0
    prex = func(left)
    for i in range(n):
        left += step
        lf = func(left)
        if prex * lf < 0:
            root_count += 1
        prex = lf
    return root_count


def find_root_for_dif(func, left, right):
    n = 1000
    step = (right - left) / n
    root_count = 0
    prex = func.subs(x, left)
    for i in range(n):
        left += step
        lf = func.subs(x, left)
        if prex * lf < 0:
            root_count += 1
        prex = lf
    return root_count


def find_max_for_dif(func, left, right):
    n = 1000
    step = (right - left) / n
    max_value = 0
    for i in range(n):
        lf = func.subs(x, left).evalf()
        if abs(lf) > max_value:
            max_value = lf
        left += step
    if abs(func.subs(x, left)) > max_value:
        max_value = func.subs(x, left)
    return max_value

def find_max_for_dif2(func, x_min, x_max, y_min, y_max):
    n1 = 50
    n2 = 50
    stepv = (y_max-y_min)/n2
    steph = (x_max-x_min)/n1
    y_perv = y_min
    max_value = 0
    for i in range(n1):
        for j in range(n2):
            lf = func.subs({x: x_min, y: y_min})
            if abs(lf) > max_value:
                max_value = lf
            y_min+=stepv
        x_min+=steph
        y_min = y_perv
    if abs(func.subs({x: x_min, y: y_min})) > max_value:
        max_value = func.subs({x: x_min, y: y_min})
    print(func, " : ", max_value)
    return max_value

def dihotomy_method(func, left, right, accuracy):
    n = int(np.ceil(np.log2(abs(right - left) / accuracy))) + 1
    for i in range(1, n + 1):
        cur_x = (left + right) / 2
        f = func(cur_x)
        lf = func(cur_x)
        if f * lf < 0:
            right = cur_x
        else:
            left = cur_x
        if abs(f) < accuracy and abs(left - right) < accuracy:
            return [i, f, cur_x]
    return [n, f, cur_x]


def Newton_method(func, spfunc, left, right, accuracy):
    diff1 = sp.diff(spfunc, x)
    diff2 = sp.diff(diff1, x)
    try:
        if find_root_for_dif(diff1, left, right): raise Exception
        if find_root_for_dif(diff2, left, right): raise Exception
    except Exception as e:
        print("не удается определить корни методом Ньютона")
        return 0
    if func(left) * diff2.subs(x, left) > 0:
        x0 = left
    else:
        x0 = right
    i = 0
    while True:
        i += 1
        x1 = x0 - func(x0) / diff1.subs(x, x0)
        print(x1.evalf())
        f = func(x1)
        if abs(f) < accuracy and abs(x0 - x1) < accuracy:
            return [i, f.evalf(), x1.evalf()]
        x0 = x1


def Simple_iterations_method(func, spfunc, left, right, accuracy):
    diff1 = sp.diff(spfunc, x)
    diff2 = sp.diff(diff1, x)
    try:
        if find_root_for_dif(diff1, left, right): raise Exception
        if find_root_for_dif(diff2, left, right):raise Exception
    except:
        print("не удается определить корни методом простой итерации")
        return 0
    lamb = 1 / find_max_for_dif(diff1, left, right)
    if diff1.subs(x, left) > 0: lamb *= -1
    fi = lambda x: x + lamb * func(x)
    if func(left) * diff2.subs(x, left) > 0:
        x0 = left
    else:
        x0=right
    i = 0
    while True:
        i += 1
        x1 = fi(x0)
        print(x1.evalf())
        f = func(x1)
        if abs(f) < accuracy and abs(x0 - x1) < accuracy:
            return [i, f.evalf(), x1.evalf()]
        x0 = x1

def Simple_iteration_sys_method(syst, first_funcsp, second_funcsp, x_min, x_max, y_min, y_max, accuracy):
    fi1_dx = sp.diff(first_funcsp, 'x')
    fi1_dy = sp.diff(first_funcsp, 'y')
    fi2_dx = sp.diff(second_funcsp, 'x')
    fi2_dy = sp.diff(second_funcsp, 'y')
    print(fi1_dx, fi1_dy, fi2_dx, fi2_dy, first_funcsp, second_funcsp, sep="|")
    if(max(abs(find_max_for_dif2(fi1_dx, x_min, x_max, y_min, y_max))+abs(find_max_for_dif2(fi1_dy, y_min, y_max, x_min, x_max)),
           abs(find_max_for_dif2(fi2_dx, x_min, x_max, y_min, y_max))+abs(find_max_for_dif2(fi2_dy, y_min, y_max, x_min, x_max)))>1):
        print("не удается определить корни методом простой итерации, не сходящийся алгоритм")
        return 0
    x0 = x_max
    y0 = y_max
    i=0
    while True:
        try:
            x1 = -syst(x0, y0)[0]+x0
            y1 = -syst(x0, y0)[1]+y0
        except Exception:
            print("не получилось получить решение системы")
            return 0
        if abs(x1-x0)<accuracy and abs(y1-y0)<accuracy:
            return [i, syst(x1, y1), [x1, y1]]
        x0 = x1
        y0 = y1
        if i>100:
            print("не получилось получить решение системы")
            return 0



def func1(x):
    return np.sin(np.exp(x) + x)


def func2(x):
    return x ** np.sin(x) - 0.5 * x


def func3(x):
    return np.arctan(x) * np.sin(x) * 9


def func4(x):
    return x ** 3 - 9 * x ** 2 + x + 11


def func5(x):
    return x ** 3 - x + 4


def syst1(x,y):
    return [0.1*x**2+x+0.2*y**2-0.3,
            0.2*x**2 + y + 0.1*x*y-0.7]
def syst2(x, y):
    return [x**2+y**3+x-y,
            np.tan(x*y)-2+y]
def syst3(x,y):
    return [x**y-3+x,
            np.arctan(x)*y-2*x**2+y]

x, y = sp.symbols('x y')
func1sp = sp.sin(sp.exp(x) + x)
func2sp = x ** sp.sin(x) - 0.5 * x
func3sp = sp.atan(x) * sp.sin(x) * 9
func4sp = x ** 3 - 9 * x ** 2 + x + 11
func5sp = x ** 3 - x + 4
syst11fi = -(0.1*x**2+0.2*y**2-0.3)
syst12fi = -(0.2*x**2 + 0.1*x*y-0.7)
syst21fi = -(x**2+y**3-y)
syst22fi = -(sp.tan(x*y)-2)
syst31fi = -(x**y-3)
syst32fi = -(sp.atan(x)*y-2*x**2)


# print(dihotomy_method(func1, 1, 1.8, 0.001))
# print(Newton_method(func5, func5sp, -2, -1, 0.01))
# print(find_root(func4, -5, 10))
# print(Simple_iterations_method(func5, func5sp, -2, -1, 0.01))
# print(Simple_iteration_sys_method(syst1, syst11fi, syst12fi, 0, 1, 0, 1, 0.01))



def draw_func():
    func = cur_func
    name = cur_func_name
    print(cur_func_name)
    ax.clear()
    try:
        x = np.linspace(float(left_gran.get()), float(right_gran.get()), 100)
        y = func(x)
    except:
        err_label.config(text="Сообщение об ошибке: некорректные значения границ")
        return 1
    ax.plot(x, y)
    ax.set_title(name)
    canvas.draw()
    return 0

def on_func_combobox_change(event):
    # Функция, которая вызывается при изменении значения в выпадающем списке
    global cur_func
    global cur_func_name
    selected_value = func_combobox.get()  # Получаем выбранное значение
    if selected_value=="sin(exp(x) + x)":
        cur_func=func1
    elif selected_value=="x ** sin(x) - 0.5 * x":
        cur_func=func2
    elif selected_value=="atan(x) * sin(x) * 9":
        cur_func=func3
    elif selected_value=="x ** 3 - 9 * x ** 2 + x + 11":
        cur_func=func4
    elif selected_value=="x ** 3 - x + 4":
        cur_func=func5
    cur_func_name = selected_value
    func_combobox_label.config(text=f"Вы выбрали: {selected_value}")  # Обновляем текст метки

def on_sys_combobox_change(event):
    selected_value = sys_combobox.get()
    if selected_value=="0.1*x**2+x+0.2*y**2-0.3\n0.2*x**2 + y + 0.1*x*y-0.7":
        cur_func=syst1
    elif selected_value=="x**2+y**3+x-y\ntan(x*y)-2+y":
        cur_func=syst2
    elif selected_value=="x**y-3+x\narctan(x)*y-2*x**2+y":
        cur_func=syst3
    sys_combobox_label.config(text=f"Вы выбрали: {selected_value}")

# def update_plot():
#     ax.clear()
#     x = np.linspace(0, 2 * np.pi, 100)
#     y = np.sin(x * float(frequency.get())) * float(amplitude.get())
#     ax.plot(x, y)
#     ax.set_title("График синуса")
#     canvas.draw()

def show_fields(event):
    selected_option = op_combobox.get()

    # Скрываем все поля
    for widget in field_set_1 + field_set_2:
        widget.pack_forget()

    # Отображаем нужный набор полей
    if selected_option == "функции":
        for widget in field_set_1:
            widget.pack(pady=3)
    elif selected_option == "системы":
        for widget in field_set_2:
            widget.pack(pady=5)
cur_func=func1
cur_func_name="sin(exp(x) + x)"
cur_sys=syst1
root = tk.Tk()
root.title("Динамическое построение графиков")

frame = ttk.Frame(root)
frame.pack(pady=10)

# Поле для ввода погрешности
accuracy_label = ttk.Label(frame, text="Точность:")
accuracy = ttk.Entry(frame)
accuracy.insert(0, "0.01")

# Поле для ввода отрезка
left_gran_label = ttk.Label(frame, text="левая граница:")
left_gran = ttk.Entry(frame)
left_gran.insert(0, "0.0")


right_gran_label = ttk.Label(frame, text="правая граница:")
right_gran = ttk.Entry(frame)
right_gran.insert(0, "1.0")

functions = ["sin(exp(x) + x)", "x ** sin(x) - 0.5 * x", "atan(x) * sin(x) * 9", "x ** 3 - 9 * x ** 2 + x + 11", "x ** 3 - x + 4"]
func_combobox = ttk.Combobox(frame, values=functions)
func_combobox.set("sin(exp(x) + x)")
#func_combobox.pack(pady=10)
func_combobox.bind("<<ComboboxSelected>>", on_func_combobox_change)

# какая функция выбрана
func_combobox_label = tk.Label(frame, text="Выберите вариант функции из списка")
#func_combobox_label.pack(pady=10)
################################################################################################################################################


# Поля для ввода отрезков
left_granx_label = ttk.Label(frame, text="левая граница x:")
left_granx = ttk.Entry(frame)
left_granx.insert(0, "0.0")


rigth_granx_label = ttk.Label(frame, text="правая граница x:")
right_granx = ttk.Entry(frame)
right_granx.insert(0, "1.0")


left_grany_label = ttk.Label(frame, text="нижняя граница y:")
left_grany = ttk.Entry(frame)
left_grany.insert(0, "0.0")


right_grany_label = ttk.Label(frame, text="верхняя граница y:")
right_grany = ttk.Entry(frame)
right_grany.insert(0, "1.0")


systems = ["0.1*x**2+x+0.2*y**2-0.3\n0.2*x**2 + y + 0.1*x*y-0.7",
           "x**2+y**3+x-y\ntan(x*y)-2+y",
           "x**y-3+x\narctan(x)*y-2*x**2+y"]
sys_combobox = ttk.Combobox(frame, values=systems)
sys_combobox.set("sin(exp(x) + x)")
#sys_combobox.pack(pady=10)
sys_combobox.bind("<<ComboboxSelected>>", on_sys_combobox_change)

# какая функция выбрана
sys_combobox_label = tk.Label(frame, text="Выберите вариант системы из списка")
#sys_combobox_label.pack(pady=10)


opt = ["функции", "системы"]
op_combobox = ttk.Combobox(root, values=opt)
op_combobox.set("функции")
op_combobox.pack(pady=10)
op_combobox.bind("<<ComboboxSelected>>", show_fields)




# # Кнопка для обновления графика

# update_button.grid(row=2, column=0, columnspan=2, pady=10)

# Создание графика
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
draw_button = ttk.Button(frame, text="Нарисовать график", command=draw_func)
err_label = ttk.Label(frame, text="Сообщение об ошибке:")
#canvas.get_tk_widget().pack()
field_set_1=[accuracy_label, accuracy, left_gran_label, left_gran, right_gran_label, right_gran, func_combobox, func_combobox_label, op_combobox, draw_button, canvas.get_tk_widget(), err_label]
field_set_2=[accuracy_label, accuracy, left_granx_label, left_granx, rigth_granx_label, right_granx, left_grany_label, left_grany, right_grany_label, right_grany, sys_combobox, sys_combobox_label, op_combobox, canvas.get_tk_widget(), err_label]
for widget in field_set_1:
    widget.pack(pady=5)


# Инициализация графика
# update_plot()

# Запуск основного цикла
root.mainloop()
