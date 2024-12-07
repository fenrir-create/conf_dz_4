import struct
import csv

class Interpreter:
    def __init__(self):
        self.instructions = {
            26: "LOAD_CONST",    # Код 26 для команды LOAD_CONST
            14: "READ_MEM",      # Код 14 для команды READ_MEM
            7: "WRITE_MEM",      # Код 7 для команды WRITE_MEM
            6: "UNARY_ABS"       # Код 6 для команды UNARY_ABS
        }
        self.registers = [0] * 16  # 16 регистров

    def interpret(self, binary_program_path, result_file_path, memory_range):
        with open(binary_program_path, 'rb') as bin_file:
            program = bin_file.read()

        i = 0
        while i < len(program):
            # Читаем 4 байта (одну инструкцию)
            instruction = struct.unpack(">I", program[i:i+4])[0]
            i += 4

            # Извлекаем opcode и параметры в зависимости от типа команды
            opcode = (instruction >> 26) & 0x3F
            if opcode == 26:  # LOAD_CONST
                B = (instruction >> 12) & 0xFFF
                C = instruction & 0xFFF
                self.load_const(B, C)

            elif opcode == 14:  # READ_MEM
                B = (instruction >> 5) & 0x7FF
                C = instruction & 0x1F
                self.read_mem(B, C)

            elif opcode == 7:  # WRITE_MEM
                B = (instruction >> 11) & 0x3F
                C = (instruction >> 5) & 0x3F
                D = instruction & 0x3F
                self.write_mem(B, C, D)

            elif opcode == 6:  # UNARY_ABS
                B = (instruction >> 12) & 0xFFF
                C = instruction & 0x7F
                self.unary_abs(B, C)

            else:
                raise ValueError(f"Неизвестный opcode: {opcode}")

        # Результаты работы программы записываем в файл
        with open(result_file_path, 'w') as result_file:
            for i, reg in enumerate(self.registers):
                result_file.write(f"R{i}: {reg}\n")

    def load_const(self, B, C):
        """Загружает константу в регистр B."""
        self.registers[B] = C

    def read_mem(self, B, C):
        """Чтение из памяти (симуляция)."""
        # Допустим, память в интерпретаторе - это просто массив
        if C < len(self.memory_range):
            self.registers[B] = self.memory_range[C]
        else:
            raise IndexError(f"Обращение к несуществующей ячейке памяти {C}")

    def write_mem(self, B, C, D):
        """Запись в память (симуляция)."""
        if D < len(self.memory_range):
            self.memory_range[D] = self.registers[B]
        else:
            raise IndexError(f"Запись в несуществующую ячейку памяти {D}")

    def unary_abs(self, B, C):
        """Вычисление абсолютного значения и запись в регистр B."""
        self.registers[B] = abs(self.registers[C])
