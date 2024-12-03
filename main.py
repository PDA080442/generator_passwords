import tkinter as tk
from tkinter import messagebox
from generator.password_generator import PasswordGenerator
import os
import json


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор сложных паролей")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # История паролей
        self.password_history = []
        self.history_file = "password_history.json"
        self.load_history()

        # Создаём интерфейс генерации паролей
        self.create_password_ui()

    def create_password_ui(self):
        """Интерфейс для генерации паролей"""
        self.clear_window()

        tk.Label(self.root, text="Генератор паролей", font=("Arial", 14)).pack(pady=10)

        # Поле для выбора длины пароля
        tk.Label(self.root, text="Длина пароля:").pack()
        self.length_entry = tk.Entry(self.root, width=10)
        self.length_entry.insert(0, "12")
        self.length_entry.pack(pady=5)

        # Чекбоксы для выбора параметров
        self.use_digits = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Цифры", variable=self.use_digits).pack(anchor="w")
        tk.Checkbutton(self.root, text="Заглавные буквы", variable=self.use_uppercase).pack(anchor="w")
        tk.Checkbutton(self.root, text="Строчные буквы", variable=self.use_lowercase).pack(anchor="w")
        tk.Checkbutton(self.root, text="Специальные символы", variable=self.use_special).pack(anchor="w")

        # Кнопка для генерации
        tk.Button(self.root, text="Сгенерировать пароль", command=self.generate_password).pack(pady=10)

        # Поле для отображения сгенерированного пароля
        self.password_output = tk.Entry(self.root, width=30, state="readonly")
        self.password_output.pack(pady=5)

        tk.Button(self.root, text="Копировать пароль", command=self.copy_password).pack(pady=5)
        tk.Button(self.root, text="Просмотреть историю", command=self.show_history).pack(pady=5)

    def clear_window(self):
        """Удалить все элементы интерфейса с окна"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_password(self):
        """Логика генерации пароля"""
        try:
            length = int(self.length_entry.get())
            password = PasswordGenerator.generate(
                length=length,
                use_digits=self.use_digits.get(),
                use_uppercase=self.use_uppercase.get(),
                use_lowercase=self.use_lowercase.get(),
                use_special=self.use_special.get(),
            )
            self.password_output.config(state="normal")
            self.password_output.delete(0, tk.END)
            self.password_output.insert(0, password)
            self.password_output.config(state="readonly")

            # Добавляем пароль в историю
            self.password_history.append(password)
            self.save_history()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def copy_password(self):
        """Копировать сгенерированный пароль в буфер обмена"""
        password = self.password_output.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()
            messagebox.showinfo("Копирование", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Копирование", "Нет пароля для копирования.")

    def load_history(self):
        """Загрузить историю паролей из файла"""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                try:
                    self.password_history = json.load(file)
                except json.JSONDecodeError:
                    self.password_history = []
        else:
            self.password_history = []

    def save_history(self):
        """Сохранить историю паролей в файл"""
        with open(self.history_file, "w") as file:
            json.dump(self.password_history, file, indent=4)

    def show_history(self):
        """Показать историю сгенерированных паролей"""
        history_window = tk.Toplevel(self.root)
        history_window.title("История паролей")
        history_window.geometry("400x300")
        history_window.resizable(False, False)

        if not self.password_history:
            tk.Label(history_window, text="История пуста", font=("Arial", 12)).pack(pady=10)
            return

        tk.Label(history_window, text="История сгенерированных паролей:", font=("Arial", 12)).pack(pady=10)
        history_listbox = tk.Listbox(history_window, width=50, height=15)
        history_listbox.pack(pady=10)

        # Добавляем пароли в список
        for idx, password in enumerate(self.password_history, start=1):
            history_listbox.insert(tk.END, f"{idx}. {password}")

        def clear_history():
            """Очистить историю"""
            self.password_history.clear()
            self.save_history()
            history_listbox.delete(0, tk.END)
            tk.Label(history_window, text="История очищена.", font=("Arial", 12)).pack(pady=10)

        # Кнопки для управления историей
        tk.Button(history_window, text="Очистить историю", command=clear_history).pack(pady=5)
        tk.Button(history_window, text="Закрыть", command=history_window.destroy).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
