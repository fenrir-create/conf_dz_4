import struct
import csv




class Assembler:
    def __init__(self):
        self.instructions = {
            "LOAD_CONST": 26,
            "READ_MEM": 14,
            "WRITE_MEM": 7,
            "UNARY_ABS": 6
        }

    def assemble(self, source_path, binary_path, log_path):
        binary_data = []
        log_data = []

        with open(source_path, 'r') as src_file:
            for line in src_file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                cmd = parts[0]
                args = list(map(int, parts[1:]))

                if cmd == "LOAD_CONST":
                    opcode = self.instructions[cmd]
                    A, B, C = args
                    instruction = (opcode << 26) | (B << 12) | C
                    binary_data.append(instruction)
                    log_data.append({"cmd": cmd, "A": A, "B": B, "C": C})
                    print(A," ",B," ",C," ",instruction," ",binary_data)

                elif cmd == "READ_MEM":
                    opcode = self.instructions[cmd]
                    A, B, C = args
                    instruction = (opcode << 26) | (B << 5) | C
                    binary_data.append(instruction)
                    log_data.append({"cmd": cmd, "A": A, "B": B, "C": C})

                elif cmd == "WRITE_MEM":
                    opcode = self.instructions[cmd]
                    A, B, C, D = args
                    instruction = (opcode << 26) | (B << 11) | (C << 5) | D
                    binary_data.append(instruction)
                    log_data.append({"cmd": cmd, "A": A, "B": B, "C": C, "D": D})

                elif cmd == "UNARY_ABS":
                    opcode = self.instructions[cmd]
                    A, B, C = args
                    instruction = (opcode << 26) | (B << 12) | C
                    binary_data.append(instruction)
                    log_data.append({"cmd": cmd, "A": A, "B": B, "C": C})

        with open(binary_path, 'wb') as bin_file:
            for instr in binary_data:
                bin_file.write(struct.pack(">I", instr))

        with open(log_path, 'w', newline='') as log_file:
            writer = csv.DictWriter(log_file, fieldnames=["cmd", "A", "B", "C", "D"])
            writer.writeheader()
            for entry in log_data:
                writer.writerow(entry)

