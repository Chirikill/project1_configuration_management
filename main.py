import tkinter as tk 
import os
from tkinter import scrolledtext


''' Пояснение к коду:
 Это эмулятор виртуальной файловой системы (vfs) с графическим интерфейсом. 
Программа имитирует работу командной строки, где пользователь может вводить команды и получать ответы.

1)tkinter - библиотека для создания графического интерфейса
os - для работы с операционной системой (раскрытия переменных окружения)

 Переменные окружения - это динамические именованные значения, которые хранят информацию о среде выполнения операционной системы. Примеры:

 $HOME - путь к домашней директории пользователя
 $USER - имя текущего пользователя
 $PATH - список путей для поиска исполняемых файлов

 Как это работает технически

 Получение переменных из ОС: Python через модуль os получает доступ к реальным переменным окружения вашей системы
 Поиск и замена: Функция ищет в строке символ $ и заменяет последующее имя переменной на её значение

2)В конструкторе класса создаем заголовок и размер окна. (title, geometry)

3)Запоминаем текущую рабочую директорию (cwd)

4)создаем поле для вывода текста (output.text)

5)создаем фрейм (bottom_frame)
 Frame - это невидимый контейнер для группировки других элементов интерфейса

6)создаем метку $ и приглашение ввода (левой кнопкой мыши)

7)Создаем поле для ввода команд

8)создаем приветственное сообщение и показ текущей директории

9)создаем метод для вывода текста (write_output)
 важно: чтобы поле текста блокировалось, чтобы пользователь не мог редактировать

10)создаем метод "парсер команд"
 Парсинг - это процесс анализа текста и разбиения его на составные части по определённым правилам
 os.path.expandvars(cmd_str) - раскрывает $HOME → /home/user

11) Метод process_command() - обработчик команд

12)добавляем обработку конкретных команд

13)запускаем программу(Создаем главное окно; создаем приложение; запускаем главный цикл)
 

'''


class VFSEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("VFS Emulator")
        self.root.geometry("800x600")
        self.cwd = "/"
        
        # Текущая директория
        self.cwd = os.getcwd()
        
        # Создаем текстовое поле с прокруткой
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=30, width=100, font=("Courier", 10))
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Фрейм для нижней части (организация элементов)
        bottom_frame = tk.Frame(root) # Создаем фрейм
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10)) # Размещаем его

        # Метка с приглашением ввода "$ "
        self.prompt_label = tk.Label(bottom_frame, text="$ ", font=("Courier", 10))
        self.prompt_label.pack(side=tk.LEFT)

        # Поле для ввода команд
        self.input_entry = tk.Entry(bottom_frame, width=100, font=("Courier", 10))
        self.input_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.input_entry.bind('<Return>', self.process_command)
        self.input_entry.focus_set()

        # Приветственное сообщение
        self.write_output("Добро пожаловать в VFS Emulator. Введите команду ('exit' для выхода).")
        self.write_output(f"Текущая директория: {self.cwd}")

    def write_output(self, text):
        """Вывод текста в текстовое поле"""
        self.output_text.configure(state='normal')  #  Разблокируем поле
        self.output_text.insert(tk.END, text + "\n") #  Добавляем текст
        self.output_text.see(tk.END) #  Прокручиваем вниз
        self.output_text.configure(state='disabled') #  Блокируем поле

    def parse_command(self, cmd_str):
        """Парсинг команды с раскрытием переменных окружения"""
        # Раскрываем переменные окружения
        expanded_cmd = os.path.expandvars(cmd_str)
        parts = expanded_cmd.split() #Разбиваем на слова
        
        if not parts:
            return None, [], expanded_cmd
            
        command = parts[0] # Первое слово - команда
        args = parts[1:] # Остальные - аргументы
        return command, args, expanded_cmd

    def process_command(self, event):
        """Обработка введенной команды"""
        # Получаем команду
        cmd_str = self.input_entry.get()  # Берем текст из поля
        self.input_entry.delete(0, tk.END) # Очищаем поле
        
        # Парсим команду
        command, args, expanded_cmd = self.parse_command(cmd_str)
        
        # Выводим то, что ввел пользователь (с раскрытыми переменными)
        self.write_output(f"$ {expanded_cmd}")

        # Если пустая команда
        if not command:
            return

        # Обработка команд
        if command == "ls":
            self.write_output(f"Команда 'ls' вызвана с аргументами: {args}")
            
        elif command == "cd":
            if not args:
                self.write_output("Ошибка: команда 'cd' требует аргумент")
            else:
                self.write_output(f"Команда 'cd' вызвана с аргументом: {args[0]}")
                
        elif command == "exit":
            self.write_output("Выход из VFS Emulator...")
            self.root.after(1000, self.root.destroy)
            
        else:
            self.write_output(f"vfs: команда не найдена: {command}")
            self.write_output("Доступные команды: ls, cd, exit")

if __name__ == "__main__":
    root = tk.Tk()
    app = VFSEmulator(root)
    root.mainloop()