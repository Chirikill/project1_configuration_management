#!/bin/bash
echo "=== Тестирование базовых параметров эмулятора ==="

echo  "==Вызов без параметров"
python3 main.py
echo ""

echo "==Вызов с параметром 'Путь к физическому расположению VFS'"
echo "вызов осуществляется двумя способами:"
echo "1. python3 main.py --vfs-path='путь к физическому расположению VFS'"
echo "2. python3 main.py --vfs-path 'путь к физическому расположению VFS'"
python3 main.py --vfs-path="/home/user/my_vfs"

echo "==Вызов с параметром 'Путь к стартовому скрипту'"
echo "вызов осуществляется двумя способами:"
echo "1. python3 main.py --startup-script=название стартового скрипта"
echo "2. python3 main.py --startup-script название стартового скрипта"
python3 main.py --startup-script=init.vfs