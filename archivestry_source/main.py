import os
from tkinter import filedialog, messagebox
import tkinter as tk

import archivator


def get_desktop_path():
    home = os.path.expanduser("~")  # Путь к домашней папке
    possible_names = ["Desktop", "Рабочий стол", "Bureau", "Escritorio", "桌面"]  # Возможные локализации

    # Проверяем все возможные названия папки
    for name in possible_names:
        desktop_path = os.path.join(home, name)
        if os.path.exists(desktop_path):
            return desktop_path

    # Если папка не найдена, возвращаем стандартный путь (на случай, если названия нет в списке)
    return os.path.join(home, "Desktop")



def select_folder(entry):
    folder_path = filedialog.askdirectory(initialdir=get_desktop_path())
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)
        entry.config(fg="black")


def select_file(entry):
    file_path = filedialog.askopenfilename(initialdir=get_desktop_path())
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        entry.config(fg="black")


class ArchiverApp:
    def __init__(self, root):
        self.root = root
        root.title("Архиватор")
        root.iconbitmap("logo.ico")

        # Поле "Выбор папки с архивируемыми файлами"
        tk.Label(root, text="Выбор папки с архивируемыми файлами:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.input_folder_entry = tk.Entry(root, width=50, fg="grey")
        self.input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Выбрать папку", command=lambda: select_folder(self.input_folder_entry)).grid(row=0,
                                                                                                           column=2,
                                                                                                           padx=10,
                                                                                                           pady=5)

        # Поле "Выбор папки для выгрузки"
        tk.Label(root, text="Выбор папки для выгрузки:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.output_folder_entry = tk.Entry(root, width=50, fg="grey")
        self.output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Выбрать папку", command=lambda: select_folder(self.output_folder_entry)).grid(row=1,
                                                                                                            column=2,
                                                                                                            padx=10,
                                                                                                            pady=5)

        # Чекбокс "Использовать пароль"
        self.use_password_var = tk.BooleanVar()
        password_check = tk.Checkbutton(root, text="Использовать пароль", variable=self.use_password_var)
        password_check.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(root, width=50, state="disabled", fg="grey")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        def toggle_password():
            if self.use_password_var.get():
                self.password_entry.config(state="normal")
            else:
                self.password_entry.config(state="disabled")

        password_check.config(command=toggle_password)

        # Чекбокс "Архивировать доп. файл"
        self.archive_file_var = tk.BooleanVar()
        file_check = tk.Checkbutton(root, text="Архивировать доп. файл", variable=self.archive_file_var)
        file_check.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.file_entry = tk.Entry(root, width=50, state="disabled", fg="grey")
        self.file_entry.grid(row=3, column=1, padx=10, pady=5)
        self.file_btn = tk.Button(root, text="Выбрать файл", state='disabled',
                                  command=lambda: select_file(self.file_entry))
        self.file_btn.grid(row=3, column=2, padx=10, pady=5)

        def toggle_file():
            if self.archive_file_var.get():
                self.file_entry.config(state="normal")
                self.file_btn.config(state="normal")
            else:
                self.file_entry.config(state="disabled")
                self.file_btn.config(state="disabled")

        file_check.config(command=toggle_file)

        # Кнопка "Архивировать"
        tk.Button(root, text="Архивировать", command=self.archive).grid(row=4, column=1, pady=20)

    def archive(self):
        # Логика для архивации
        try:
            # Пример: проверка заполненности полей
            input_folder = self.input_folder_entry.get()
            if not input_folder or not os.path.isdir(input_folder):
                raise ValueError("Укажите существующую папку с архивируемыми файлами.")

            # Проверка папки для выгрузки
            output_folder = self.output_folder_entry.get()
            if not output_folder:
                raise ValueError("Укажите существующую папку для выгрузки.")

            # Проверка использования пароля
            if self.use_password_var.get():
                password = self.password_entry.get()
                if not password:
                    raise ValueError("Вы выбрали использование пароля, но не ввели его.")

            # Проверка дополнительного файла
            if self.archive_file_var.get():
                additional_file = self.file_entry.get()
                if not additional_file or not os.path.isfile(additional_file):
                    raise ValueError("Вы выбрали архивирование дополнительного файла, но не указали его путь.")

            password = bytes(self.password_entry.get(), 'utf-8')
            archivator.archive_files(self.input_folder_entry.get(), self.output_folder_entry.get(),
                                     self.use_password_var.get(), password,
                                     self.archive_file_var.get(), self.file_entry.get())
            # Показываем сообщение об успехе
            messagebox.showinfo("Успех", "Успешно завершено")

        except Exception as e:
            # Показываем сообщение об ошибке
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ArchiverApp(root)
    root.mainloop()
