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

    def test_direct_addressing(self):
        m = mcu.Microcontroller()
        byte_id = id(m._mem[17])
        m._mem[17] = 123
        assert m._mem[17] == 123 and id(m._mem[17]) == byte_id, 'Byte replaced with int?'
        m._mem[17][7] = 0
        assert m._mem[17] == 122, 'Bit setting not supported'

    def test_register_addressing(self):
        m = mcu.Microcontroller()
        m._mem.selected_register_bank = 3
        byte_id = id(m._mem[8 * m._mem.selected_register_bank + 1])
        m._mem.r1 = 200
        assert m._mem.r1 == 200, 'R1 property not supported'
        assert m._mem[8 * 3 + 1] == 200, 'Address not calculated properly'
        assert id(m._mem[8 * 3 + 1]) == byte_id, 'Value not changed in place'

    def test_mem_prop_bit_access(self):
        m = mcu.Microcontroller()
        m._mem.a = 8
        assert m._mem[224] == 8, 'Property not aliased properly'
        assert m._mem[224][4] == 1
        assert m._mem.a[4] == 1, 'Bit access on property not supported'
        m._mem.a[5] = 1
        assert m._mem.a == 12, 'Bit setting on property not supported'

    def test_mem_val_overflow(self):
        m = mcu.Microcontroller()
        m._mem[30] += 300
        assert m._mem[30] == 44, 'Overflow not supported'

    def test_exec_2(self):
        m = mcu.Microcontroller()
        m._exec_2(171, 205)
        assert m.pc == 43981

    def test_exec_4(self):
        m = mcu.Microcontroller()
        m._exec_4()
        assert m._mem.a == 1

    def test_exec_5(self):
        m = mcu.Microcontroller()
        m._mem[23] = 15
        m._exec_5(23)
        assert m._mem[23] == 16

    def test_exec_6(self):
        m = mcu.Microcontroller()
        m._mem.r0 = 17
        m._mem[m._mem.r0] = 100
        m._exec_6()
        assert m._mem[m._mem.r0] == 101

    def test_exec_8(self):
        m = mcu.Microcontroller()
        m._exec_8()
        m._exec_8()
        assert m._mem.r0 == 2

    def test_exec_20(self):
        m = mcu.Microcontroller()
        m._exec_20()
        assert m._mem.a == 255

    def test_exec_21(self):
        m = mcu.Microcontroller()
        m._mem[23] = 15
        m._exec_21(23)
        assert m._mem[23] == 14

    def test_exec_23(self):
        m = mcu.Microcontroller()
        m._mem.r1 = 17
        m._mem[m._mem.r1] = 100
        m._exec_23()
        assert m._mem[m._mem.r1] == 99

    def test_exec_26(self):
        m = mcu.Microcontroller()
        m._exec_26()
        assert m._mem.r2 == 255

    def test_exec_36(self):
        m = mcu.Microcontroller()
        m._mem.a = 10
        m._exec_36(20)
        assert m._mem.a == 30

    def test_exec_37(self):
        m = mcu.Microcontroller()
        m._mem.a = 10
        m._mem[15] = 40
        m._exec_37(15)
        assert m._mem.a == 50

    def test_exec_38(self):
        m = mcu.Microcontroller()
        m._mem.a = 30
        m._mem.r0 = 100
        m._mem[m._mem.r0] = 25
        m._exec_38()
        assert m._mem.a == 55

    def test_exec_44(self):
        m = mcu.Microcontroller()
        m._mem.a = 50
        m._mem.r4 = 5
        m._exec_44()
        assert m._mem.a == 55

    def test_exec_52(self):
        m = mcu.Microcontroller()
        m._mem.a = 10
        m._mem.c = 1
        m._exec_52(20)
        assert m._mem.a == 31

    def test_exec_53(self):
        m = mcu.Microcontroller()
        m._mem.a = 10
        m._mem.c = 1
        m._mem[15] = 40
        m._exec_53(15)
        assert m._mem.a == 51


class TestDataMemory:
    def test_decimal_access(self):
        mem = mcu.DataMemory()
        byte_id = id(mem[2])
        mem[2] = 30
        assert mem[2] == 30 and id(mem[2]) == byte_id, 'Decimal access not supported'
        b = mcu.Byte()
        b.value = 3
        mem[b] = 30
        assert mem[3] == 30, 'Cannot use a Byte instance as an address - not converted to int?'

    def test_bit_access(self):
        mem = mcu.DataMemory()
        mem[5][1] = 1
        assert mem[5] == 64, 'Bit access not supported'

    def test_dptr(self):
        mem = mcu.DataMemory()
        mem.dptr = 65530
        mem.dptr += 10
        assert mem.dptr == 4, 'Overflow not supported - int?'
        mem.dptr = 65530
        assert mem[130] == int('1' * 8, 2) and mem[131] == int('11111010', 2), 'Wrong binary representation'

    def test_psw_prop(self):
        mem = mcu.DataMemory()
        mem.psw[0] = 1
        assert mem.psw == 128

    def test_c_prop(self):
        mem = mcu.DataMemory()
        mem.c = 1
        assert mem.c == 1
        assert mem[208][0] == 1

    def test_ac_prop(self):
        mem = mcu.DataMemory()
        mem.ac = 1
        assert mem.ac == 1
        assert mem[208][1] == 1

    def test_rs1_prop(self):
        mem = mcu.DataMemory()
        mem.rs1 = 1
        assert mem.rs1 == 1
        assert mem[208][3] == 1

    def test_rs2_prop(self):
        mem = mcu.DataMemory()
        mem.rs2 = 1
        assert mem.rs2 == 1
        assert mem[208][4] == 1

    def test_ov_prop(self):
        mem = mcu.DataMemory()
        mem.ov = 1
        assert mem.ov == 1
        assert mem[208][5] == 1

    def test_p_prop(self):
        mem = mcu.DataMemory()
        mem.p = 1
        assert mem.p == 1
        assert mem[208][7] == 1

    def test_selected_register_bank_prop(self):
        mem = mcu.DataMemory()
        mem.selected_register_bank = 3
        assert mem.selected_register_bank == 3 and mem.rs1 == 1 and mem.rs2 == 1

    def test_r1_prop(self):
        mem = mcu.DataMemory()
        mem.selected_register_bank = 2
        mem.r1 = 3
        assert mem.r1 == 3 and mem[8 * 2 + 1] == 3


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
        b2 = mcu.Byte()
        b2.value = 3
        assert b + b2 == 8

    def test__radd__(self):
        b = mcu.Byte()
        b.value = 4
        assert 5 + b == 9

    def test__sub__(self):
        b = mcu.Byte()
        b.value = 4
        b -= 1
        assert b == 3
        b2 = mcu.Byte()
        b2.value = 2
        assert b - b2 == 1

    def test__rsub__(self):
        b = mcu.Byte()
        b.value = 5
        assert 20 - b == 15

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
