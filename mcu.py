import disassembler


class Microcontroller:
    def __init__(self):
        self._rom = ROM()

    def load_hex_file(self, filepath):
        for record in disassembler.IntelHexFile(filepath):
            for addr, byte in enumerate(record, record.first_byte_addr):
                self._rom[addr] = byte


class ROM:
    def __init__(self):
        self._data = [0] * 4000  # 4 KB

    def __getitem__(self, addr):
        return self._data[addr]

    def __setitem__(self, addr, value: int):
        self._data[addr] = value
