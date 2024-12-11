import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import simpledialog, messagebox


class Charge:
    def __init__(self, q, x, y):
        self.q = q
        self.x = x
        self.y = y


class EquipotentialApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Визуализация эквипотенциальных линий")

        # Список зарядов
        self.charges = []

        # Настройка интерфейса
        self.setup_ui()

        # Построить график при запуске
        self.plot_initial_graph()

    def setup_ui(self):
        # Кнопки
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(side=tk.TOP, pady=10)

        add_charge_btn = tk.Button(btn_frame, text="Добавить заряд", command=self.add_charge)
        add_charge_btn.pack(side=tk.LEFT, padx=5)

        plot_btn = tk.Button(btn_frame, text="Построить потенциал", command=self.plot_potential)
        plot_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(btn_frame, text="Очистить заряды", command=self.clear_charges)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Поле для отображения зарядов
        self.charge_list = tk.Listbox(self.master, height=5)
        self.charge_list.pack(fill=tk.X, padx=10)

        # Полотно для графика
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_charge(self):
        # Диалог для ввода параметров заряда
        try:
            q = float(simpledialog.askstring("Ввод", "Введите величину заряда (q):", parent=self.master))
            x = float(simpledialog.askstring("Ввод", "Введите координату X:", parent=self.master))
            y = float(simpledialog.askstring("Ввод", "Введите координату Y:", parent=self.master))
            charge = Charge(q, x, y)
            self.charges.append(charge)
            self.charge_list.insert(tk.END, f"q={q} @ ({x}, {y})")
        except (TypeError, ValueError):
            messagebox.showerror("Ошибка", "Некорректный ввод. Пожалуйста, введите числовые значения.")

    def clear_charges(self):
        self.charges.clear()
        self.charge_list.delete(0, tk.END)
        self.ax.clear()
        self.plot_initial_graph()

    def plot_initial_graph(self):
        # Построить пустую область графика с фиксированным масштабом
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_title("Эквипотенциальные линии системы точечных зарядов")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.canvas.draw()

    def plot_potential(self):
        if not self.charges:
            messagebox.showwarning("Предупреждение", "Нет зарядов для отображения.")
            return

        # Создание сетки
        x = np.linspace(-10, 10, 500)
        y = np.linspace(-10, 10, 500)
        X, Y = np.meshgrid(x, y)

        # Вычисление потенциала
        V = np.zeros_like(X)
        epsilon0 = 1  # Для упрощения единиц

        for charge in self.charges:
            r = np.sqrt((X - charge.x)**2 + (Y - charge.y)**2)
            r[r == 0] = 1e-9  # Избежание деления на 0
            V += charge.q / r

        # Ограничение потенциала для улучшения визуализации
        V = np.clip(V, -100, 100)

        # Очистка предыдущего графика
        self.ax.clear()

        # Построение изолиний потенциала
        levels = np.linspace(-50, 50, 100)
        contours = self.ax.contour(X, Y, V, levels=levels, cmap='Blues')
        self.ax.set_title("Эквипотенциальные линии системы точечных зарядов")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_aspect('equal')

        # Фиксация масштаба
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        # Отображение зарядов
        for charge in self.charges:
            color = 'r' if charge.q > 0 else 'b'
            self.ax.plot(charge.x, charge.y, marker='o', color=color, markersize=10)
            self.ax.text(charge.x, charge.y, f" q={charge.q}", color='k', fontsize=9, ha='left')

        self.ax.grid(True)
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = EquipotentialApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
