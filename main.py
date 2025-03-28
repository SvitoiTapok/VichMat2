import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
from numpy.lib.format import read_magic
from sympy.physics.units import action


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
        max_value = abs(func.subs(x, left))
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

def dihotomy_method(func, spfunc, left, right, accuracy):
    X = []
    Y = []
    i=0
    while True:
        i+=1
        cur_x = (left + right) / 2
        X.append(cur_x)
        f = func(cur_x)
        Y.append(f)
        lf = func(left)
        if f * lf < 0:
            right = cur_x
        else:
            left = cur_x
        if abs(f) < accuracy and abs(left - right) < accuracy:
            ax.plot(X, Y, marker='o')
            ax.plot([cur_x], [f],marker='o', color='red')
            canvas.draw()
            return [i, f, cur_x]


def Newton_method(func, spfunc, left, right, accuracy):
    X = []
    Y = []
    diff1 = sp.diff(spfunc, x)
    diff2 = sp.diff(diff1, x)
    try:
        if find_root_for_dif(diff1, left, right): raise Exception
        if find_root_for_dif(diff2, left, right): raise Exception
    except Exception as e:
        calc_err_label.config(text="Сообщение об ошибке: не удается определить корни методом Ньютона(производные меняют знак)")
        return 0
    if func(left) * diff2.subs(x, left) > 0:
        x0 = left

    else:
        x0 = right
    i = 0
    X.append(x0)
    Y.append(func(x0))
    while True:
        i += 1
        x1 = x0 - func(float(x0)) / diff1.subs(x, x0)
        X.append(x1.evalf())

        f = func(float(x1))
        Y.append(f)
        if abs(f) < accuracy and abs(x0 - x1) < accuracy:
            ax.plot(X, Y, marker='o')
            ax.plot([x1.evalf()], [f], marker='o', color='red')
            canvas.draw()
            return [i, f, x1.evalf()]
        x0 = x1


def Simple_iterations_method(func, spfunc, left, right, accuracy):
    X = []
    Y = []
    diff1 = sp.diff(spfunc, x)
    diff2 = sp.diff(diff1, x)
    try:
        if find_root_for_dif(diff1, left, right): raise Exception
        if find_root_for_dif(diff2, left, right):raise Exception
    except:
        calc_err_label.config(text="Сообщение об ошибке: не удается определить корни методом простой итерации(производные меняют знак)")
        return 0
    lamb = 1 / find_max_for_dif(diff1, left, right)
    print(lamb)
    print(diff2, diff2.subs(x, left), diff1.subs(x, left))
    if diff1.subs(x, left) > 0: lamb *= -1
    fi = lambda x: x + lamb * func(x)
    if func(left) * diff2.subs(x, left) > 0:
        x0 = left
    else:
        x0=right
    X.append(x0)
    Y.append(func(float(x0)))
    i = 0
    while True:
        i += 1
        x1 = fi(float(x0))
        X.append(x1.evalf())

        f = func(float(x1))
        Y.append(f)
        if abs(f) < accuracy and abs(x0 - x1) < accuracy:
            ax.plot(X, Y, marker='o')
            ax.plot([x1.evalf()], [f], marker='o', color='red')
            canvas.draw()
            return [i, f, x1.evalf()]
        x0 = x1
        if i>100:
            ax.plot(X, Y, marker='o')
            ax.plot([x1.evalf()], [f], marker='o', color='red')
            canvas.draw()
            calc_err_label.config(text="Сообщение об ошибке: не получилось получить решение системы")
            return 0

