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
