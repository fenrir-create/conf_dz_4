import struct

def read_binary_file(binary_path):
    instructions = []
    
    # Открываем бинарный файл для чтения
    with open(binary_path, 'rb') as bin_file:
        while True:
            # Читаем 4 байта (32 бита) — размер одной инструкции
            bytes_data = bin_file.read(4)
            if not bytes_data:
                break  # Конец файла
            
            # Распаковываем 4 байта в 32-битное число
            instruction = struct.unpack(">I", bytes_data)[0]
            instructions.append(instruction)
    
    return instructions

def decode_instructions(instructions):
    decoded = []
    for instr in instructions:
        # Извлекаем opcode
        opcode = (instr >> 26) & 0x3F  # opcode занимает старшие 6 бит
        if opcode == 26:  # LOAD_CONST
            B = (instr >> 12) & 0xFFF  # 12 бит для B
            C = instr & 0xFFF          # 12 бит для C
            decoded.append(f"LOAD_CONST B={B}, C={C}")
        elif opcode == 14:  # READ_MEM
            B = (instr >> 5) & 0x7FF    # 11 бит для B
            C = instr & 0x1FFFFF       # 21 бит для C
            decoded.append(f"READ_MEM B={B}, C={C}")
        elif opcode == 7:  # WRITE_MEM
            B = (instr >> 11) & 0x3F    # 6 бит для B
            C = (instr >> 5) & 0x3F     # 6 бит для C
            D = instr & 0x3F           # 6 бит для D
            decoded.append(f"WRITE_MEM B={B}, C={C}, D={D}")
        elif opcode == 6:  # UNARY_ABS
            B = (instr >> 12) & 0xFFF   # 12 бит для B
            C = instr & 0x7F           # 7 бит для C
            decoded.append(f"UNARY_ABS B={B}, C={C}")
        else:
            decoded.append(f"UNKNOWN_OPCODE {opcode}")
    
    return decoded

# Укажите путь к бинарному файлу
binary_path = "program.bin"

# Чтение и декодирование инструкций
instructions = read_binary_file(binary_path)
decoded = decode_instructions(instructions)

# Вывод инструкций в читаемом виде
for instr in decoded:
    print(instr)