def Simple_iteration_sys_method(syst, first_funcsp, second_funcsp, x_min, x_max, y_min, y_max, accuracy):
    fi1_dx = sp.diff(first_funcsp, 'x')
    fi1_dy = sp.diff(first_funcsp, 'y')
    fi2_dx = sp.diff(second_funcsp, 'x')
    fi2_dy = sp.diff(second_funcsp, 'y')
    X = []
    Y = []
    print(fi1_dx, fi1_dy, fi2_dx, fi2_dy, first_funcsp, second_funcsp, sep="|")
    if(max(abs(find_max_for_dif2(fi1_dx, x_min, x_max, y_min, y_max))+abs(find_max_for_dif2(fi1_dy, y_min, y_max, x_min, x_max)),
           abs(find_max_for_dif2(fi2_dx, x_min, x_max, y_min, y_max))+abs(find_max_for_dif2(fi2_dy, y_min, y_max, x_min, x_max)))>1):
        calc_err_label1.config(text="Сообщение об ошибке: не удается определить корни методом простой итерации, не сходящийся алгоритм")
        return 0
    x0 = x_max
    y0 = y_max

    i=0
    while True:
        X.append(x0)
        Y.append(y0)
        i+=1
        try:
            print(x0, y0)
            x1 = syst(x0, y0)[0]+x0
            y1 = syst(x0, y0)[1]+y0
        except Exception as e:
            print(e)

            calc_err_label1.config(text="Сообщение об ошибке: не получилось получить решение системы")
            return 0
        if abs(x1-x0)<accuracy and abs(y1-y0)<accuracy:
            X.append(x1)
            Y.append(y1)
            ax1.plot(X, Y, marker='o')
            ax1.plot(X[-1], Y[-1], marker='o', color='red')
            canvas1.draw()
            return [i, syst(x1, y1), [x1, y1]]
        x0 = x1
        y0 = y1
        if i>100:
            calc_err_label1.config(text="Сообщение об ошибке: не получилось получить решение системы")
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
    return [0.1*x**2-x+0.2*y**2-0.3,
            0.2*x**2 - y + 0.1*x*y-0.7]
def syst2(x, y):
    return [np.log(y+2)-x,
            np.exp(-x)-y]
def syst3(x,y):
    return [(y+np.exp(-x))/3-x,
            (x**2+1)/4-y]

x, y = sp.symbols('x y')
func1sp = sp.sin(sp.exp(x) + x)
func2sp = x ** sp.sin(x) - 0.5 * x
func3sp = sp.atan(x) * sp.sin(x) * 9
func4sp = x ** 3 - 9 * x ** 2 + x + 11
func5sp = x ** 3 - x + 4
syst11fi = 0.1*x**2+0.2*y**2-0.3
syst12fi = 0.2*x**2 + 0.1*x*y-0.7
syst21fi = sp.log(y+2)
syst22fi = sp.exp(-x)
syst31fi = (y+sp.exp(-x))/3
syst32fi = (x**+2+1)/4






