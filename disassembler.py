import mcu


class IntelHexFile:
    def __init__(self, filepath):
        with open(filepath) as file:
            # [:-1] to skip the trailing EOF Record
            self._records = [Record(line.rstrip()) for line in list(file)[:-1]]

    def __iter__(self):
        for record in self._records:
            yield record


class Record:
    def __init__(self, line):
        self.first_byte_addr = int(line[3:7], 16)
        self._data = line[9:-2]

    def __iter__(self):
        # Every two consecutive hexadecimal digits (ASCII) represent a byte of data
        for idx in range(0, len(self._data), 2):
            yield int(self._data[idx:idx + 2], 16)


def disassemble(filepath):
    # Disassemble a file having in mind that arguments may not be in the same record as an opcode
    getting_opcode = True
    for record in IntelHexFile(filepath):
        # If a record starts with an opcode, an ORG statement may have changed its address
        if getting_opcode:
            addr = record.first_byte_addr
        for byte in record:
            if getting_opcode:
                op = mcu.Operation(byte)
                if len(op) == 1:
                    yield addr, len(op), op.opcode, op.args, str(op)
                    addr += len(op)
                    continue
                getting_opcode = False
                args = []
            else:
                if len(args) < len(op) - 1:
                    args.append(byte)
                    if len(args) == len(op) - 1:
                        op.args = args
                        yield addr, len(op), op.opcode, op.args, str(op)
                        getting_opcode = True
                        addr += len(op)
