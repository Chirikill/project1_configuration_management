from tkinter import *
import os


window = Tk() #создаем корневой объект - окно
window.title("VFS Emulator")
window.geometry("800x600")

"""Текущая рабочая директория"""
cwd = "/"
cwd = os.getcwd()


output_text = Text(window) #внутри указала родительское окно
output_text.pack(fill=BOTH, expand=True) # fill =both - чтобы белый квадрат располагался сверху, expand=True - растяжение по всему окну

 

"""Вывод текста в текстовое поле"""
def write_output(text):
    output_text.config(state='normal') #разблокируем поле
    output_text.insert(END, text + "\n") #Метод insert() в Python позволяет вставить элемент в список на указанную позицию. (end - вставить в конец)
    output_text.see(END) #прокручиваем вниз (end -  указывает на то, чтобы был виден конец текста)
    output_text.config(state='disabled') #заблокировали поле

write_output("Добро пожаловать в VFS Emulator. Введите команду ('exit' для выхода).")
write_output(f"Текущая директория: {cwd}")

"""Создаем фрейм для нижней части"""
bottom_frame = Frame(window) #создала фрейм
bottom_frame.pack(fill=BOTH)

#в фрейме будет расплагаться ввод данных
write_input = Entry(bottom_frame) 
write_input.pack(fill=BOTH)


#создадим парсинг команд. Здесь же будет раскрытие переменных окружения
def parse_command(cmd_str):
    expanded_cmd = os.path.expandvars(cmd_str)  # ← Python подставляет реальные значения из ОС
    parts = expanded_cmd.split() #Разбиваем на слова
        
    if not parts:
        return None, [], expanded_cmd
            
    command = parts[0] # Первое слово - команда
    args = parts[1:] # Остальные - аргументы
    return command, args, expanded_cmd


#функция для анализа команд
def analysis_command(entered):
    cmd_str = write_input.get()
    write_input.delete(0, END) #очистка поля ввода
    #Если вызвать delete() без параметров, то удалится только один символ - тот, который находится на позиции курсора 
    "команды могут состоять из нескольких составных частей. Поэтому команды надо разбивать - то есть парсировать"
    command, args, expanded_cmd = parse_command(cmd_str)

    # Выводим то, что ввел пользователь (с раскрытыми переменными)
    write_output(f"$ {expanded_cmd}")


    # Если пустая команда
    if not command:
        return

        # Обработка команд
    if command == "ls":
        write_output(f"Команда 'ls' вызвана с аргументами: {args}")
            
    elif command == "cd":
        if not args:
            write_output("Ошибка: команда 'cd' требует аргумент")
        else:
            write_output(f"Команда 'cd' вызвана с аргументом: {args[0]}")
                
    elif command == "exit":
        write_output("Выход из VFS Emulator...")
        window.after(1000, window.destroy)
            
    else:
         write_output(f"vfs: команда не найдена: {command}")
         write_output("Доступные команды: ls, cd, exit")

#привязываем enter к вводу польз
write_input.bind('<Return>', analysis_command)


window.mainloop() #для отображения окна                       