def draw_func():
    func = cur_func
    name = cur_func_name
    ax.clear()

    try:
        left, right = float(left_gran.get().replace(',', '.')), float(right_gran.get().replace(',', '.'))
        if left>=right:
            err_label.config(text="Сообщение об ошибке: левая граница больше правой")
            return 1
        x = np.linspace(left, right, 100)
        y = func(x)
    except:
        err_label.config(text="Сообщение об ошибке: некорректные значения границ")
        return 1
    ax.plot(x, y)
    ax.set_title(name)
    ax.grid( color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    canvas.draw()
    return 0

def calculate_root():
    if draw_func():
        return 1

    meth = cur_meth
    name = cur_meth_name
    func = cur_func
    left, right = float(left_gran.get().replace(',', '.')), float(right_gran.get().replace(',', '.'))
    c = find_root(func, left, right)
    if c>1:
        calc_err_label.config(text="Сообщение об ошибке: на интервале более одного корня")
        return 1
    if c==0:
        calc_err_label.config(text="Сообщение об ошибке: на интервале ни одного корня(нет пересечения оси OX)")
        return 1
    try:
        acc = float(accuracy.get().replace(',', '.'))
        if acc<=0: raise Exception
    except:
        calc_err_label.config(text="Сообщение об ошибке: некорректное значение точности")
        return 1
    calc_err_label.config(text="Сообщение об ошибке:")
    answ = meth(func, cur_sp_func, left, right, acc)

    if answ:
        root_label.config(text=f"Рассчитанный конень: {round(answ[2], 10)}")
        iter_label.config(text=f"Количество итераций: {answ[0]}")
        func_label.config(text=f"Значение в точке: {round(answ[1], 10)}")
        Info_label.config(text=f"Информация о выполнении({name})")
    else:
        return 1
    print(answ)


def draw_sys():
    sys = cur_sys
    name = cur_sys_name
    ax1.clear()

    try:
        lx, rx = float(left_granx.get().replace(',', '.')), float(right_granx.get().replace(',', '.'))
        ly, ry = float(left_grany.get().replace(',', '.')), float(right_grany.get().replace(',', '.'))
        if lx>=rx:
            err_label1.config(text="Сообщение об ошибке: левая граница больше правой")
            return 1
        if ly>=ry:
            err_label1.config(text="Сообщение об ошибке: верхняя граница больше нижней")
            return 1
        x = np.linspace(lx, rx, 500)
        y = np.linspace(ly, ry, 500)
    except:
        err_label.config(text="Сообщение об ошибке: некорректные значения границ")
        return 1
    X, Y = np.meshgrid(x, y)
    F = sys(X, Y)
    ax1.contour(X, Y, F[0], levels=[0], colors='blue')
    ax1.contour(X, Y, F[1], levels=[0], colors='red')
    ax1.set_title(name)
    ax1.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    canvas1.draw()
    return 0

def calculate_root_sys():
    if draw_sys():
        return 1
    sys = cur_sys
    lx, rx = float(left_granx.get().replace(',', '.')), float(right_granx.get().replace(',', '.'))
    ly, ry = float(left_grany.get().replace(',', '.')), float(right_grany.get().replace(',', '.'))
    try:
        acc = float(accuracy.get().replace(',', '.'))
        if acc<=0: raise Exception
    except:

        calc_err_label1.config(text="Сообщение об ошибке: некорректное значение точности")
        return 1
    calc_err_label.config(text="Сообщение об ошибке:")
    answ = Simple_iteration_sys_method(sys, cur_first_sys_func, cur_second_sys_func, lx, rx, ly, ry, acc)

    if answ:
        root_label1.config(text=f"Рассчитанный конень: x={round(answ[2][0], 10)}, y={round(answ[2][1], 10)}")
        iter_label1.config(text=f"Количество итераций: {answ[0]}")
        func_label1.config(text=f"Значение в точке: f1(x,y)={round(answ[1][0], 10)}, f2(x,y)={round(answ[1][1], 10)}")
    else:
        return 1
    print(answ)


def on_func_combobox_change(event):
    # Функция, которая вызывается при изменении значения в выпадающем списке
    global cur_func
    global cur_func_name
    global cur_sp_func
    selected_value = func_combobox.get()  # Получаем выбранное значение
    if selected_value=="sin(exp(x) + x)":
        cur_func=func1
        cur_sp_func = func1sp
    elif selected_value=="x ** sin(x) - 0.5 * x":
        cur_func=func2
        cur_sp_func = func2sp
    elif selected_value=="atan(x) * sin(x) * 9":
        cur_func=func3
        cur_sp_func = func3sp
    elif selected_value=="x ** 3 - 9 * x ** 2 + x + 11":
        cur_func=func4
        cur_sp_func = func4sp
    elif selected_value=="x ** 3 - x + 4":
        cur_func=func5
        cur_sp_func = func5sp
    cur_func_name = selected_value
    func_combobox_label.config(text=f"Вы выбрали: {selected_value}")  # Обновляем текст метки

def on_meth_combobox_change(event):
    global cur_meth
    global cur_meth_name
    selected_value = method_combobox.get()
    if selected_value=="Метод половинного деления":
        cur_meth=dihotomy_method
    elif selected_value=="Метод Ньютона":
        cur_meth=Newton_method
    elif selected_value=="Метод простой итерации":
        cur_meth=Simple_iterations_method
    cur_meth_name = selected_value
    method_combobox_label.config(text=f"Вы выбрали: {selected_value}")  # Обновляем текст метки

def on_sys_combobox_change(event):
    global cur_sys
    global cur_sys_name
    global cur_first_sys_func
    global cur_second_sys_func
    selected_value = sys_combobox.get()

    if selected_value=="0.1*x**2+x+0.2*y**2-0.3      0.2*x**2 + y + 0.1*x*y-0.7":
        cur_sys=syst1
        cur_first_sys_func = syst11fi
        cur_second_sys_func = syst12fi
    elif selected_value=="log(y + 2) - x      exp(-x) - y":
        cur_sys=syst2
        cur_first_sys_func = syst21fi
        cur_second_sys_func = syst22fi
    elif selected_value=="(y+np.exp(-x))/3-x      (x**2+1)/4-y":
        cur_sys=syst3
        cur_first_sys_func = syst31fi
        cur_second_sys_func = syst32fi
    cur_sys_name = selected_value
    sys_combobox_label.config(text=f"Вы выбрали: {selected_value}")

# def update_plot():
#     ax.clear()
#     x = np.linspace(0, 2 * np.pi, 100)
#     y = np.sin(x * float(frequency.get())) * float(amplitude.get())
#     ax.plot(x, y)
#     ax.set_title("График синуса")
#     canvas.draw()

def show_frame(frame):
    # Скрыть все фреймы
    for f in (frame_func, frame_sys):
        f.grid_forget()
    # Показать выбранный фрейм
    frame.grid(row=0, column=0, sticky="nsew")

cur_func=func1
cur_func_name="sin(exp(x) + x)"
cur_sp_func=func1sp
cur_meth=dihotomy_method
cur_meth_name="Метод половинного деления"
cur_sys=syst1
cur_sys_name="0.1*x**2+x+0.2*y**2-0.3\n0.2*x**2 + y + 0.1*x*y-0.7"
cur_first_sys_func=syst11fi
cur_second_sys_func=syst12fi
root = tk.Tk()
root.title("Динамическое построение графиков")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame_func = ttk.Frame(root)
frame_func.grid_rowconfigure(0, weight=1)
frame_func.grid_rowconfigure(1, weight=1)
frame_func.grid_rowconfigure(2, weight=1)
frame_func.grid_rowconfigure(3, weight=1)
frame_func.grid_rowconfigure(4, weight=1)
frame_func.grid_rowconfigure(5, weight=1)
frame_func.grid_rowconfigure(6, weight=1)
frame_func.grid_rowconfigure(7, weight=1)
frame_func.grid_rowconfigure(8, weight=1)
frame_func.grid_rowconfigure(9, weight=1)
frame_func.grid_rowconfigure(10, weight=1)
frame_func.grid_rowconfigure(11, weight=1)
frame_func.grid_columnconfigure(0, weight=1)
frame_func.grid_columnconfigure(1, weight=1)

frame_sys = ttk.Frame(root)
frame_sys.grid_rowconfigure(0, weight=1)
frame_sys.grid_rowconfigure(1, weight=1)
frame_sys.grid_rowconfigure(2, weight=1)
frame_sys.grid_rowconfigure(3, weight=1)
frame_sys.grid_rowconfigure(4, weight=1)
frame_sys.grid_rowconfigure(5, weight=1)
frame_sys.grid_rowconfigure(6, weight=1)
frame_sys.grid_rowconfigure(7, weight=1)
frame_sys.grid_rowconfigure(8, weight=1)
frame_sys.grid_rowconfigure(9, weight=1)
frame_sys.grid_rowconfigure(10, weight=1)
frame_sys.grid_rowconfigure(11, weight=1)
frame_sys.grid_rowconfigure(12, weight=1)
frame_sys.grid_rowconfigure(13, weight=1)
frame_sys.grid_columnconfigure(0, weight=1)
frame_sys.grid_columnconfigure(1, weight=1)

# Поле для ввода погрешности
accuracy_label = ttk.Label(frame_func, text="Точность:")
accuracy_label.grid(row=0,column=0, padx=10, pady=10,sticky="ew")
accuracy = ttk.Entry(frame_func)
accuracy.insert(0, "0.01")
accuracy.grid(row=0,column=1, padx=10, pady=10,sticky="ew")

# Поле для ввода отрезка
left_gran_label = ttk.Label(frame_func, text="левая граница:")
left_gran_label.grid(row=1,column=0, padx=10, pady=10,sticky="ew")
left_gran = ttk.Entry(frame_func)
left_gran.insert(0, "0.0")
left_gran.grid(row=1,column=1, padx=10, pady=10,sticky="ew")


right_gran_label = ttk.Label(frame_func, text="правая граница:")
right_gran_label.grid(row=2,column=0, padx=10, pady=10,sticky="ew")
right_gran = ttk.Entry(frame_func)
right_gran.insert(0, "1.0")
right_gran.grid(row=2,column=1, padx=10, pady=10,sticky="ew")

functions = ["sin(exp(x) + x)", "x ** sin(x) - 0.5 * x", "atan(x) * sin(x) * 9", "x ** 3 - 9 * x ** 2 + x + 11", "x ** 3 - x + 4"]
func_combobox = ttk.Combobox(frame_func, values=functions)
func_combobox.set("sin(exp(x) + x)")
#func_combobox.pack(pady=10)
func_combobox.bind("<<ComboboxSelected>>", on_func_combobox_change)
func_combobox.grid(row=3,column=0)

# какая функция выбрана
func_combobox_label = tk.Label(frame_func, text="Выберите вариант функции из списка")
func_combobox_label.grid(row=4,column=0)


fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=frame_func)
draw_button = ttk.Button(frame_func, text="Нарисовать график", command=draw_func)
err_label = ttk.Label(frame_func, text="Сообщение об ошибке:")
draw_button.grid(row=5, column=0, padx=10, pady=10,sticky="ew")
err_label.grid(row=6, column=0, padx=10, pady=10,sticky="ew")

