import disassembler


def test_disassemble():
    file_content = ':03000000020100FA\n:10010000AE00783879307420F37400F2C29674200F\n:00000001FF\n'
    test_output = list(disassembler.disassemble(file_content))
    correct_output = [
        (0, 3, 2, [1, 0], 'LJMP 100h'),
        (256, 2, 174, [0], 'MOV R6, 0h'),
        (258, 2, 120, [56], 'MOV R0, #56'),
        (260, 2, 121, [48], 'MOV R1, #48'),
        (262, 2, 116, [32], 'MOV A, #32'),
        (264, 1, 243, (), 'MOVX @R1, A'),
        (265, 2, 116, [0], 'MOV A, #0'),
        (267, 1, 242, (), 'MOVX @R0, A'),
        (268, 2, 194, [150], 'CLR 96h'),
        (270, 2, 116, [32], 'MOV A, #32')]
    assert test_output == correct_output


class TestIntelHexFile:
    def test_loading_a_file(self):
        file_content = ':03000000020100FA\n:10010000AE00783879307420F37400F2C29674200F\n:00000001FF\n'
        i = disassembler.IntelHexFile(file_content)
        assert i._records[0].first_byte_addr == 0
        assert i._records[0]._data == '020100'
        assert i._records[1].first_byte_addr == 256
        assert i._records[1]._data == 'AE00783879307420F37400F2C2967420'


class TestRecord:
    def test__init__(self):
        r = disassembler.Record(':10010000AE00783879307420F37400F2C29674200F')
        assert r.first_byte_addr == 256
        assert r._data == 'AE00783879307420F37400F2C2967420'

    def test__iter__(self):
        r = disassembler.Record(':10010000AE00783879307420F37400F2C29674200F')
        assert list(r) == [174, 0, 120, 56, 121, 48, 116, 32, 243, 116, 0, 242, 194, 150, 116, 32]
