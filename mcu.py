class Microcontroller:
    def __init__(self):
        self._rom = ROM()


class ROM:
    def __init__(self):
        self._data = [0] * 4000  # 4 KB

    def __getitem__(self, addr):
        return self._data[addr]

    def __setitem__(self, addr, value: int):
        self._data[addr] = value
