import mcu


class TestMicrocontroller:
    def test_load_hex_file(self):
        m = mcu.Microcontroller()
        m.load_hex_file('test.hex')
        assert m._rom[0] == 2, 'First byte not loaded'
        assert m._rom[1] == 1, 'Second byte not loaded'
        assert m._rom[256] == 174, 'Misplaced byte - addr change due to ORG statement ignored'

    def test_pc_prop(self):
        m = mcu.Microcontroller()
        m.pc = 65538
        assert m.pc == 2, 'Overflow not supported - int?'


class TestByte:
    def test__getitem__(self):
        b = mcu.Byte()
        b.value = 4
        assert b[5] == 1, 'Bit access not supported'

    def test__setitem__(self):
        b = mcu.Byte()
        b[2] = 1
        assert b == 32, 'Bit setting not supported'

    def test__setattr__(self):
        b = mcu.Byte()
        b.value = 260
        assert b == 4, 'Overflow not supported'
        b.value = -2
        assert b == 254, 'Underflow not supported'

    def test__add__(self):
        b = mcu.Byte()
        b.value = 4
        b += 1
        assert b == 5

    def test__sub__(self):
        b = mcu.Byte()
        b.value = 4
        b -= 1
        assert b == 3

    def test__mod__(self):
        b = mcu.Byte()
        b.value = 9
        assert b % 2 == 1

    def test__divmod__(self):
        b1 = mcu.Byte()
        b1.value = 9
        b2 = mcu.Byte()
        b2.value = 2
        assert divmod(b1, b2) == (4, 1)


class TestDoubleByte:
    def test__getitem__(self):
        b = mcu.DoubleByte()
        b.value = 2048
        assert b[4] == 1, 'Bit access not supported'

    def test__setitem__(self):
        b = mcu.DoubleByte()
        b[5] = 1
        assert b == 1024, 'Bit setting not supported'

    def test__setattr__(self):
        b = mcu.DoubleByte()
        b.value = 65538
        assert b == 2, 'Overflow not supported'
        b.value = -4
        assert b == 65532, 'Underflow not supported'


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