methods = ["Метод половинного деления", "Метод Ньютона", "Метод простой итерации"]
method_combobox = ttk.Combobox(frame_func, values=methods)
method_combobox.set("Метод половинного деления")
#func_combobox.pack(pady=10)
method_combobox.bind("<<ComboboxSelected>>", on_meth_combobox_change)
method_combobox.grid(row=3,column=1)

# какой метод выбрана
method_combobox_label = tk.Label(frame_func, text="Выберите метод из списка")
method_combobox_label.grid(row=4,column=1)

calc_button = ttk.Button(frame_func, text="Расчитать корень", command=calculate_root)
calc_err_label = ttk.Label(frame_func, text="Сообщение об ошибке:")
calc_button.grid(row=5, column=1, padx=10, pady=10,sticky="ew")
calc_err_label.grid(row=6, column=1, padx=10, pady=10,sticky="ew")



switch_button_sys = ttk.Button(frame_func, text="Перейти к системам", command=lambda: show_frame(frame_sys))
switch_button_sys.grid(row=7, column=0, columnspan=2)
canvas.get_tk_widget().grid(row=8, column=0, columnspan=2)

Info_label = ttk.Label(frame_func, text="Информация о выполнении")
Info_label.grid(row=9, column=0, columnspan=2)

root_label = ttk.Label(frame_func, text="Рассчитанный конень:")
root_label.grid(row=10, column=0, padx=10, pady=10,sticky="ew")

