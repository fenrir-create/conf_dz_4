import struct
import csv

# class Interpreter:
#     def __init__(self, memory_size=1024):
#         self.memory = [0] * memory_size
#         self.registers = [0] * 16

#     def interpret(self, binary_path, result_path, memory_range):
#         with open(binary_path, 'rb') as bin_file:
#             binary_data = []
#             while byte := bin_file.read(4):
#                 instruction = struct.unpack(">I", byte)[0]
#                 binary_data.append(instruction)

#         for instruction in binary_data:
#             opcode = (instruction >> 26) & 0x3F

#             if opcode == 26:
#                 B = (instruction >> 12) & 0xFFF
#                 C = instruction & 0xFFF
#                 self.registers[B] = C

#             elif opcode == 14:
#                 B = (instruction >> 5) & 0x1FFFFF
#                 C = instruction & 0x1F
#                 self.registers[B] = self.memory[self.registers[C]]

#             elif opcode == 7:
#                 B = (instruction >> 11) & 0x3F
#                 C = (instruction >> 5) & 0x3F
#                 D = instruction & 0x1F
#                 self.memory[self.registers[D] + C] = self.registers[B]

#             elif opcode == 6:
#                 B = (instruction >> 12) & 0xFFF
#                 C = instruction & 0xFFF
#                 self.registers[B] = abs(self.registers[C])

#         mem_start, mem_end = memory_range
#         with open(result_path, 'w', newline='') as result_file:
#             writer = csv.writer(result_file)
#             writer.writerow(["Address", "Value"])
#             for addr in range(mem_start, mem_end + 1):
#                 writer.writerow([addr, self.memory[addr]])
class Interpreter:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size
        self.registers = [0] * 16  # 16 регистров, с индексами от 0 до 15

    def interpret(self, binary_path, result_path, memory_range):
        with open(binary_path, 'rb') as bin_file:
            binary_data = []
            while byte := bin_file.read(4):
                instruction = struct.unpack(">I", byte)[0]
                binary_data.append(instruction)

        for instruction in binary_data:
            opcode = (instruction >> 26) & 0x3F
            print(opcode)
            if opcode == 26:  # LOAD_CONST
                B = (instruction >> 12) & 0xFFF
                print(B)
                C = instruction & 0xFFF
                print(B," ",C)

                # Проверка границ индекса
                if B < len(self.registers):
                    self.registers[B] = C
                    print(self.registers[B])
                else:
                    raise IndexError(f"26 Индекс регистра B={B} выходит за пределы 0..15")

            elif opcode == 14:  # READ_MEM
                B = (instruction >> 5) & 0x1FFFFF
                C = instruction & 0x5F
                print(B," ",C)
                if B < len(self.registers) and C < len(self.registers):
                    self.registers[B] = self.memory[self.registers[C]]
                else:
                    raise IndexError(f"14 Индексы регистров B={B}, C={C} выходят за пределы 0..15")

            elif opcode == 7:  # WRITE_MEM
                B = (instruction >> 11) & 0x3F
                C = (instruction >> 5) & 0x6FE
                D = instruction & 0xFF
                print(B," ",C," ",D)
                if B < len(self.registers) and D < len(self.registers):
                    address = self.registers[D] + C
                    if 0 <= address < len(self.memory):
                        self.memory[address] = self.registers[B]
                    else:
                        raise IndexError(f"7 Адрес памяти {address} выходит за пределы 0..{len(self.memory) - 1}")
                else:
                    raise IndexError(f"7 Индексы регистров B={B}, D={D} выходят за пределы 0..15")

            elif opcode == 6:  # UNARY_ABS
                B = (instruction >> 12) & 0xFFF
                C = instruction & 0xFFF
                print(B," ",C)
                if B < len(self.registers) and C < len(self.registers):
                    self.registers[B] = abs(self.registers[C])
                else:
                    raise IndexError(f"6 Индексы регистров B={B}, C={C} выходят за пределы 0..15")

        # for i in self.registers:
        #     print(self.registers[i])
        mem_start, mem_end = memory_range
        with open(result_path, 'w', newline='') as result_file:
            writer = csv.writer(result_file)
            writer.writerow(["Address", "Value"])
            for addr in range(mem_start, mem_end + 1):
                writer.writerow([addr, self.memory[addr]])
                # writer.writerow([addr, self.registers[addr]])
