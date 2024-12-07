import os
from assembler import Assembler
from interpreter import Interpreter

# Шаг 1: Параметры для запуска
source_program_path = "code.txt"  # Файл с текстовым описанием программы
binary_program_path = "program.bin"        # Файл для хранения бинарного кода
log_file_path = "program_log.csv"          # Лог файл для ассемблера
result_file_path = "program_result.csv"    # Результат работы интерпретатора
memory_range = (0, 1000)                     # Диапазон памяти для сохранения результата

# Шаг 2: Ассемблирование программы
print("Ассемблирование программы...")
assembler = Assembler()
assembler.assemble(source_program_path, binary_program_path, log_file_path)
print(f"Бинарный файл создан: {binary_program_path}")
print(f"Лог-файл создан: {log_file_path}")

# Шаг 3: Интерпретация бинарного файла
print("Интерпретация программы...")
interpreter = Interpreter()
interpreter.interpret(binary_program_path, result_file_path, memory_range)
print(f"Результат выполнения программы сохранён: {result_file_path}")