iter_label = ttk.Label(frame_func, text="Количество итераций:")
iter_label.grid(row=10, column=1, padx=10, pady=10,sticky="ew")

func_label = ttk.Label(frame_func, text="Значение в точке:")
func_label.grid(row=11, column=0, columnspan=2)

#func_combobox_label.pack(pady=10)
################################################################################################################################################

accuracy_label = ttk.Label(frame_sys, text="Точность:")
accuracy_label.grid(row=0,column=0, padx=10, pady=10,sticky="ew")
accuracy1 = ttk.Entry(frame_sys)
accuracy1.insert(0, "0.01")
accuracy1.grid(row=0,column=1, padx=10, pady=10,sticky="ew")

# Поля для ввода отрезков
left_granx_label = ttk.Label(frame_sys, text="левая граница x:")
left_granx = ttk.Entry(frame_sys)
left_granx.grid(row=1,column=1, padx=10, pady=10,sticky="ew")
left_granx.insert(0, "0.0")
left_granx_label.grid(row=1,column=0, padx=10, pady=10,sticky="ew")


right_granx_label = ttk.Label(frame_sys, text="правая граница x:")
right_granx = ttk.Entry(frame_sys)
right_granx.insert(0, "1.0")
right_granx.grid(row=2,column=1, padx=10, pady=10,sticky="ew")
right_granx_label.grid(row=2,column=0, padx=10, pady=10,sticky="ew")


