import struct
import csv

class Assembler:
    def __init__(self):
        # Маппинг для кодов команд
        self.instructions = {
            26: "LOAD_CONST",    # Код 26 для команды LOAD_CONST
            14: "READ_MEM",      # Код 14 для команды READ_MEM
            7: "WRITE_MEM",      # Код 7 для команды WRITE_MEM
            6: "UNARY_ABS"       # Код 6 для команды UNARY_ABS
        }

    def assemble(self, source_path, binary_path, log_path):
        binary_data = []
        log_data = []

        with open(source_path, 'r') as src_file:
            for line in src_file:
                line = line.strip()
                if not line:
                    continue

                parts = list(map(int, line.split()))  # Преобразуем числа в список
                opcode = parts[0]  # Первое число — это код команды (opcode)

                # Обработка команд в зависимости от количества параметров
                if opcode == 26:  # LOAD_CONST
                    if len(parts) != 4:
                        raise ValueError(f"Ошибка: команда LOAD_CONST требует 3 аргумента, но получено {len(parts) - 1}.")
                    A, B, C = parts[1:4]
                    instruction = (opcode << 26) | (B << 12) | C
                    binary_data.append(instruction)
                    log_data.append({"cmd": self.instructions[opcode], "A": A, "B": B, "C": C})

                elif opcode == 14:  # READ_MEM
                    if len(parts) != 3:
                        raise ValueError(f"Ошибка: команда READ_MEM требует 2 аргумента, но получено {len(parts) - 1}.")
                    B, C = parts[1:3]
                    instruction = (opcode << 27) | (B << 5) | C
                    binary_data.append(instruction)
                    log_data.append({"cmd": self.instructions[opcode], "B": B, "C": C})

                elif opcode == 7:  # WRITE_MEM
                    if len(parts) != 4:
                        raise ValueError(f"Ошибка: команда WRITE_MEM требует 3 аргумента, но получено {len(parts) - 1}.")
                    B, C, D = parts[1:4]
                    instruction = (opcode << 27) | (B << 11) | (C << 5) | D
                    binary_data.append(instruction)
                    log_data.append({"cmd": self.instructions[opcode], "B": B, "C": C, "D": D})

                elif opcode == 6:  # UNARY_ABS
                    if len(parts) != 3:
                        raise ValueError(f"Ошибка: команда UNARY_ABS требует 2 аргумента, но получено {len(parts) - 1}.")
                    B, C = parts[1:3]
                    instruction = (opcode << 29) | (B << 12) | C
                    binary_data.append(instruction)
                    log_data.append({"cmd": self.instructions[opcode], "B": B, "C": C})

                else:
                    raise ValueError(f"Неизвестный opcode: {opcode}")

        # Запись бинарных данных в файл
        with open(binary_path, 'wb') as bin_file:
            for instr in binary_data:
                bin_file.write(struct.pack(">I", instr))

        # Запись лога в CSV файл
        with open(log_path, 'w', newline='') as log_file:
            writer = csv.DictWriter(log_file, fieldnames=["cmd", "A", "B", "C", "D"])
            writer.writeheader()
            for entry in log_data:
                writer.writerow(entry)
