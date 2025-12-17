from tkinter import *
import os
import sys


# === Глобальные переменные ===
vfs_root = os.getcwd()  
startup_script = None
vfs_cwd = "/"
window = None
output_text = None
write_input = None


def parse_program_args():
    """
    Обрабатывает: --vfs-path ПУТЬ и --startup-script ПУТЬ
    """
    global vfs_root, startup_script
    
    args = sys.argv[1:] 
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        # --vfs-path /some/path
        if arg == "--vfs-path" and i + 1 < len(args):
            vfs_root = os.path.abspath(args[i + 1])
            i += 2  # Пропускаем сам аргумент и его значение
            
        elif arg == "--startup-script" and i + 1 < len(args):
            startup_script = os.path.abspath(args[i + 1])
            i += 2
            
        # через =
        elif arg.startswith("--vfs-path="):
            vfs_root = os.path.abspath(arg.split("=", 1)[1])
            i += 1
            
        elif arg.startswith("--startup-script="):
            startup_script = os.path.abspath(arg.split("=", 1)[1])
            i += 1
            
        # Неизвестный аргумент
        else:
            print(f"Предупреждение: неизвестный аргумент '{arg}', игнорирую")
            i += 1
    
 


def write_output(text):
    """Вывод текста в текстовое поле"""
    output_text.config(state='normal')
    output_text.insert(END, text + "\n")
    output_text.see(END)
    output_text.config(state='disabled')


def parse_user_command(cmd_str):
    """
    Парсинг команд, которые вводит пользователь
    Раскрывает переменные окружения ($HOME, $PATH и т.д.)
    """
    # Раскрытие переменных окружения
    expanded_cmd = os.path.expandvars(cmd_str)
    parts = expanded_cmd.split()
    
    if not parts:
        return None, [], expanded_cmd
    
    command = parts[0]
    args = parts[1:]
    return command, args, expanded_cmd


def execute_command(command, args):
    """Выполнение команды эмулятора"""
    global vfs_cwd
    
    if command == "ls":
        write_output(f"Команда 'ls' вызвана с аргументами: {args}")
        
        
    elif command == "cd":
        if not args:
            write_output("Ошибка: команда 'cd' требует аргумент")
        else:
            vfs_cwd = args[0]
            write_output(f"Команда 'cd' вызвана с аргументами: {args}")
            
    elif command == "exit":
        write_output("Выход из VFS Emulator...")
        window.after(1000, window.destroy)
        
    else:
        write_output(f"vfs: команда не найдена: {command}")
        write_output("Доступные команды: ls, cd, exit")


def analysis_command(event):
    """Обработка ввода пользователя"""
    cmd_str = write_input.get()
    write_input.delete(0, END)
    
    if not cmd_str.strip():
        return
    
    # Парсим команду
    command, args, expanded_cmd = parse_user_command(cmd_str)
    
    # Выводим то, что ввел пользователь
    write_output(f"$ {expanded_cmd}")
    
    if command:
        execute_command(command, args)


def run_startup_script():
    """Выполнение стартового скрипта"""
    global startup_script
    
    if not startup_script:
        return
    
    write_output(f"\nВыполнение стартового скрипта...")
    
    try:
        with open(startup_script, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        line_number = 0
        for line in lines:
            line_number += 1
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            # Имитируем ввод команды
            write_output(f"$ {line}")
            window.update()
            window.after(200)  # Пауза для наглядности
            
            # Парсим и выполняем команду
            command, args, _ = parse_user_command(line)
            if command:
                execute_command(command, args)
            else:
                write_output(f"[Строка {line_number}] Пустая команда, пропускаю")
            
            window.update()
        
        
    except FileNotFoundError:
        write_output(f"ОШИБКА: файл скрипта не найден: {startup_script}")
    except Exception as e:
        write_output(f"ОШИБКА при выполнении скрипта: {e}")


def init_gui():
    """Инициализация графического интерфейса"""
    global window, output_text, write_input
    
    window = Tk()
    window.title("VFS Emulator")
    window.geometry("800x600")
    
    
    # Основное поле вывода
    output_text = Text(window)
    output_text.pack(fill=BOTH, expand=True)
    
    # Фрейм для ввода
    bottom_frame = Frame(window)
    bottom_frame.pack(fill=BOTH, side=BOTTOM)
    
    # Поле ввода
    write_input = Entry(bottom_frame)
    write_input.pack(fill=BOTH, side=LEFT, expand=True)
    
    # Кнопка
    Button(bottom_frame, text="Выполнить", 
           command=lambda: analysis_command(None)).pack(side=RIGHT)
    
    # Привязка Enter
    write_input.bind('<Return>', analysis_command)
    
    
    write_output("Добро пожаловать в VFS Emulator")
    write_output("Введите команду ('exit' для выхода):")
    write_output("")
    

    if startup_script:
        window.after(500, run_startup_script)


def main():
    """Главная функция"""
    parse_program_args()
    
    init_gui()
    
    window.mainloop()


if __name__ == "__main__":
    main()