left_grany_label = ttk.Label(frame_sys, text="нижняя граница y:")
left_grany = ttk.Entry(frame_sys)
left_grany.grid(row=3,column=1, padx=10, pady=10,sticky="ew")
left_grany.insert(0, "0.0")
left_grany_label.grid(row=3,column=0, padx=10, pady=10,sticky="ew")


right_grany_label = ttk.Label(frame_sys, text="верхняя граница y:")
right_grany = ttk.Entry(frame_sys)
right_grany.insert(0, "1.0")
right_grany.grid(row=4,column=1, padx=10, pady=10, sticky="ew")
right_grany_label.grid(row=4,column=0, padx=10, pady=10, sticky="ew")



systems = ["0.1*x**2+x+0.2*y**2-0.3      0.2*x**2 + y + 0.1*x*y-0.7",
           "log(y + 2) - x      exp(-x) - y",
           "(y+np.exp(-x))/3-x      (x**2+1)/4-y"]
sys_combobox = ttk.Combobox(frame_sys, values=systems)
sys_combobox.set("0.1*x**2+x+0.2*y**2-0.3\n0.2*x**2 + y + 0.1*x*y-0.7")
sys_combobox.grid(row=5,column=0, padx=10, pady=10,sticky="ew")
sys_combobox.bind("<<ComboboxSelected>>", on_sys_combobox_change)


# какая система выбрана
sys_combobox_label = tk.Label(frame_sys, text="Выберите вариант системы из списка")
sys_combobox_label.grid(row=6,column=0, padx=10, pady=10,sticky="ew")






fig1, ax1 = plt.subplots()
canvas1 = FigureCanvasTkAgg(fig1, master=frame_sys)
draw_button1 = ttk.Button(frame_sys, text="Нарисовать множество точек", command=draw_sys)
err_label1 = ttk.Label(frame_sys, text="Сообщение об ошибке:")
draw_button1.grid(row=7, column=0, padx=10, pady=10,sticky="ew")
err_label1.grid(row=8, column=0, padx=10, pady=10,sticky="ew")
switch_button_func = ttk.Button(frame_sys,text="Перейти к функциям", command=lambda: show_frame(frame_func))
switch_button_func.grid(row=9,column=0, columnspan=2)
canvas1.get_tk_widget().grid(row=10, column=0, columnspan=2)

calc_button1 = ttk.Button(frame_sys, text="Расчитать корень", command=calculate_root_sys)
calc_err_label1 = ttk.Label(frame_sys, text="Сообщение об ошибке:")
calc_button1.grid(row=6, column=1, padx=10, pady=10,sticky="ew")
calc_err_label1.grid(row=7, column=1, padx=10, pady=10,sticky="ew")

Info_label1 = ttk.Label(frame_sys, text="Информация о выполнении")
Info_label1.grid(row=11, column=0, columnspan=2)

root_label1 = ttk.Label(frame_sys, text="Рассчитанный конень:")
root_label1.grid(row=12, column=0, padx=10, pady=10,sticky="ew")

iter_label1 = ttk.Label(frame_sys, text="Количество итераций:")
iter_label1.grid(row=12, column=1, padx=10, pady=10,sticky="ew")

func_label1 = ttk.Label(frame_sys, text="Значение в точке:")
func_label1.grid(row=13, column=0, columnspan=2)



# # Кнопка для обновления графика

# update_button.grid(row=2, column=0, columnspan=2, pady=10)

# Создание графика




#canvas.get_tk_widget().pack()
#field_set_1=[accuracy_label, accuracy, left_gran_label, left_gran, right_gran_label, right_gran, func_combobox, func_combobox_label, op_combobox, draw_button, canvas.get_tk_widget(), err_label]
#field_set_2=[accuracy_label, accuracy, left_granx_label, left_granx, rigth_granx_label, right_granx, left_grany_label, left_grany, right_grany_label, right_grany, sys_combobox, sys_combobox_label, op_combobox, canvas.get_tk_widget(), err_label]
#for widget in field_set_1:
#    widget.pack(pady=5)


# Инициализация графика
# update_plot()
show_frame(frame_func)
# Запуск основного цикла
root.mainloop()
