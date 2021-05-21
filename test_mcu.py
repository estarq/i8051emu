import mcu


class TestMicrocontroller:
    def test_load_hex_file(self):
        m = mcu.Microcontroller()
        m.load_hex_file('test.hex')
        assert m._rom[0] == 2, 'First byte not loaded'
        assert m._rom[1] == 1, 'Second byte not loaded'
        assert m._rom[256] == 174, 'Misplaced byte - addr change due to ORG statement ignored'


class TestOperation:
    def test__len__(self):
        op = mcu.Operation(2)
        assert len(op) == 3, 'Wrong length - op has one two-byte long arg'

    def test__str__(self):
        op = mcu.Operation(16, 1, 2)
        assert str(op) == 'JBC 1h, 2h', 'Wrong representation - args switched?'

        op = mcu.Operation(36, 10)
        assert str(op) == 'ADD A, #10', 'Wrong representation - hexadecimal value?'

        op = mcu.Operation(18, 171, 205)
        assert op.args == (171, 205), 'Wrong args - merged?'
        assert str(op) == 'LCALL ABCDh', 'Wrong representation - miscalculated value?'
