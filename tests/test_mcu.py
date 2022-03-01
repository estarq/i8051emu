import mcu


class TestMicrocontroller:
    def test_load_hex_file(self):
        m = mcu.Microcontroller()
        m.load_hex_file('tests/test.hex')
        assert m._rom[0] == 2, 'First byte not loaded'
        assert m._rom[1] == 1, 'Second byte not loaded'
        assert m._rom[256] == 174, 'Misplaced byte - addr change due to ORG statement ignored'

    def test_reset_rom(self):
        m = mcu.Microcontroller()
        m._rom[100] = 123
        m.mem.a = 20
        m.reset_rom()
        assert m._rom[100] == 0 and m.mem.a == 0

    def test_next_cycle__parity_flag(self):
        m = mcu.Microcontroller()
        m._rom[0] = 0  # NOP
        m._rom[1] = 0
        m.mem.a = 0b101
        m.next_cycle()
        assert m.mem.p == 1
        m.mem.a = 0b100
        m.next_cycle()
        assert m.mem.p == 0

    def test_next_cycle__int0_level_activated(self):
        m = mcu.Microcontroller()
        m.mem.it0 = 0
        m.mem.int0 = 0
        m._rom[0] = 0  # NOP
        m.next_cycle()
        assert m.mem.ie0 == 1

    def test_next_cycle__int0_edge_triggered(self):
        m = mcu.Microcontroller()
        m.mem.it0 = 1
        m._rom[0] = 0  # NOP
        m._rom[1] = 0
        m.mem.int0 = 1
        m.next_cycle()
        m.mem.int0 = 0
        m.next_cycle()
        assert m.mem.ie0 == 1

    def test_next_cycle__interrupt(self):
        m = mcu.Microcontroller()
        m.pc = 123
        m.mem.ea = 1

        # INT0 (low priority)
        m.mem.ie0 = 1
        m.mem.ex0 = 1
        m._rom[3] = 4  # INC A
        m._rom[4] = 50  # RETI

        # T1 (high priority)
        m.mem.tf1 = 1
        m.mem.et1 = 1
        m.mem.pt1 = 1
        # ADD A, #4
        m._rom[27] = 36
        m._rom[28] = 4
        # ADD A, #5
        m._rom[29] = 36
        m._rom[30] = 5
        # ADD A, #6
        m._rom[31] = 36
        m._rom[32] = 6
        # RETI
        m._rom[33] = 50

        m.next_cycle()  # ADD A, #4
        m.next_cycle()  # ADD A, #5
        assert m.mem.a == 9

        m.mem.tf1 = 1

        # T0 (high priority)
        m.mem.tf0 = 1
        m.mem.et0 = 1
        m.mem.pt0 = 1
        m._rom[11] = 20  # DEC A
        m._rom[12] = 50  # RETI

        m.next_cycle()  # DEC A
        m.next_cycle()  # RETI
        assert m.mem.a == 8

        m.next_cycle()  # ADD A, #6
        m.next_cycle()  # RETI
        assert m.mem.a == 14

        m.next_cycle()  # ADD A, #4
        m.next_cycle()  # ADD A, #5
        m.next_cycle()  # ADD A, #6
        m.next_cycle()  # RETI
        assert m.mem.a == 29

        m.next_cycle()  # INC A
        m.next_cycle()  # RETI
        assert m.mem.a == 30

        assert m.pc == 123
        assert m.interrupt_stack.top() == 0

    def test_next_cycle__timers(self):
        # Timer 0, Mode 0, T0
        m1 = mcu.Microcontroller()
        m1._rom[0] = 0  # NOP
        m1._rom[1] = 0
        m1._rom[2] = 0
        m1.mem.tr0 = 1
        m1.mem.int0 = 1
        m1.mem.t0_ct = 1
        m1.mem.t0 = 0
        m1.next_cycle()
        assert m1.mem.tl0 == 1
        m1.mem.t0 = 1
        m1.next_cycle()
        m1.mem.t0 = 0
        m1.next_cycle()
        assert m1.mem.tl0 == 2

        # Timer 1, Mode 1, cycles
        m2 = mcu.Microcontroller()
        m2._rom[0] = 0  # NOP (1 cycle)
        m2._rom[1] = 2  # LJMP (2 cycles)
        m2._rom[3] = 123
        m2._rom[4] = 123
        m2.mem.t1_m0 = 1
        m2.mem.tr1 = 1
        m2.mem.t1_gate = 0
        m2.mem.t1_ct = 0
        m2.next_cycle()
        assert m2.mem.tl1 == 1
        m2.next_cycle()
        assert m2.mem.tl1 == 3

        # Timer 0, Mode 3, TL0: T0 (TH0: cycles)
        m3 = mcu.Microcontroller()
        m3._rom[0] = 163  # INC DPTR (2 cycles)
        m3._rom[1] = 237  # MOV A, R5 (1 cycle)
        m3._rom[2] = 163  # INC DPTR
        m3.mem.tr1 = 1
        m3.mem.t0_m1 = 1
        m3.mem.t0_m0 = 1
        m3.mem.tr0 = 1
        m3.mem.t0_gate = 0
        m3.mem.t0_ct = 1
        m3.mem.t0 = 0
        m3.next_cycle()
        assert m3.mem.tl0 == 1
        assert m3.mem.th0 == 2
        m3.mem.t0 = 1
        m3.next_cycle()
        assert m3.mem.tl0 == 1
        assert m3.mem.th0 == 3
        m3.mem.t0 = 0
        m3.next_cycle()
        assert m3.mem.tl0 == 2
        assert m3.mem.th0 == 5

    def test_next_cycle__operation_execution(self):
        m = mcu.Microcontroller()
        m.pc = mcu.DoubleByte(50)
        m._rom[50] = 0  # NOP
        m.next_cycle()
        assert m.pc == 51

        m.pc = mcu.DoubleByte(100)
        m._rom[100] = 2  # LJMP
        m._rom[101] = 171
        m._rom[102] = 205
        m.next_cycle()
        assert m.pc == 43981  # 171 * 2 ** 8 + 205

    def test_pc_prop(self):
        m = mcu.Microcontroller()
        m.pc = 65538
        assert m.pc == 2, 'Overflow not supported - int?'

    def test_direct_addressing(self):
        m = mcu.Microcontroller()
        byte_id = id(m.mem[17])
        m.mem[17] = 123
        assert m.mem[17] == 123 and id(m.mem[17]) == byte_id, 'Byte replaced with int?'
        m.mem[17][7] = 0
        assert m.mem[17] == 122, 'Bit setting not supported'

    def test_register_addressing(self):
        m = mcu.Microcontroller()
        m.mem.selected_register_bank = 3
        byte_id = id(m.mem[8 * m.mem.selected_register_bank + 1])
        m.mem.r1 = 200
        assert m.mem.r1 == 200, 'R1 property not supported'
        assert m.mem[8 * 3 + 1] == 200, 'Address not calculated properly'
        assert id(m.mem[8 * 3 + 1]) == byte_id, 'Value not changed in place'

    def test_mem_prop_bit_access(self):
        m = mcu.Microcontroller()
        m.mem.a = 8
        assert m.mem[224] == 8, 'Property not aliased properly'
        assert m.mem[224][4] == 1
        assert m.mem.a[4] == 1, 'Bit access on property not supported'
        m.mem.a[5] = 1
        assert m.mem.a == 12, 'Bit setting on property not supported'

    def test_mem_val_overflow(self):
        m = mcu.Microcontroller()
        m.mem[30] += 300
        assert m.mem[30] == 44, 'Overflow not supported'

    def test_exec_2(self):
        m = mcu.Microcontroller()
        m._exec_2(171, 205)
        assert m.pc == 43981

    def test_exec_3(self):
        m = mcu.Microcontroller()
        m.mem.a = 2
        m._exec_3()
        assert m.mem.a == 1
        m._exec_3()
        assert m.mem.a == 128

    def test_exec_4(self):
        m = mcu.Microcontroller()
        m._exec_4()
        assert m.mem.a == 1

    def test_exec_5(self):
        m = mcu.Microcontroller()
        m.mem[23] = 15
        m._exec_5(23)
        assert m.mem[23] == 16

    def test_exec_6(self):
        m = mcu.Microcontroller()
        m.mem.r0 = 17
        m.mem[m.mem.r0] = 100
        m._exec_6()
        assert m.mem[m.mem.r0] == 101

    def test_exec_8(self):
        m = mcu.Microcontroller()
        m._exec_8()
        m._exec_8()
        assert m.mem.r0 == 2

    def test_exec_16(self):
        m = mcu.Microcontroller()
        m.mem[33][5] = 1
        m.pc = 105
        m._exec_16(10, 20)
        assert m.mem[33][5] == 0 and m.pc == 125
        m.mem[184][1] = 1
        m._exec_16(190, 15)
        assert m.mem[184][1] == 0 and m.pc == 140

    def test_exec_18(self):
        m = mcu.Microcontroller()
        m.pc = 33719  # 131 * 2 ** 8 + 183
        m._exec_18(171, 205)
        assert m.mem[m.mem.sp] == 131 and m.mem[m.mem.sp - 1] == 183
        assert m.pc == 43981  # 171 * 2 ** 8 + 205

    def test_exec_19(self):
        m = mcu.Microcontroller()
        m.mem.a = 2
        m.mem.c = 1
        m._exec_19()
        assert m.mem.a == 129 and m.mem.c == 0

    def test_exec_20(self):
        m = mcu.Microcontroller()
        m._exec_20()
        assert m.mem.a == 255

    def test_exec_21(self):
        m = mcu.Microcontroller()
        m.mem[23] = 15
        m._exec_21(23)
        assert m.mem[23] == 14

    def test_exec_23(self):
        m = mcu.Microcontroller()
        m.mem.r1 = 17
        m.mem[m.mem.r1] = 100
        m._exec_23()
        assert m.mem[m.mem.r1] == 99

    def test_exec_26(self):
        m = mcu.Microcontroller()
        m._exec_26()
        assert m.mem.r2 == 255

    def test_exec_32(self):
        m = mcu.Microcontroller()
        m.mem[33][5] = 1
        m.pc = 105
        m._exec_32(10, 20)
        assert m.pc == 125
        m.mem[184][1] = 1
        m._exec_32(190, 15)
        assert m.pc == 140

    def test_exec_34(self):
        m = mcu.Microcontroller()
        m.mem.sp += 1
        m.mem[m.mem.sp] = 183
        m.mem.sp += 1
        m.mem[m.mem.sp] = 131
        m._exec_34()
        assert m.pc == 33719  # 131 * 2 ** 8 + 183

    def test_exec_35(self):
        m = mcu.Microcontroller()
        m.mem.a = 64
        m._exec_35()
        assert m.mem.a == 128
        m._exec_35()
        assert m.mem.a == 1

    def test_exec_36(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m._exec_36(20)
        assert m.mem.a == 30

    def test_exec_37(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m.mem[15] = 40
        m._exec_37(15)
        assert m.mem.a == 50

    def test_exec_38(self):
        m = mcu.Microcontroller()
        m.mem.a = 30
        m.mem.r0 = 100
        m.mem[m.mem.r0] = 25
        m._exec_38()
        assert m.mem.a == 55

    def test_exec_44(self):
        m = mcu.Microcontroller()
        m.mem.a = 50
        m.mem.r4 = 5
        m._exec_44()
        assert m.mem.a == 55

    def test_exec_48(self):
        m = mcu.Microcontroller()
        m.mem[33][5] = 0
        m.pc = 105
        m._exec_48(10, 20)
        assert m.pc == 125
        m.mem[184][1] = 0
        m._exec_48(190, 15)
        assert m.pc == 140

    def test_exec_50(self):
        m = mcu.Microcontroller()
        m.pc = 123
        m._exec_18(0, 3)  # INT0: LCALL 3h
        m.interrupt_stack.push(5)
        assert m.pc == 3
        assert m.interrupt_stack.top() == 5
        m._exec_50()
        assert m.pc == 123
        assert m.interrupt_stack.top() == 0

    def test_exec_51(self):
        m = mcu.Microcontroller()
        m.mem.a = 65
        m.mem.c = 1
        m._exec_51()
        assert m.mem.a == 131 and m.mem.c == 0

    def test_exec_52(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m.mem.c = 1
        m._exec_52(20)
        assert m.mem.a == 31

    def test_exec_53(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m.mem.c = 1
        m.mem[15] = 40
        m._exec_53(15)
        assert m.mem.a == 51

    def test_exec_55(self):
        m = mcu.Microcontroller()
        m.mem.a = 30
        m.mem.c = 1
        m.mem.r1 = 100
        m.mem[m.mem.r1] = 25
        m._exec_55()
        assert m.mem.a == 56

    def test_exec_60(self):
        m = mcu.Microcontroller()
        m.mem.a = 50
        m.mem.c = 1
        m.mem.r4 = 5
        m._exec_60()
        assert m.mem.a == 56

    def test_exec_64(self):
        m = mcu.Microcontroller()
        m.pc = 123
        m.mem.c = 0
        m._exec_64(30)
        assert m.pc == 123
        m.mem.c = 1
        m._exec_64(30)
        assert m.pc == 153

    def test_exec_66(self):
        m = mcu.Microcontroller()
        m.mem.a = 5
        m.mem[10] = 2
        m._exec_66(10)
        assert m.mem[10] == 7

    def test_exec_67(self):
        m = mcu.Microcontroller()
        m.mem[10] = 2
        m._exec_67(10, 1)
        assert m.mem[10] == 3

    def test_exec_68(self):
        m = mcu.Microcontroller()
        m.mem.a = 6
        m._exec_68(5)
        assert m.mem.a == 7

    def test_exec_69(self):
        m = mcu.Microcontroller()
        m.mem.a = 6
        m.mem[10] = 5
        m._exec_69(10)
        assert m.mem.a == 7

    def test_exec_71(self):
        m = mcu.Microcontroller()
        m.mem.a = 1
        m.mem.r1 = 10
        m.mem[m.mem.r1] = 8
        m._exec_71()
        assert m.mem.a == 9

    def test_exec_74(self):
        m = mcu.Microcontroller()
        m.mem.a = 3
        m.mem.r2 = 10
        m._exec_74()
        assert m.mem.a == 11

    def test_exec_80(self):
        m = mcu.Microcontroller()
        m.pc = 123
        m.mem.c = 1
        m._exec_80(30)
        assert m.pc == 123
        m.mem.c = 0
        m._exec_80(30)
        assert m.pc == 153

    def test_exec_82(self):
        m = mcu.Microcontroller()
        m.mem.a = 5
        m.mem[10] = 3
        m._exec_82(10)
        assert m.mem[10] == 1

    def test_exec_83(self):
        m = mcu.Microcontroller()
        m.mem[10] = 13
        m._exec_83(10, 5)
        assert m.mem[10] == 5

    def test_exec_84(self):
        m = mcu.Microcontroller()
        m.mem.a = 6
        m._exec_84(5)
        assert m.mem.a == 4

    def test_exec_85(self):
        m = mcu.Microcontroller()
        m.mem.a = 5
        m.mem[10] = 3
        m._exec_85(10)
        assert m.mem.a == 1

    def test_exec_87(self):
        m = mcu.Microcontroller()
        m.mem.a = 13
        m.mem.r1 = 10
        m.mem[m.mem.r1] = 3
        m._exec_87()
        assert m.mem.a == 1

    def test_exec_90(self):
        m = mcu.Microcontroller()
        m.mem.a = 3
        m.mem.r2 = 10
        m._exec_90()
        assert m.mem.a == 2

    def test_exec_96(self):
        m = mcu.Microcontroller()
        m.pc = 100
        m.mem.a = 0
        m._exec_96(30)
        assert m.pc == 130
        m.mem.a = 15
        m._exec_96(30)
        assert m.pc == 130

    def test_exec_97(self):
        m = mcu.Microcontroller()
        m.pc = 291
        m._exec_97(69)
        assert m.pc == 837

    def test_exec_98(self):
        m = mcu.Microcontroller()
        m.mem.a = 5
        m.mem[10] = 3
        m._exec_98(10)
        assert m.mem[10] == 6

    def test_exec_99(self):
        m = mcu.Microcontroller()
        m.mem[10] = 13
        m._exec_99(10, 5)
        assert m.mem[10] == 8

    def test_exec_100(self):
        m = mcu.Microcontroller()
        m.mem.a = 6
        m._exec_100(5)
        assert m.mem.a == 3

    def test_exec_101(self):
        m = mcu.Microcontroller()
        m.mem.a = 5
        m.mem[10] = 3
        m._exec_101(10)
        assert m.mem.a == 6

    def test_exec_103(self):
        m = mcu.Microcontroller()
        m.mem.a = 13
        m.mem.r1 = 3
        m.mem[m.mem.r1] = 10
        m._exec_103()
        assert m.mem.a == 7

    def test_exec_106(self):
        m = mcu.Microcontroller()
        m.mem.a = 3
        m.mem.r2 = 10
        m._exec_106()
        assert m.mem.a == 9

    def test_exec_112(self):
        m = mcu.Microcontroller()
        m.pc = 100
        m.mem.a = 0
        m._exec_112(30)
        assert m.pc == 100
        m.mem.a = 15
        m._exec_112(30)
        assert m.pc == 130

    def test_exec_113(self):
        m = mcu.Microcontroller()
        m.pc = 291
        m._exec_113(69)
        assert m.pc == 837
        assert m.mem[m.mem.sp] == 1 and m.mem[m.mem.sp - 1] == 35

    def test_exec_114(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m.mem[32][2] = 0
        m._exec_114(5)
        assert m.mem.c == 0
        m.mem.c = 0
        m.mem[32][2] = 1
        m._exec_114(5)
        assert m.mem.c == 1
        m.mem.c = 1
        m.mem[184][1] = 0
        m._exec_114(190)
        assert m.mem.c == 1
        m.mem.c = 1
        m.mem[184][1] = 1
        m._exec_114(190)
        assert m.mem.c == 1

    def test_exec_115(self):
        m = mcu.Microcontroller()
        m.mem.a = 20
        m.mem.dptr = 65000
        m._exec_115()
        assert m.pc == 65020

    def test_exec_116(self):
        m = mcu.Microcontroller()
        m._exec_116(21)
        assert m.mem.a == 21

    def test_exec_117(self):
        m = mcu.Microcontroller()
        m._exec_117(10, 21)
        assert m.mem[10] == 21

    def test_exec_118(self):
        m = mcu.Microcontroller()
        m.mem.r0 = 20
        m._exec_118(10)
        assert m.mem[m.mem.r0] == 10

    def test_exec_127(self):
        m = mcu.Microcontroller()
        m._exec_127(33)
        assert m.mem.r7 == 33

    def test_exec_128(self):
        m = mcu.Microcontroller()
        m.pc = 1000
        m._exec_128(30)
        assert m.pc == 1030
        m._exec_128(131)
        assert m.pc == 905

    def test_exec_130(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m.mem[32][2] = 0
        m._exec_130(5)
        assert m.mem.c == 0
        m.mem.c = 0
        m.mem[32][2] = 1
        m._exec_130(5)
        assert m.mem.c == 0
        m.mem.c = 1
        m.mem[184][1] = 0
        m._exec_130(190)
        assert m.mem.c == 0
        m.mem.c = 1
        m.mem[184][1] = 1
        m._exec_130(190)
        assert m.mem.c == 1

    def test_exec_131(self):
        m = mcu.Microcontroller()
        m._rom[30050] = 123
        m.pc = 30000
        m.mem.a = 50
        m._exec_131()
        assert m.mem.a == 123

    def test_exec_132(self):
        m = mcu.Microcontroller()
        m.mem.a = 11
        m.mem.b = 4
        m._exec_132()
        assert m.mem.a == 2 and m.mem.b == 3
        assert m.mem.c == 0

    def test_exec_133(self):
        m = mcu.Microcontroller()
        m.mem[20] = 50
        m._exec_133(20, 30)
        assert m.mem[30] == 50

    def test_exec_134(self):
        m = mcu.Microcontroller()
        m.mem.r0 = 20
        m.mem[m.mem.r0] = 100
        m._exec_134(10)
        assert m.mem[10] == 100

    def test_exec_138(self):
        m = mcu.Microcontroller()
        m.mem.r2 = 20
        m._exec_138(50)
        assert m.mem[50] == 20

    def test_exec_144(self):
        m = mcu.Microcontroller()
        m._exec_144(30)
        assert m.mem.dptr == 30

    def test_exec_146(self):
        m = mcu.Microcontroller()
        m.mem.c = 1
        m._exec_146(5)
        assert m.mem[32][2] == 1
        m._exec_146(190)
        assert m.mem[184][1] == 1

    def test_exec_148(self):
        m = mcu.Microcontroller()
        m.mem.a = 100
        m.mem.c = 1
        m._exec_148(20)
        assert m.mem.a == 79

    def test_exec_149(self):
        m = mcu.Microcontroller()
        m.mem.a = 100
        m.mem.c = 1
        m.mem[10] = 50
        m._exec_149(10)
        assert m.mem.a == 49

    def test_exec_151(self):
        m = mcu.Microcontroller()
        m.mem.a = 50
        m.mem.c = 1
        m.mem.r1 = 30
        m.mem[m.mem.r1] = 10
        m._exec_151()
        assert m.mem.a == 39

    def test_exec_154(self):
        m = mcu.Microcontroller()
        m.mem.a = 50
        m.mem.c = 1
        m.mem.r2 = 30
        m._exec_154()
        assert m.mem.a == 19

    def test_exec_160(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m.mem[32][2] = 0
        m._exec_160(5)
        assert m.mem.c == 1
        m.mem.c = 0
        m.mem[32][2] = 1
        m._exec_160(5)
        assert m.mem.c == 0
        m.mem.c = 1
        m.mem[184][1] = 0
        m._exec_160(190)
        assert m.mem.c == 1
        m.mem.c = 1
        m.mem[184][1] = 1
        m._exec_160(190)
        assert m.mem.c == 1

    def test_exec_162(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m.mem[32][2] = 1
        m._exec_162(5)
        assert m.mem.c == 1
        m.mem[184][1] = 0
        m._exec_162(190)
        assert m.mem.c == 0

    def test_exec_163(self):
        m = mcu.Microcontroller()
        m.mem.dptr = 50
        m._exec_163()
        assert m.mem.dptr == 51

    def test_exec_164(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m.mem.b = 90
        m._exec_164()
        assert m.mem.a == 132
        assert m.mem.b == 3
        assert m.mem.c == 0

    def test_exec_167(self):
        m = mcu.Microcontroller()
        m.mem.r1 = 35
        m.mem[15] = 200
        m._exec_167(15)
        assert m.mem[35] == 200

    def test_exec_174(self):
        m = mcu.Microcontroller()
        m.mem[15] = 200
        m._exec_174(15)
        assert m.mem.r6 == 200

    def test_exec_176(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m.mem[32][2] = 0
        m._exec_176(5)
        assert m.mem.c == 0
        m.mem.c = 0
        m.mem[32][2] = 1
        m._exec_176(5)
        assert m.mem.c == 0
        m.mem.c = 1
        m.mem[184][1] = 0
        m._exec_176(190)
        assert m.mem.c == 1
        m.mem.c = 1
        m.mem[184][1] = 1
        m._exec_176(190)
        assert m.mem.c == 0

    def test_exec_178(self):
        m = mcu.Microcontroller()
        m.mem[33][5] = 0
        m._exec_178(10)
        assert m.mem[33][5] == 1
        m._exec_178(10)
        assert m.mem[33][5] == 0
        m.mem[184][1] = 0
        m._exec_178(190)
        assert m.mem[184][1] == 1
        m._exec_178(190)
        assert m.mem[184][1] == 0

    def test_exec_179(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m._exec_179()
        assert m.mem.c == 1
        m._exec_179()
        assert m.mem.c == 0

    def test_exec_180(self):
        m = mcu.Microcontroller()
        m.pc = 50
        m.mem.a = 3
        m._exec_180(4, 30)
        assert m.pc == 80 and m.mem.c == 1
        m._exec_180(3, 20)
        assert m.pc == 80 and m.mem.c == 0

    def test_exec_181(self):
        m = mcu.Microcontroller()
        m.pc = 50
        m.mem.a = 3
        m.mem[10] = 4
        m._exec_181(10, 30)
        assert m.pc == 80 and m.mem.c == 1
        m.mem[10] = 3
        m._exec_181(10, 20)
        assert m.pc == 80 and m.mem.c == 0

    def test_exec_182(self):
        m = mcu.Microcontroller()
        m.pc = 50
        m.mem.r0 = 10
        m.mem[m.mem.r0] = 3
        m._exec_182(4, 30)
        assert m.pc == 80 and m.mem.c == 1
        m.mem[m.mem.r0] = 4
        m._exec_182(4, 20)
        assert m.pc == 80 and m.mem.c == 0

    def test_exec_190(self):
        m = mcu.Microcontroller()
        m.pc = 50
        m.mem.r6 = 3
        m._exec_190(4, 30)
        assert m.pc == 80 and m.mem.c == 1
        m.mem.r6 = 4
        m._exec_190(4, 20)
        assert m.pc == 80 and m.mem.c == 0

    def test_exec_192(self):
        m = mcu.Microcontroller()
        m.mem.sp = 10
        m.mem[120] = 30
        m._exec_192(120)
        assert m.mem.sp == 11 and m.mem[11] == 30

    def test_exec_194(self):
        m = mcu.Microcontroller()
        m.mem[35] = 7
        m._exec_194(25)
        assert m.mem[35] == 5
        m.mem[136][3] = 1
        m._exec_194(140)
        assert m.mem[136][3] == 0

    def test_exec_195(self):
        m = mcu.Microcontroller()
        m.mem.c = 1
        m._exec_195()
        assert m.mem.c == 0

    def test_exec_196(self):
        m = mcu.Microcontroller()
        m.mem.a = 217
        m._exec_196()
        assert m.mem.a == 157

    def test_exec_197(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m.mem[20] = 30
        m._exec_197(20)
        assert m.mem.a == 30 and m.mem[20] == 10

    def test_exec_198(self):
        m = mcu.Microcontroller()
        m.mem.a = 33
        m.mem.r0 = 50
        m.mem[50] = 123
        m._exec_198()
        assert m.mem.a == 123 and m.mem[50] == 33

    def test_exec_201(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m.mem.r1 = 20
        m._exec_201()
        assert m.mem.a == 20 and m.mem.r1 == 10

    def test_exec_208(self):
        m = mcu.Microcontroller()
        m.mem.sp = 10
        m.mem[10] = 123
        m._exec_208(50)
        assert m.mem.sp == 9 and m.mem[50] == 123

    def test_exec_210(self):
        m = mcu.Microcontroller()
        m.mem[35] = 1
        m._exec_210(25)
        assert m.mem[35] == 3
        m._exec_210(140)
        assert m.mem[136][3] == 1

    def test_exec_211(self):
        m = mcu.Microcontroller()
        m.mem.c = 0
        m._exec_211()
        assert m.mem.c == 1

    def test_exec_212(self):
        m = mcu.Microcontroller()
        m.mem.a = 190
        m._exec_212()
        assert m.mem.a == 36

    def test_exec_213(self):
        m = mcu.Microcontroller()
        m.mem[20] = 2
        m.pc = 50
        m._exec_213(20, 30)
        assert m.mem[20] == 1 and m.pc == 80
        m._exec_213(20, 30)
        assert m.mem[20] == 0 and m.pc == 80

    def test_exec_214(self):
        m = mcu.Microcontroller()
        m.mem.a = 0b10011100
        m.mem.r0 = 30
        m.mem[30] = 0b01110101
        m._exec_214()
        assert m.mem.a == 0b10010101 and m.mem[30] == 0b01111100

    def test_exec_222(self):
        m = mcu.Microcontroller()
        m.mem.r6 = 2
        m.pc = 50
        m._exec_222(30)
        assert m.mem.r6 == 1 and m.pc == 80
        m._exec_222(30)
        assert m.mem.r6 == 0 and m.pc == 80

    def test_exec_224(self):
        m = mcu.Microcontroller()
        m.mem.dptr = 20000
        m.xmem[20000] = 123
        m._exec_224()
        assert m.mem.a == 123

    def test_exec_226(self):
        m = mcu.Microcontroller()
        m.mem.p2 = 0b01011011
        m.mem.r0 = 0b00010011
        m.xmem[0b0101101100010011] = 123
        m._exec_226()
        assert m.mem.a == 123

    def test_exec_228(self):
        m = mcu.Microcontroller()
        m.mem.a = 30
        m._exec_228()
        assert m.mem.a == 0

    def test_exec_229(self):
        m = mcu.Microcontroller()
        m.mem[15] = 100
        m._exec_229(15)
        assert m.mem.a == 100

    def test_exec_230(self):
        m = mcu.Microcontroller()
        m.mem.r0 = 15
        m.mem[m.mem.r0] = 150
        m._exec_230()
        assert m.mem.a == 150

    def test_exec_235(self):
        m = mcu.Microcontroller()
        m.mem.r3 = 20
        m._exec_235()
        assert m.mem.a == 20

    def test_exec_240(self):
        m = mcu.Microcontroller()
        m.mem.a = 123
        m.mem.dptr = 50000
        m._exec_240()
        assert m.xmem[50000] == 123

    def test_exec_243(self):
        m = mcu.Microcontroller()
        m.mem.a = 123
        m.mem.p2 = 0b01011011
        m.mem.r1 = 0b00010011
        m._exec_243()
        assert m.xmem[0b0101101100010011] == 123

    def test_exec_244(self):
        m = mcu.Microcontroller()
        m.mem.a = 7
        m._exec_244()
        assert m.mem.a == 248

    def test_exec_245(self):
        m = mcu.Microcontroller()
        m.mem.a = 10
        m._exec_245(100)
        assert m.mem[100] == 10

    def test_exec_247(self):
        m = mcu.Microcontroller()
        m.mem.a = 30
        m.mem.r1 = 20
        m._exec_247()
        assert m.mem[20] == 30

    def test_exec_250(self):
        m = mcu.Microcontroller()
        m.mem.a = 50
        m._exec_250()
        assert m.mem.r2 == 50


class TestProgramMemory:
    def test__getitem__(self):
        rom = mcu.ProgramMemory()
        rom[5] = 10
        rom[6] = 20
        rom[7] = 30
        assert rom[6] == 20
        assert rom[5:8] == [10, 20, 30]

    def test__setitem__(self):
        rom = mcu.ProgramMemory()
        rom[5] = 10
        assert rom[5] == 10


class TestInternalDataMemory:
    def test_decimal_access(self):
        mem = mcu.InternalDataMemory()
        byte_id = id(mem[2])
        mem[2] = 30
        assert mem[2] == 30 and id(mem[2]) == byte_id, 'Decimal access not supported'
        b = mcu.Byte(3)
        mem[b] = 30
        assert mem[3] == 30, 'Cannot use a Byte instance as an address - not converted to int?'

    def test_bit_access(self):
        mem = mcu.InternalDataMemory()
        mem[5][1] = 1
        assert mem[5] == 64, 'Bit access not supported'

    def test_p0_prop(self):
        mem = mcu.InternalDataMemory()
        assert mem.p0 == 0b11111111
        mem.p0 = 30
        assert mem[128] == 30
        mem.p0 = 1
        assert mem.p0[7] == 1

    def test_dptr_prop(self):
        mem = mcu.InternalDataMemory()
        mem.dptr = 65530
        mem.dptr += 10
        assert mem.dptr == 4, 'Overflow not supported - int?'
        mem.dptr = 65530
        assert mem[130] == int('1' * 8, 2) and mem[131] == int('11111010', 2), 'Wrong binary representation'

    def test_tcon_prop(self):
        mem = mcu.InternalDataMemory()
        mem.tcon[1] = 1
        assert mem.tcon == 64

    def test_tf1_prop(self):
        mem = mcu.InternalDataMemory()
        mem.tf1 = 1
        assert mem.tf1 == 1
        assert mem[136][0] == 1

    def test_tmod_prop(self):
        mem = mcu.InternalDataMemory()
        mem.tmod[2] = 1
        assert mem.tmod == 32

    def test_t1_m0_prop(self):
        mem = mcu.InternalDataMemory()
        mem.t1_m0 = 1
        assert mem.t1_m0 == 1
        assert mem[137][3] == 1

    def test_t1_mode_prop(self):
        mem = mcu.InternalDataMemory()
        mem.t1_m1 = 1
        mem.t1_m0 = 1
        assert mem.t1_mode == 3

    def test_tl0_prop(self):
        mem = mcu.InternalDataMemory()
        mem.tl0 = 32
        assert mem.tl0 == 32
        assert mem[138][2] == 1

    def test_th1_prop(self):
        mem = mcu.InternalDataMemory()
        mem.th1 = 16
        assert mem.th1 == 16
        assert mem[141][3] == 1

    def test_p1_prop(self):
        mem = mcu.InternalDataMemory()
        assert mem.p1 == 0b11111111
        mem.p1 = 50
        assert mem[144] == 50
        mem.p1 = 8
        assert mem.p1[4] == 1

    def test_p2_prop(self):
        mem = mcu.InternalDataMemory()
        assert mem.p2 == 0b11111111
        mem.p2 = 10
        assert mem[160] == 10
        mem.p2 = 2
        assert mem.p2[6] == 1

    def test_ie_prop(self):
        mem = mcu.InternalDataMemory()
        mem.ie[2] = 1
        assert mem.ie == 32

    def test_es_prop(self):
        mem = mcu.InternalDataMemory()
        mem.es = 1
        assert mem.es == 1
        assert mem[168][3] == 1

    def test_p3_prop(self):
        mem = mcu.InternalDataMemory()
        assert mem.p3 == 0b11111111
        mem.p3 = 0
        assert mem[176] == 0
        mem.p3 = 4
        assert mem.p3[5] == 1

    def test_t1_prop(self):
        mem = mcu.InternalDataMemory()
        assert mem.t1 == 1
        mem.t1 = 0
        assert mem.t1 == 0

    def test_int0_prop(self):
        mem = mcu.InternalDataMemory()
        assert mem.int0 == 1
        mem.int0 = 0
        assert mem.int0 == 0

    def test_ip_prop(self):
        mem = mcu.InternalDataMemory()
        mem.ip[3] = 1
        assert mem.ip == 16

    def test_pt1_prop(self):
        mem = mcu.InternalDataMemory()
        mem.pt1 = 1
        assert mem.pt1 == 1
        assert mem[184][4] == 1

    def test_psw_prop(self):
        mem = mcu.InternalDataMemory()
        mem.psw[0] = 1
        assert mem.psw == 128

    def test_c_prop(self):
        mem = mcu.InternalDataMemory()
        mem.c = 1
        assert mem.c == 1
        assert mem[208][0] == 1

    def test_ac_prop(self):
        mem = mcu.InternalDataMemory()
        mem.ac = 1
        assert mem.ac == 1
        assert mem[208][1] == 1

    def test_rs1_prop(self):
        mem = mcu.InternalDataMemory()
        mem.rs1 = 1
        assert mem.rs1 == 1
        assert mem[208][3] == 1

    def test_rs0_prop(self):
        mem = mcu.InternalDataMemory()
        mem.rs0 = 1
        assert mem.rs0 == 1
        assert mem[208][4] == 1

    def test_ov_prop(self):
        mem = mcu.InternalDataMemory()
        mem.ov = 1
        assert mem.ov == 1
        assert mem[208][5] == 1

    def test_p_prop(self):
        mem = mcu.InternalDataMemory()
        mem.p = 1
        assert mem.p == 1
        assert mem[208][7] == 1

    def test_selected_register_bank_prop(self):
        mem = mcu.InternalDataMemory()
        mem.selected_register_bank = 3
        assert mem.selected_register_bank == 3 and mem.rs1 == 1 and mem.rs0 == 1

    def test_r1_prop(self):
        mem = mcu.InternalDataMemory()
        mem.selected_register_bank = 2
        mem.r1 = 3
        assert mem.r1 == 3 and mem[8 * 2 + 1] == 3


class TestExternalDataMemory:
    def test_access(self):
        xmem = mcu.ExternalDataMemory()
        byte_id = id(xmem[2])
        xmem[2] = mcu.Byte(30)
        assert xmem[2] == 30 and id(xmem[2]) == byte_id, 'Decimal access not supported'
        b = mcu.DoubleByte(500)
        xmem[b] = mcu.Byte(30)
        assert xmem[500] == 30, 'Cannot use a DoubleByte instance as an address - not converted to int?'


class TestByte:
    def test__getitem__(self):
        assert mcu.Byte(4)[5] == 1, 'Bit access not supported'

    def test__setitem__(self):
        b = mcu.Byte()
        b[2] = 1
        assert b == 32, 'Bit setting not supported'

    def test__setattr__(self):
        assert mcu.Byte(260) == 4, 'Overflow not supported'
        assert mcu.Byte(-2) == 254, 'Underflow not supported'

    def test__add__(self):
        b = mcu.Byte(4)
        b += 1
        assert b == 5
        assert b + mcu.Byte(3) == 8

    def test__radd__(self):
        assert 5 + mcu.Byte(4) == 9

    def test__sub__(self):
        b = mcu.Byte(4)
        b -= 1
        assert b == 3
        assert b - mcu.Byte(2) == 1

    def test__rsub__(self):
        assert 20 - mcu.Byte(5) == 15

    def test__mul__(self):
        assert mcu.Byte(25) * mcu.Byte(40) == (3, 232)

    def test__divmod__(self):
        assert divmod(mcu.Byte(9), mcu.Byte(2)) == (4, 1)

    def test__and__(self):
        assert mcu.Byte(5) & mcu.Byte(3) == 1

    def test__or__(self):
        assert mcu.Byte(5) | mcu.Byte(2) == 7

    def test__xor__(self):
        assert mcu.Byte(5) ^ mcu.Byte(3) == 6

    def test_rotate_left(self):
        b = mcu.Byte(64)
        b.rotate_left()
        assert b == 128
        b.rotate_left()
        assert b == 1

    def test_rotate_right(self):
        b = mcu.Byte(2)
        b.rotate_right()
        assert b == 1
        b.rotate_right()
        assert b == 128


class TestDoubleByte:
    def test__getitem__(self):
        assert mcu.DoubleByte(2048)[4] == 1, 'Bit access not supported'

    def test__setitem__(self):
        b = mcu.DoubleByte()
        b[5] = 1
        assert b == 1024, 'Bit setting not supported'

    def test__setattr__(self):
        assert mcu.DoubleByte(65538) == 2, 'Overflow not supported'
        assert mcu.DoubleByte(-4) == 65532, 'Underflow not supported'


class TestTimer0:
    def test_increment__mode3_th0_only(self):
        m = mcu.Microcontroller()
        m.mem.th0 = 254
        for _ in range(3):
            m.timer0.increment(mode3_th0_only=True)
        assert m.mem.th0 == 1
        assert m.mem.tf1 == 1

    def test_increment__mode0(self):
        m = mcu.Microcontroller()
        m.mem.th0 = 254
        m.mem.tl0 = 29
        m.timer0.increment()
        assert m.mem.th0 == 254
        assert m.mem.tl0 == 30
        assert m.mem.tf0 == 0

        m.mem.th0 = 255
        m.timer0.increment()
        assert m.mem.th0 == 255
        assert m.mem.tl0 == 31
        assert m.mem.tf0 == 0

        m.timer0.increment()
        assert m.mem.th0 == 0
        assert m.mem.tl0 == 0
        assert m.mem.tf0 == 1

    def test_increment__mode1(self):
        m = mcu.Microcontroller()
        m.mem.th0 = 254
        m.mem.tl0 = 253
        m.mem.t0_m0 = 1
        m.timer0.increment()
        assert m.mem.th0 == 254
        assert m.mem.tl0 == 254
        assert m.mem.tf0 == 0

        m.mem.th0 = 255
        m.timer0.increment()
        assert m.mem.th0 == 255
        assert m.mem.tl0 == 255
        assert m.mem.tf0 == 0

        m.timer0.increment()
        assert m.mem.th0 == 0
        assert m.mem.tl0 == 0
        assert m.mem.tf0 == 1

    def test_increment__mode2(self):
        m = mcu.Microcontroller()
        m.mem.th0 = 123
        m.mem.tl0 = 254
        m.mem.t0_m1 = 1
        m.timer0.increment()
        assert m.mem.th0 == 123
        assert m.mem.tl0 == 255
        assert m.mem.tf0 == 0
        m.timer0.increment()
        assert m.mem.th0 == 123
        assert m.mem.tl0 == 123
        assert m.mem.tf0 == 1

    def test_increment__mode3(self):
        m = mcu.Microcontroller()
        m.mem.t0_m1 = 1
        m.mem.t0_m0 = 1
        m.mem.tl0 = 254
        for _ in range(4):
            m.timer0.increment()
        assert m.mem.tl0 == 2
        assert m.mem.tf0 == 1


class TestOperation:
    def test_cycles(self):
        op = mcu.Operation(16)
        assert op.cycles == 2

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


class TestStack:
    def test_stack(self):
        s = mcu.Stack()
        s.push(10)
        s.push(20)
        assert s.top() == 20
        assert s.pop() == 20
        assert s.pop() == 10
