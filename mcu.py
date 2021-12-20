from typing import Union

import disassembler


class Microcontroller:
    def __init__(self):
        self._rom = ProgramMemory()
        self._mem = DataMemory()
        self._pc = DoubleByte()
        self.interrupt_stack = Stack()
        self.interrupt_stack.push(0)

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, value):
        self._pc.value = value

    def load_hex_file(self, filepath):
        for record in disassembler.IntelHexFile(filepath):
            for addr, byte in enumerate(record, record.first_byte_addr):
                self._rom[addr] = byte

    def reset_rom(self):
        self._rom = ProgramMemory()

    def next_cycle(self):
        # handle an interrupt request
        if self._mem.ea:
            # INT0 (high priority)
            if ((int0_awaiting := self._mem.ie0 and self._mem.ex0)
                    and self._mem.px0 and self.interrupt_stack.top() < 10):
                self._mem.ie0 = 0
                self.interrupt_stack.push(10)
                self._exec_18(0, 3)

            # T0 (high priority)
            elif ((t0_awaiting := self._mem.tf0 and self._mem.et0)
                  and self._mem.pt0 and self.interrupt_stack.top() < 9):
                self._mem.tf0 = 0
                self.interrupt_stack.push(9)
                self._exec_18(0, 11)

            # INT1 (high priority)
            elif ((int1_awaiting := self._mem.ie1 and self._mem.ex1)
                  and self._mem.px1 and self.interrupt_stack.top() < 8):
                self._mem.ie1 = 0
                self.interrupt_stack.push(8)
                self._exec_18(0, 19)

            # T1 (high priority)
            elif ((t1_awaiting := self._mem.tf1 and self._mem.et1)
                  and self._mem.pt1 and self.interrupt_stack.top() < 7):
                self._mem.tf1 = 0
                self.interrupt_stack.push(7)
                self._exec_18(0, 27)

            # TODO: SP (RI/TI) (high priority)

            # INT0 (low priority)
            elif int0_awaiting and self.interrupt_stack.top() < 5:
                self._mem.ie0 = 0
                self.interrupt_stack.push(5)
                self._exec_18(0, 3)

            # T0 (low priority)
            elif t0_awaiting and self.interrupt_stack.top() < 4:
                self._mem.tf0 = 0
                self.interrupt_stack.push(4)
                self._exec_18(0, 11)

            # INT1 (low priority)
            elif int1_awaiting and self.interrupt_stack.top() < 3:
                self._mem.ie1 = 0
                self.interrupt_stack.push(3)
                self._exec_18(0, 19)

            # T1 (low priority)
            elif t1_awaiting and self.interrupt_stack.top() < 2:
                self._mem.tf1 = 0
                self.interrupt_stack.push(2)
                self._exec_18(0, 27)

            # TODO: SP (RI/TI) (low priority)

        op = Operation(self._rom[self.pc])
        op.args = self._rom[int(self.pc + 1):int(self.pc + len(op))]
        self.pc += len(op)
        # Jump operations may override the PC
        exec(f'self._exec_{op.opcode}(*op.args)')

    def _exec_0(self):
        return

    def _exec_2(self, high_order_byte, low_order_byte):
        # Turn two one-byte arguments (as stored in a .hex file) into one two-byte argument
        # e.g. 0xAB = 171, 0xCD = 205; 171 * 16 ** 2 + 205 = 43981 = 0xABCD
        self.pc = high_order_byte * 16 ** 2 + low_order_byte

    def _exec_4(self):
        self._mem.a += 1

    def _exec_5(self, direct):
        self._mem[direct] += 1

    def _exec_6(self):
        self._mem[self._mem.r0] += 1

    def _exec_7(self):
        self._mem[self._mem.r1] += 1

    def _exec_8(self):
        self._mem.r0 += 1

    def _exec_9(self):
        self._mem.r1 += 1

    def _exec_10(self):
        self._mem.r2 += 1

    def _exec_11(self):
        self._mem.r3 += 1

    def _exec_12(self):
        self._mem.r4 += 1

    def _exec_13(self):
        self._mem.r5 += 1

    def _exec_14(self):
        self._mem.r6 += 1

    def _exec_15(self):
        self._mem.r7 += 1

    def _exec_18(self, high_order_byte, low_order_byte):
        self._mem.sp += 1
        self._mem[self._mem.sp] = int(self.pc.bits()[8:], 2)
        self._mem.sp += 1
        self._mem[self._mem.sp] = int(self.pc.bits()[:8], 2)
        # Turn two one-byte arguments (as stored in a .hex file) into one two-byte argument
        # e.g. 0xAB = 171, 0xCD = 205; 171 * 16 ** 2 + 205 = 43981 = 0xABCD
        self.pc = high_order_byte * 16 ** 2 + low_order_byte

    def _exec_20(self):
        self._mem.a -= 1

    def _exec_21(self, direct):
        self._mem[direct] -= 1

    def _exec_22(self):
        self._mem[self._mem.r0] -= 1

    def _exec_23(self):
        self._mem[self._mem.r1] -= 1

    def _exec_24(self):
        self._mem.r0 -= 1

    def _exec_25(self):
        self._mem.r1 -= 1

    def _exec_26(self):
        self._mem.r2 -= 1

    def _exec_27(self):
        self._mem.r3 -= 1

    def _exec_28(self):
        self._mem.r4 -= 1

    def _exec_29(self):
        self._mem.r5 -= 1

    def _exec_30(self):
        self._mem.r6 -= 1

    def _exec_31(self):
        self._mem.r7 -= 1

    def _exec_34(self):
        high_order_byte = self._mem[self._mem.sp]
        self._mem.sp -= 1
        low_order_byte = self._mem[self._mem.sp]
        self._mem.sp -= 1
        self.pc = int(f'{high_order_byte:b}{low_order_byte:08b}', 2)

    def _exec_36(self, immed):
        self._mem.a += immed

    def _exec_37(self, direct):
        self._mem.a += self._mem[direct]

    def _exec_38(self):
        self._mem.a += self._mem[self._mem.r0]

    def _exec_39(self):
        self._mem.a += self._mem[self._mem.r1]

    def _exec_40(self):
        self._mem.a += self._mem.r0

    def _exec_41(self):
        self._mem.a += self._mem.r1

    def _exec_42(self):
        self._mem.a += self._mem.r2

    def _exec_43(self):
        self._mem.a += self._mem.r3

    def _exec_44(self):
        self._mem.a += self._mem.r4

    def _exec_45(self):
        self._mem.a += self._mem.r5

    def _exec_46(self):
        self._mem.a += self._mem.r6

    def _exec_47(self):
        self._mem.a += self._mem.r7

    def _exec_50(self):
        high_order_byte = self._mem[self._mem.sp]
        self._mem.sp -= 1
        low_order_byte = self._mem[self._mem.sp]
        self._mem.sp -= 1
        self.pc = int(f'{high_order_byte:b}{low_order_byte:08b}', 2)
        self.interrupt_stack.pop()

    def _exec_52(self, immed):
        self._mem.a += self._mem.c + immed

    def _exec_53(self, direct):
        self._mem.a += self._mem.c + self._mem[direct]

    def _exec_54(self):
        self._mem.a += self._mem.c + self._mem[self._mem.r0]

    def _exec_55(self):
        self._mem.a += self._mem.c + self._mem[self._mem.r1]

    def _exec_56(self):
        self._mem.a += self._mem.c + self._mem.r0

    def _exec_57(self):
        self._mem.a += self._mem.c + self._mem.r1

    def _exec_58(self):
        self._mem.a += self._mem.c + self._mem.r2

    def _exec_59(self):
        self._mem.a += self._mem.c + self._mem.r3

    def _exec_60(self):
        self._mem.a += self._mem.c + self._mem.r4

    def _exec_61(self):
        self._mem.a += self._mem.c + self._mem.r5

    def _exec_62(self):
        self._mem.a += self._mem.c + self._mem.r6

    def _exec_63(self):
        self._mem.a += self._mem.c + self._mem.r7

    def _exec_64(self, offset):
        if self._mem.c:
            self.pc += offset

    def _exec_66(self, direct):
        self._mem[direct] |= self._mem.a

    def _exec_67(self, direct, immed):
        self._mem[direct] |= immed

    def _exec_68(self, immed):
        self._mem.a |= immed

    def _exec_69(self, direct):
        self._mem.a |= self._mem[direct]

    def _exec_70(self):
        self._mem.a |= self._mem[self._mem.r0]

    def _exec_71(self):
        self._mem.a |= self._mem[self._mem.r1]

    def _exec_72(self):
        self._mem.a |= self._mem.r0

    def _exec_73(self):
        self._mem.a |= self._mem.r1

    def _exec_74(self):
        self._mem.a |= self._mem.r2

    def _exec_75(self):
        self._mem.a |= self._mem.r3

    def _exec_76(self):
        self._mem.a |= self._mem.r4

    def _exec_77(self):
        self._mem.a |= self._mem.r5

    def _exec_78(self):
        self._mem.a |= self._mem.r6

    def _exec_79(self):
        self._mem.a |= self._mem.r7

    def _exec_80(self, offset):
        if not self._mem.c:
            self.pc += offset

    def _exec_82(self, direct):
        self._mem[direct] &= self._mem.a

    def _exec_83(self, direct, immed):
        self._mem[direct] &= immed

    def _exec_84(self, immed):
        self._mem.a &= immed

    def _exec_85(self, direct):
        self._mem.a &= self._mem[direct]

    def _exec_86(self):
        self._mem.a &= self._mem[self._mem.r0]

    def _exec_87(self):
        self._mem.a &= self._mem[self._mem.r1]

    def _exec_88(self):
        self._mem.a &= self._mem.r0

    def _exec_89(self):
        self._mem.a &= self._mem.r1

    def _exec_90(self):
        self._mem.a &= self._mem.r2

    def _exec_91(self):
        self._mem.a &= self._mem.r3

    def _exec_92(self):
        self._mem.a &= self._mem.r4

    def _exec_93(self):
        self._mem.a &= self._mem.r5

    def _exec_94(self):
        self._mem.a &= self._mem.r6

    def _exec_95(self):
        self._mem.a &= self._mem.r7

    def _exec_96(self, offset):
        if self._mem.a == 0:
            self.pc += offset

    def _exec_98(self, direct):
        self._mem[direct] ^= self._mem.a

    def _exec_99(self, direct, immed):
        self._mem[direct] ^= immed

    def _exec_100(self, immed):
        self._mem.a ^= immed

    def _exec_101(self, direct):
        self._mem.a ^= self._mem[direct]

    def _exec_102(self):
        self._mem.a ^= self._mem[self._mem.r0]

    def _exec_103(self):
        self._mem.a ^= self._mem[self._mem.r1]

    def _exec_104(self):
        self._mem.a ^= self._mem.r0

    def _exec_105(self):
        self._mem.a ^= self._mem.r1

    def _exec_106(self):
        self._mem.a ^= self._mem.r2

    def _exec_107(self):
        self._mem.a ^= self._mem.r3

    def _exec_108(self):
        self._mem.a ^= self._mem.r4

    def _exec_109(self):
        self._mem.a ^= self._mem.r5

    def _exec_110(self):
        self._mem.a ^= self._mem.r6

    def _exec_111(self):
        self._mem.a ^= self._mem.r7

    def _exec_112(self, offset):
        if self._mem.a != 0:
            self.pc += offset

    def _exec_115(self):
        self.pc = self._mem.dptr + self._mem.a

    def _exec_116(self, immed):
        self._mem.a = immed

    def _exec_117(self, direct, immed):
        self._mem[direct] = immed

    def _exec_118(self, immed):
        self._mem[self._mem.r0] = immed

    def _exec_119(self, immed):
        self._mem[self._mem.r1] = immed

    def _exec_120(self, immed):
        self._mem.r0 = immed

    def _exec_121(self, immed):
        self._mem.r1 = immed

    def _exec_122(self, immed):
        self._mem.r2 = immed

    def _exec_123(self, immed):
        self._mem.r3 = immed

    def _exec_124(self, immed):
        self._mem.r4 = immed

    def _exec_125(self, immed):
        self._mem.r5 = immed

    def _exec_126(self, immed):
        self._mem.r6 = immed

    def _exec_127(self, immed):
        self._mem.r7 = immed

    def _exec_132(self):
        self._mem.a, self._mem.b = divmod(self._mem.a, self._mem.b)

    def _exec_133(self, src_direct, dest_direct):
        self._mem[dest_direct] = self._mem[src_direct]

    def _exec_134(self, direct):
        self._mem[direct] = self._mem[self._mem.r0]

    def _exec_135(self, direct):
        self._mem[direct] = self._mem[self._mem.r1]

    def _exec_136(self, direct):
        self._mem[direct] = self._mem.r0

    def _exec_137(self, direct):
        self._mem[direct] = self._mem.r1

    def _exec_138(self, direct):
        self._mem[direct] = self._mem.r2

    def _exec_139(self, direct):
        self._mem[direct] = self._mem.r3

    def _exec_140(self, direct):
        self._mem[direct] = self._mem.r4

    def _exec_141(self, direct):
        self._mem[direct] = self._mem.r5

    def _exec_142(self, direct):
        self._mem[direct] = self._mem.r6

    def _exec_143(self, direct):
        self._mem[direct] = self._mem.r7

    def _exec_144(self, immed):
        self._mem.dptr = immed

    def _exec_148(self, immed):
        self._mem.a -= self._mem.c + immed

    def _exec_149(self, direct):
        self._mem.a -= self._mem.c + self._mem[direct]

    def _exec_150(self):
        self._mem.a -= self._mem.c + self._mem[self._mem.r0]

    def _exec_151(self):
        self._mem.a -= self._mem.c + self._mem[self._mem.r1]

    def _exec_152(self):
        self._mem.a -= self._mem.c + self._mem.r0

    def _exec_153(self):
        self._mem.a -= self._mem.c + self._mem.r1

    def _exec_154(self):
        self._mem.a -= self._mem.c + self._mem.r2

    def _exec_155(self):
        self._mem.a -= self._mem.c + self._mem.r3

    def _exec_156(self):
        self._mem.a -= self._mem.c + self._mem.r4

    def _exec_157(self):
        self._mem.a -= self._mem.c + self._mem.r5

    def _exec_158(self):
        self._mem.a -= self._mem.c + self._mem.r6

    def _exec_159(self):
        self._mem.a -= self._mem.c + self._mem.r7

    def _exec_163(self):
        self._mem.dptr += 1

    def _exec_165(self):
        return

    def _exec_166(self, direct):
        self._mem[self._mem.r0] = self._mem[direct]

    def _exec_167(self, direct):
        self._mem[self._mem.r1] = self._mem[direct]

    def _exec_168(self, direct):
        self._mem.r0 = self._mem[direct]

    def _exec_169(self, direct):
        self._mem.r1 = self._mem[direct]

    def _exec_170(self, direct):
        self._mem.r2 = self._mem[direct]

    def _exec_171(self, direct):
        self._mem.r3 = self._mem[direct]

    def _exec_172(self, direct):
        self._mem.r4 = self._mem[direct]

    def _exec_173(self, direct):
        self._mem.r5 = self._mem[direct]

    def _exec_174(self, direct):
        self._mem.r6 = self._mem[direct]

    def _exec_175(self, direct):
        self._mem.r7 = self._mem[direct]

    def _exec_179(self):
        self._mem.c = not self._mem.c

    def _exec_180(self, immed, offset):
        if self._mem.a != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.a < immed else 0

    def _exec_181(self, direct, offset):
        if self._mem.a != self._mem[direct]:
            self.pc += offset
        self._mem.c = 1 if self._mem.a < self._mem[direct] else 0

    def _exec_182(self, immed, offset):
        if self._mem[self._mem.r0] != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem[self._mem.r0] < immed else 0

    def _exec_183(self, immed, offset):
        if self._mem[self._mem.r1] != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem[self._mem.r1] < immed else 0

    def _exec_184(self, immed, offset):
        if self._mem.r0 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r0 < immed else 0

    def _exec_185(self, immed, offset):
        if self._mem.r1 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r1 < immed else 0

    def _exec_186(self, immed, offset):
        if self._mem.r2 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r2 < immed else 0

    def _exec_187(self, immed, offset):
        if self._mem.r3 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r3 < immed else 0

    def _exec_188(self, immed, offset):
        if self._mem.r4 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r4 < immed else 0

    def _exec_189(self, immed, offset):
        if self._mem.r5 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r5 < immed else 0

    def _exec_190(self, immed, offset):
        if self._mem.r6 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r6 < immed else 0

    def _exec_191(self, immed, offset):
        if self._mem.r7 != immed:
            self.pc += offset
        self._mem.c = 1 if self._mem.r7 < immed else 0

    def _exec_195(self):
        self._mem.c = 0

    def _exec_211(self):
        self._mem.c = 1

    def _exec_213(self, direct, offset):
        self._mem[direct] -= 1
        if self._mem[direct] != 0:
            self.pc += offset

    def _exec_216(self, offset):
        self._mem.r0 -= 1
        if self._mem.r0 != 0:
            self.pc += offset

    def _exec_217(self, offset):
        self._mem.r1 -= 1
        if self._mem.r1 != 0:
            self.pc += offset

    def _exec_218(self, offset):
        self._mem.r2 -= 1
        if self._mem.r2 != 0:
            self.pc += offset

    def _exec_219(self, offset):
        self._mem.r3 -= 1
        if self._mem.r3 != 0:
            self.pc += offset

    def _exec_220(self, offset):
        self._mem.r4 -= 1
        if self._mem.r4 != 0:
            self.pc += offset

    def _exec_221(self, offset):
        self._mem.r5 -= 1
        if self._mem.r5 != 0:
            self.pc += offset

    def _exec_222(self, offset):
        self._mem.r6 -= 1
        if self._mem.r6 != 0:
            self.pc += offset

    def _exec_223(self, offset):
        self._mem.r7 -= 1
        if self._mem.r7 != 0:
            self.pc += offset

    def _exec_228(self):
        self._mem.a = 0

    def _exec_229(self, direct):
        self._mem.a = self._mem[direct]

    def _exec_230(self):
        self._mem.a = self._mem[self._mem.r0]

    def _exec_231(self):
        self._mem.a = self._mem[self._mem.r1]

    def _exec_232(self):
        self._mem.a = self._mem.r0

    def _exec_233(self):
        self._mem.a = self._mem.r1

    def _exec_234(self):
        self._mem.a = self._mem.r2

    def _exec_235(self):
        self._mem.a = self._mem.r3

    def _exec_236(self):
        self._mem.a = self._mem.r4

    def _exec_237(self):
        self._mem.a = self._mem.r5

    def _exec_238(self):
        self._mem.a = self._mem.r6

    def _exec_239(self):
        self._mem.a = self._mem.r7

    def _exec_244(self):
        self._mem.a ^= 255

    def _exec_245(self, direct):
        self._mem[direct] = self._mem.a

    def _exec_246(self):
        self._mem[self._mem.r0] = self._mem.a

    def _exec_247(self):
        self._mem[self._mem.r1] = self._mem.a

    def _exec_248(self):
        self._mem.r0 = self._mem.a

    def _exec_249(self):
        self._mem.r1 = self._mem.a

    def _exec_250(self):
        self._mem.r2 = self._mem.a

    def _exec_251(self):
        self._mem.r3 = self._mem.a

    def _exec_252(self):
        self._mem.r4 = self._mem.a

    def _exec_253(self):
        self._mem.r5 = self._mem.a

    def _exec_254(self):
        self._mem.r6 = self._mem.a

    def _exec_255(self):
        self._mem.r7 = self._mem.a


class ProgramMemory:
    def __init__(self):
        self._data = [0] * 64000  # 64 KB

    def __getitem__(self, addr: Union[int, 'DoubleByte', slice]):
        if isinstance(addr, slice):
            return self._data[int(addr.start):int(addr.stop)]
        return self._data[int(addr)]

    def __setitem__(self, addr: int, value: int):
        self._data[addr] = value


class DataMemory:
    def __init__(self):
        self._data = [Byte() for _ in range(256)]
        self._dptr = DoubleByte()
        self.sp = 7

    def __getitem__(self, addr: Union[int, 'Byte']):
        return self._data[int(addr)]

    def __setitem__(self, addr, value: Union[int, 'Byte']):
        self[addr].value = value

    @property
    def sp(self):
        return self[129]

    @sp.setter
    def sp(self, value):
        self[129].value = value

    @property
    def dptr(self):
        return self._dptr

    @dptr.setter
    def dptr(self, value: Union[int, 'Byte', 'DoubleByte']):
        self._dptr.value = value
        self[130].value = int(f'{int(value):016b}'[:8], 2)
        self[131].value = int(f'{int(value):016b}'[8:], 2)

    @property
    def tcon(self):
        return self[136]

    @tcon.setter
    def tcon(self, value):
        self[136].value = value

    @property
    def tf1(self):
        return self.tcon[0]

    @tf1.setter
    def tf1(self, value):
        self.tcon[0] = value

    @property
    def tr1(self):
        return self.tcon[1]

    @tr1.setter
    def tr1(self, value):
        self.tcon[1] = value

    @property
    def tf0(self):
        return self.tcon[2]

    @tf0.setter
    def tf0(self, value):
        self.tcon[2] = value

    @property
    def tr0(self):
        return self.tcon[3]

    @tr0.setter
    def tr0(self, value):
        self.tcon[3] = value

    @property
    def ie1(self):
        return self.tcon[4]

    @ie1.setter
    def ie1(self, value):
        self.tcon[4] = value

    @property
    def it1(self):
        return self.tcon[5]

    @it1.setter
    def it1(self, value):
        self.tcon[5] = value

    @property
    def ie0(self):
        return self.tcon[6]

    @ie0.setter
    def ie0(self, value):
        self.tcon[6] = value

    @property
    def it0(self):
        return self.tcon[7]

    @it0.setter
    def it0(self, value):
        self.tcon[7] = value

    @property
    def tmod(self):
        return self[137]

    @tmod.setter
    def tmod(self, value):
        self[137].value = value

    @property
    def t1_gate(self):
        return self.tmod[0]

    @t1_gate.setter
    def t1_gate(self, value):
        self.tmod[0] = value

    @property
    def t1_ct(self):
        return self.tmod[1]

    @t1_ct.setter
    def t1_ct(self, value):
        self.tmod[1] = value

    @property
    def t1_m1(self):
        return self.tmod[2]

    @t1_m1.setter
    def t1_m1(self, value):
        self.tmod[2] = value

    @property
    def t1_m0(self):
        return self.tmod[3]

    @t1_m0.setter
    def t1_m0(self, value):
        self.tmod[3] = value

    @property
    def t0_gate(self):
        return self.tmod[4]

    @t0_gate.setter
    def t0_gate(self, value):
        self.tmod[4] = value

    @property
    def t0_ct(self):
        return self.tmod[5]

    @t0_ct.setter
    def t0_ct(self, value):
        self.tmod[5] = value

    @property
    def t0_m1(self):
        return self.tmod[6]

    @t0_m1.setter
    def t0_m1(self, value):
        self.tmod[6] = value

    @property
    def t0_m0(self):
        return self.tmod[7]

    @t0_m0.setter
    def t0_m0(self, value):
        self.tmod[7] = value

    @property
    def tl0(self):
        return self[138]

    @tl0.setter
    def tl0(self, value):
        self[138].value = value

    @property
    def tl1(self):
        return self[139]

    @tl1.setter
    def tl1(self, value):
        self[139].value = value

    @property
    def th0(self):
        return self[140]

    @th0.setter
    def th0(self, value):
        self[140].value = value

    @property
    def th1(self):
        return self[141]

    @th1.setter
    def th1(self, value):
        self[141].value = value

    @property
    def ie(self):
        return self[168]

    @ie.setter
    def ie(self, value):
        self[168].value = value

    @property
    def ea(self):
        return self.ie[0]

    @ea.setter
    def ea(self, value):
        self.ie[0] = value

    @property
    def es(self):
        return self.ie[3]

    @es.setter
    def es(self, value):
        self.ie[3] = value

    @property
    def et1(self):
        return self.ie[4]

    @et1.setter
    def et1(self, value):
        self.ie[4] = value

    @property
    def ex1(self):
        return self.ie[5]

    @ex1.setter
    def ex1(self, value):
        self.ie[5] = value

    @property
    def et0(self):
        return self.ie[6]

    @et0.setter
    def et0(self, value):
        self.ie[6] = value

    @property
    def ex0(self):
        return self.ie[7]

    @ex0.setter
    def ex0(self, value):
        self.ie[7] = value

    @property
    def ip(self):
        return self[184]

    @ip.setter
    def ip(self, value):
        self[184].value = value

    @property
    def ps(self):
        return self.ip[3]

    @ps.setter
    def ps(self, value):
        self.ip[3] = value

    @property
    def pt1(self):
        return self.ip[4]

    @pt1.setter
    def pt1(self, value):
        self.ip[4] = value

    @property
    def px1(self):
        return self.ip[5]

    @px1.setter
    def px1(self, value):
        self.ip[5] = value

    @property
    def pt0(self):
        return self.ip[6]

    @pt0.setter
    def pt0(self, value):
        self.ip[6] = value

    @property
    def px0(self):
        return self.ip[7]

    @px0.setter
    def px0(self, value):
        self.ip[7] = value

    @property
    def a(self):
        return self[224]

    @a.setter
    def a(self, value):
        self[224].value = value

    @property
    def b(self):
        return self[240]

    @b.setter
    def b(self, value):
        self[240].value = value

    @property
    def psw(self):
        return self[208]

    @property
    def c(self):
        return self.psw[0]

    @c.setter
    def c(self, value: Union[int, bool]):
        self.psw[0] = int(value)

    @property
    def ac(self):
        return self.psw[1]

    @ac.setter
    def ac(self, value):
        self.psw[1] = value

    @property
    def rs1(self):
        return self.psw[3]

    @rs1.setter
    def rs1(self, value):
        self.psw[3] = value

    @property
    def rs2(self):
        return self.psw[4]

    @rs2.setter
    def rs2(self, value):
        self.psw[4] = value

    @property
    def ov(self):
        return self.psw[5]

    @ov.setter
    def ov(self, value):
        self.psw[5] = value

    @property
    def p(self):
        return self.psw[7]

    @p.setter
    def p(self, value):
        self.psw[7] = value

    @property
    def selected_register_bank(self):
        return 2 * self.rs1 + self.rs2

    @selected_register_bank.setter
    def selected_register_bank(self, value: int):
        self.rs1, self.rs2 = [int(bit) for bit in f'{value:02b}']

    @property
    def r0(self):
        return self[8 * self.selected_register_bank]

    @r0.setter
    def r0(self, value):
        self[8 * self.selected_register_bank].value = value

    @property
    def r1(self):
        return self[8 * self.selected_register_bank + 1]

    @r1.setter
    def r1(self, value):
        self[8 * self.selected_register_bank + 1].value = value

    @property
    def r2(self):
        return self[8 * self.selected_register_bank + 2]

    @r2.setter
    def r2(self, value):
        self[8 * self.selected_register_bank + 2].value = value

    @property
    def r3(self):
        return self[8 * self.selected_register_bank + 3]

    @r3.setter
    def r3(self, value):
        self[8 * self.selected_register_bank + 3].value = value

    @property
    def r4(self):
        return self[8 * self.selected_register_bank + 4]

    @r4.setter
    def r4(self, value):
        self[8 * self.selected_register_bank + 4].value = value

    @property
    def r5(self):
        return self[8 * self.selected_register_bank + 5]

    @r5.setter
    def r5(self, value):
        self[8 * self.selected_register_bank + 5].value = value

    @property
    def r6(self):
        return self[8 * self.selected_register_bank + 6]

    @r6.setter
    def r6(self, value):
        self[8 * self.selected_register_bank + 6].value = value

    @property
    def r7(self):
        return self[8 * self.selected_register_bank + 7]

    @r7.setter
    def r7(self, value):
        self[8 * self.selected_register_bank + 7].value = value


class Byte:
    # Warning: big-endian
    def __init__(self, value=0):
        self.value = value

    def __getitem__(self, bit_number: int):
        return int(self.bits()[bit_number])

    def __setitem__(self, bit_number: int, bit_value: int):
        bits = self.bits()
        bits = bits[:bit_number] + str(bit_value) + bits[bit_number + 1:]
        self.value = int(bits, 2)

    def __setattr__(self, name, value: Union[int, 'Byte']):
        super(Byte, self).__setattr__(name, int(value) % 256)

    def __repr__(self):
        return f'{self.__class__.__name__}({int(self)})'

    def __format__(self, format_spec):
        return format(int(self), format_spec)

    def __int__(self):
        return self.value

    def __eq__(self, other: Union[int, 'Byte']):
        return int(self) == int(other)

    def __lt__(self, other: Union[int, 'Byte']):
        return int(self) < int(other)

    def __add__(self, other: Union[int, 'Byte']):
        return self.__class__(int(self) + int(other))

    def __radd__(self, other: int):
        return self.__add__(other)

    def __sub__(self, other: Union[int, 'Byte']):
        return self.__class__(int(self) - int(other))

    def __rsub__(self, other: int):
        return self.__class__(other - int(self))

    def __divmod__(self, other: Union[int, 'Byte']):
        return divmod(int(self), int(other))

    def __and__(self, other: Union[int, 'Byte']):
        return int(self) & int(other)

    def __or__(self, other: Union[int, 'Byte']):
        return int(self) | int(other)

    def __xor__(self, other: Union[int, 'Byte']):
        return int(self) ^ int(other)

    def bits(self):
        return f'{self:08b}'


class DoubleByte(Byte):
    def __setattr__(self, name, value: Union[int, 'DoubleByte']):
        super(Byte, self).__setattr__(name, int(value) % 65536)

    def bits(self):
        return f'{self:016b}'


class Operation:
    _opcodes = {
        0: {'bytes': 1, 'mnemonic': 'NOP'},
        1: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        2: {'bytes': 3, 'mnemonic': 'LJMP {:X}h'},
        3: {'bytes': 1, 'mnemonic': 'RR A'},
        4: {'bytes': 1, 'mnemonic': 'INC A'},
        5: {'bytes': 2, 'mnemonic': 'INC {:X}h'},
        6: {'bytes': 1, 'mnemonic': 'INC @R0'},
        7: {'bytes': 1, 'mnemonic': 'INC @R1'},
        8: {'bytes': 1, 'mnemonic': 'INC R0'},
        9: {'bytes': 1, 'mnemonic': 'INC R1'},
        10: {'bytes': 1, 'mnemonic': 'INC R2'},
        11: {'bytes': 1, 'mnemonic': 'INC R3'},
        12: {'bytes': 1, 'mnemonic': 'INC R4'},
        13: {'bytes': 1, 'mnemonic': 'INC R5'},
        14: {'bytes': 1, 'mnemonic': 'INC R6'},
        15: {'bytes': 1, 'mnemonic': 'INC R7'},
        16: {'bytes': 3, 'mnemonic': 'JBC {:X}h, {:X}h'},
        17: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        18: {'bytes': 3, 'mnemonic': 'LCALL {:X}h'},
        19: {'bytes': 1, 'mnemonic': 'RRC A'},
        20: {'bytes': 1, 'mnemonic': 'DEC A'},
        21: {'bytes': 2, 'mnemonic': 'DEC {:X}h'},
        22: {'bytes': 1, 'mnemonic': 'DEC @R0'},
        23: {'bytes': 1, 'mnemonic': 'DEC @R1'},
        24: {'bytes': 1, 'mnemonic': 'DEC R0'},
        25: {'bytes': 1, 'mnemonic': 'DEC R1'},
        26: {'bytes': 1, 'mnemonic': 'DEC R2'},
        27: {'bytes': 1, 'mnemonic': 'DEC R3'},
        28: {'bytes': 1, 'mnemonic': 'DEC R4'},
        29: {'bytes': 1, 'mnemonic': 'DEC R5'},
        30: {'bytes': 1, 'mnemonic': 'DEC R6'},
        31: {'bytes': 1, 'mnemonic': 'DEC R7'},
        32: {'bytes': 3, 'mnemonic': 'JB {:X}h, {:X}h'},
        33: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        34: {'bytes': 1, 'mnemonic': 'RET'},
        35: {'bytes': 1, 'mnemonic': 'RL A'},
        36: {'bytes': 2, 'mnemonic': 'ADD A, #{}'},
        37: {'bytes': 2, 'mnemonic': 'ADD A, {:X}h'},
        38: {'bytes': 1, 'mnemonic': 'ADD A, @R0'},
        39: {'bytes': 1, 'mnemonic': 'ADD A, @R1'},
        40: {'bytes': 1, 'mnemonic': 'ADD A, R0'},
        41: {'bytes': 1, 'mnemonic': 'ADD A, R1'},
        42: {'bytes': 1, 'mnemonic': 'ADD A, R2'},
        43: {'bytes': 1, 'mnemonic': 'ADD A, R3'},
        44: {'bytes': 1, 'mnemonic': 'ADD A, R4'},
        45: {'bytes': 1, 'mnemonic': 'ADD A, R5'},
        46: {'bytes': 1, 'mnemonic': 'ADD A, R6'},
        47: {'bytes': 1, 'mnemonic': 'ADD A, R7'},
        48: {'bytes': 3, 'mnemonic': 'JNB {:X}h, {:X}h'},
        49: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        50: {'bytes': 1, 'mnemonic': 'RETI'},
        51: {'bytes': 1, 'mnemonic': 'RLC A'},
        52: {'bytes': 2, 'mnemonic': 'ADDC A, #{}'},
        53: {'bytes': 2, 'mnemonic': 'ADDC A, {:X}h'},
        54: {'bytes': 1, 'mnemonic': 'ADDC A, @R0'},
        55: {'bytes': 1, 'mnemonic': 'ADDC A, @R1'},
        56: {'bytes': 1, 'mnemonic': 'ADDC A, R0'},
        57: {'bytes': 1, 'mnemonic': 'ADDC A, R1'},
        58: {'bytes': 1, 'mnemonic': 'ADDC A, R2'},
        59: {'bytes': 1, 'mnemonic': 'ADDC A, R3'},
        60: {'bytes': 1, 'mnemonic': 'ADDC A, R4'},
        61: {'bytes': 1, 'mnemonic': 'ADDC A, R5'},
        62: {'bytes': 1, 'mnemonic': 'ADDC A, R6'},
        63: {'bytes': 1, 'mnemonic': 'ADDC A, R7'},
        64: {'bytes': 2, 'mnemonic': 'JC {:X}h'},
        65: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        66: {'bytes': 2, 'mnemonic': 'ORL {:X}h, A'},
        67: {'bytes': 3, 'mnemonic': 'ORL {:X}h, #{}'},
        68: {'bytes': 2, 'mnemonic': 'ORL A, #{}'},
        69: {'bytes': 2, 'mnemonic': 'ORL A, {:X}h'},
        70: {'bytes': 1, 'mnemonic': 'ORL A, @R0'},
        71: {'bytes': 1, 'mnemonic': 'ORL A, @R1'},
        72: {'bytes': 1, 'mnemonic': 'ORL A, R0'},
        73: {'bytes': 1, 'mnemonic': 'ORL A, R1'},
        74: {'bytes': 1, 'mnemonic': 'ORL A, R2'},
        75: {'bytes': 1, 'mnemonic': 'ORL A, R3'},
        76: {'bytes': 1, 'mnemonic': 'ORL A, R4'},
        77: {'bytes': 1, 'mnemonic': 'ORL A, R5'},
        78: {'bytes': 1, 'mnemonic': 'ORL A, R6'},
        79: {'bytes': 1, 'mnemonic': 'ORL A, R7'},
        80: {'bytes': 2, 'mnemonic': 'JNC {:X}h'},
        81: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        82: {'bytes': 2, 'mnemonic': 'ANL {:X}h, A'},
        83: {'bytes': 3, 'mnemonic': 'ANL {:X}h, #{}'},
        84: {'bytes': 2, 'mnemonic': 'ANL A, #{}'},
        85: {'bytes': 2, 'mnemonic': 'ANL A, {:X}h'},
        86: {'bytes': 1, 'mnemonic': 'ANL A, @R0'},
        87: {'bytes': 1, 'mnemonic': 'ANL A, @R1'},
        88: {'bytes': 1, 'mnemonic': 'ANL A, R0'},
        89: {'bytes': 1, 'mnemonic': 'ANL A, R1'},
        90: {'bytes': 1, 'mnemonic': 'ANL A, R2'},
        91: {'bytes': 1, 'mnemonic': 'ANL A, R3'},
        92: {'bytes': 1, 'mnemonic': 'ANL A, R4'},
        93: {'bytes': 1, 'mnemonic': 'ANL A, R5'},
        94: {'bytes': 1, 'mnemonic': 'ANL A, R6'},
        95: {'bytes': 1, 'mnemonic': 'ANL A, R7'},
        96: {'bytes': 2, 'mnemonic': 'JZ {:X}h'},
        97: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        98: {'bytes': 2, 'mnemonic': 'XRL {:X}h, A'},
        99: {'bytes': 3, 'mnemonic': 'XRL {:X}h, #{}'},
        100: {'bytes': 2, 'mnemonic': 'XRL A, #{}'},
        101: {'bytes': 2, 'mnemonic': 'XRL A, {:X}h'},
        102: {'bytes': 1, 'mnemonic': 'XRL A, @R0'},
        103: {'bytes': 1, 'mnemonic': 'XRL A, @R1'},
        104: {'bytes': 1, 'mnemonic': 'XRL A, R0'},
        105: {'bytes': 1, 'mnemonic': 'XRL A, R1'},
        106: {'bytes': 1, 'mnemonic': 'XRL A, R2'},
        107: {'bytes': 1, 'mnemonic': 'XRL A, R3'},
        108: {'bytes': 1, 'mnemonic': 'XRL A, R4'},
        109: {'bytes': 1, 'mnemonic': 'XRL A, R5'},
        110: {'bytes': 1, 'mnemonic': 'XRL A, R6'},
        111: {'bytes': 1, 'mnemonic': 'XRL A, R7'},
        112: {'bytes': 2, 'mnemonic': 'JNZ {:X}h'},
        113: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        114: {'bytes': 2, 'mnemonic': 'ORL C, {:X}h'},
        115: {'bytes': 1, 'mnemonic': 'JMP @A+DPTR'},
        116: {'bytes': 2, 'mnemonic': 'MOV A, #{}'},
        117: {'bytes': 3, 'mnemonic': 'MOV {:X}h, #{}'},
        118: {'bytes': 2, 'mnemonic': 'MOV @R0, #{}'},
        119: {'bytes': 2, 'mnemonic': 'MOV @R1, #{}'},
        120: {'bytes': 2, 'mnemonic': 'MOV R0, #{}'},
        121: {'bytes': 2, 'mnemonic': 'MOV R1, #{}'},
        122: {'bytes': 2, 'mnemonic': 'MOV R2, #{}'},
        123: {'bytes': 2, 'mnemonic': 'MOV R3, #{}'},
        124: {'bytes': 2, 'mnemonic': 'MOV R4, #{}'},
        125: {'bytes': 2, 'mnemonic': 'MOV R5, #{}'},
        126: {'bytes': 2, 'mnemonic': 'MOV R6, #{}'},
        127: {'bytes': 2, 'mnemonic': 'MOV R7, #{}'},
        128: {'bytes': 2, 'mnemonic': 'SJMP {:X}h'},
        129: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        130: {'bytes': 2, 'mnemonic': 'ANL C, {:X}h'},
        131: {'bytes': 1, 'mnemonic': 'MOVC A, @A+PC'},
        132: {'bytes': 1, 'mnemonic': 'DIV AB'},
        133: {'bytes': 3, 'mnemonic': 'MOV {:X}h, {:X}h'},
        134: {'bytes': 2, 'mnemonic': 'MOV {:X}h, @R0'},
        135: {'bytes': 2, 'mnemonic': 'MOV {:X}h, @R1'},
        136: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R0'},
        137: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R1'},
        138: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R2'},
        139: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R3'},
        140: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R4'},
        141: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R5'},
        142: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R6'},
        143: {'bytes': 2, 'mnemonic': 'MOV {:X}h, R7'},
        144: {'bytes': 3, 'mnemonic': 'MOV DPTR, #{}'},
        145: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        146: {'bytes': 2, 'mnemonic': 'MOV {:X}h, C'},
        147: {'bytes': 1, 'mnemonic': 'MOVC A, @A+DPTR'},
        148: {'bytes': 2, 'mnemonic': 'SUBB A, #{}'},
        149: {'bytes': 2, 'mnemonic': 'SUBB A, {:X}h'},
        150: {'bytes': 1, 'mnemonic': 'SUBB A, @R0'},
        151: {'bytes': 1, 'mnemonic': 'SUBB A, @R1'},
        152: {'bytes': 1, 'mnemonic': 'SUBB A, R0'},
        153: {'bytes': 1, 'mnemonic': 'SUBB A, R1'},
        154: {'bytes': 1, 'mnemonic': 'SUBB A, R2'},
        155: {'bytes': 1, 'mnemonic': 'SUBB A, R3'},
        156: {'bytes': 1, 'mnemonic': 'SUBB A, R4'},
        157: {'bytes': 1, 'mnemonic': 'SUBB A, R5'},
        158: {'bytes': 1, 'mnemonic': 'SUBB A, R6'},
        159: {'bytes': 1, 'mnemonic': 'SUBB A, R7'},
        160: {'bytes': 2, 'mnemonic': 'ORL C, /{:X}h'},
        161: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        162: {'bytes': 2, 'mnemonic': 'MOV C, {:X}h'},
        163: {'bytes': 1, 'mnemonic': 'INC DPTR'},
        164: {'bytes': 1, 'mnemonic': 'MUL AB'},
        165: {'bytes': 1, 'mnemonic': None},
        166: {'bytes': 2, 'mnemonic': 'MOV @R0, {:X}h'},
        167: {'bytes': 2, 'mnemonic': 'MOV @R1, {:X}h'},
        168: {'bytes': 2, 'mnemonic': 'MOV R0, {:X}h'},
        169: {'bytes': 2, 'mnemonic': 'MOV R1, {:X}h'},
        170: {'bytes': 2, 'mnemonic': 'MOV R2, {:X}h'},
        171: {'bytes': 2, 'mnemonic': 'MOV R3, {:X}h'},
        172: {'bytes': 2, 'mnemonic': 'MOV R4, {:X}h'},
        173: {'bytes': 2, 'mnemonic': 'MOV R5, {:X}h'},
        174: {'bytes': 2, 'mnemonic': 'MOV R6, {:X}h'},
        175: {'bytes': 2, 'mnemonic': 'MOV R7, {:X}h'},
        176: {'bytes': 2, 'mnemonic': 'ANL C, /{:X}h'},
        177: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        178: {'bytes': 2, 'mnemonic': 'CPL {:X}h'},
        179: {'bytes': 1, 'mnemonic': 'CPL C'},
        180: {'bytes': 3, 'mnemonic': 'CJNE A, #{}, {:X}h'},
        181: {'bytes': 3, 'mnemonic': 'CJNE A, {:X}h, {:X}h'},
        182: {'bytes': 3, 'mnemonic': 'CJNE @R0, #{}, {:X}h'},
        183: {'bytes': 3, 'mnemonic': 'CJNE @R1, #{}, {:X}h'},
        184: {'bytes': 3, 'mnemonic': 'CJNE R0, #{}, {:X}h'},
        185: {'bytes': 3, 'mnemonic': 'CJNE R1, #{}, {:X}h'},
        186: {'bytes': 3, 'mnemonic': 'CJNE R2, #{}, {:X}h'},
        187: {'bytes': 3, 'mnemonic': 'CJNE R3, #{}, {:X}h'},
        188: {'bytes': 3, 'mnemonic': 'CJNE R4, #{}, {:X}h'},
        189: {'bytes': 3, 'mnemonic': 'CJNE R5, #{}, {:X}h'},
        190: {'bytes': 3, 'mnemonic': 'CJNE R6, #{}, {:X}h'},
        191: {'bytes': 3, 'mnemonic': 'CJNE R7, #{}, {:X}h'},
        192: {'bytes': 2, 'mnemonic': 'PUSH {:X}h'},
        193: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        194: {'bytes': 2, 'mnemonic': 'CLR {:X}h'},
        195: {'bytes': 1, 'mnemonic': 'CLR C'},
        196: {'bytes': 1, 'mnemonic': 'SWAP A'},
        197: {'bytes': 2, 'mnemonic': 'XCH A, {:X}h'},
        198: {'bytes': 1, 'mnemonic': 'XCH A, @R0'},
        199: {'bytes': 1, 'mnemonic': 'XCH A, @R1'},
        200: {'bytes': 1, 'mnemonic': 'XCH A, R0'},
        201: {'bytes': 1, 'mnemonic': 'XCH A, R1'},
        202: {'bytes': 1, 'mnemonic': 'XCH A, R2'},
        203: {'bytes': 1, 'mnemonic': 'XCH A, R3'},
        204: {'bytes': 1, 'mnemonic': 'XCH A, R4'},
        205: {'bytes': 1, 'mnemonic': 'XCH A, R5'},
        206: {'bytes': 1, 'mnemonic': 'XCH A, R6'},
        207: {'bytes': 1, 'mnemonic': 'XCH A, R7'},
        208: {'bytes': 2, 'mnemonic': 'POP {:X}h'},
        209: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        210: {'bytes': 2, 'mnemonic': 'SETB {:X}h'},
        211: {'bytes': 1, 'mnemonic': 'SETB C'},
        212: {'bytes': 1, 'mnemonic': 'DA A'},
        213: {'bytes': 3, 'mnemonic': 'DJNZ {:X}h, {:X}h'},
        214: {'bytes': 1, 'mnemonic': 'XCHD A, @R0'},
        215: {'bytes': 1, 'mnemonic': 'XCHD A, @R1'},
        216: {'bytes': 2, 'mnemonic': 'DJNZ R0, {:X}h'},
        217: {'bytes': 2, 'mnemonic': 'DJNZ R1, {:X}h'},
        218: {'bytes': 2, 'mnemonic': 'DJNZ R2, {:X}h'},
        219: {'bytes': 2, 'mnemonic': 'DJNZ R3, {:X}h'},
        220: {'bytes': 2, 'mnemonic': 'DJNZ R4, {:X}h'},
        221: {'bytes': 2, 'mnemonic': 'DJNZ R5, {:X}h'},
        222: {'bytes': 2, 'mnemonic': 'DJNZ R6, {:X}h'},
        223: {'bytes': 2, 'mnemonic': 'DJNZ R7, {:X}h'},
        224: {'bytes': 1, 'mnemonic': 'MOVX A, @DPTR'},
        225: {'bytes': 2, 'mnemonic': 'AJMP {:X}h'},
        226: {'bytes': 1, 'mnemonic': 'MOVX A, @R0'},
        227: {'bytes': 1, 'mnemonic': 'MOVX A, @R1'},
        228: {'bytes': 1, 'mnemonic': 'CLR A'},
        229: {'bytes': 2, 'mnemonic': 'MOV A, {:X}h'},
        230: {'bytes': 1, 'mnemonic': 'MOV A, @R0'},
        231: {'bytes': 1, 'mnemonic': 'MOV A, @R1'},
        232: {'bytes': 1, 'mnemonic': 'MOV A, R0'},
        233: {'bytes': 1, 'mnemonic': 'MOV A, R1'},
        234: {'bytes': 1, 'mnemonic': 'MOV A, R2'},
        235: {'bytes': 1, 'mnemonic': 'MOV A, R3'},
        236: {'bytes': 1, 'mnemonic': 'MOV A, R4'},
        237: {'bytes': 1, 'mnemonic': 'MOV A, R5'},
        238: {'bytes': 1, 'mnemonic': 'MOV A, R6'},
        239: {'bytes': 1, 'mnemonic': 'MOV A, R7'},
        240: {'bytes': 1, 'mnemonic': 'MOVX @DPTR, A'},
        241: {'bytes': 2, 'mnemonic': 'ACALL {:X}h'},
        242: {'bytes': 1, 'mnemonic': 'MOVX @R0, A'},
        243: {'bytes': 1, 'mnemonic': 'MOVX @R1, A'},
        244: {'bytes': 1, 'mnemonic': 'CPL A'},
        245: {'bytes': 2, 'mnemonic': 'MOV {:X}h, A'},
        246: {'bytes': 1, 'mnemonic': 'MOV @R0, A'},
        247: {'bytes': 1, 'mnemonic': 'MOV @R1, A'},
        248: {'bytes': 1, 'mnemonic': 'MOV R0, A'},
        249: {'bytes': 1, 'mnemonic': 'MOV R1, A'},
        250: {'bytes': 1, 'mnemonic': 'MOV R2, A'},
        251: {'bytes': 1, 'mnemonic': 'MOV R3, A'},
        252: {'bytes': 1, 'mnemonic': 'MOV R4, A'},
        253: {'bytes': 1, 'mnemonic': 'MOV R5, A'},
        254: {'bytes': 1, 'mnemonic': 'MOV R6, A'},
        255: {'bytes': 1, 'mnemonic': 'MOV R7, A'}
    }

    def __init__(self, opcode: int, *args: int):
        self.opcode = opcode
        self.args = args

    def __len__(self):
        return self._opcodes[self.opcode]['bytes']

    def __str__(self):
        # Turn two one-byte arguments (as stored in a .hex file) into one two-byte argument
        # e.g. 0xAB = 171, 0xCD = 205; 171 * 16 ** 2 + 205 = 43981 = 0xABCD
        args = [self.args[0] * 16 ** 2 + self.args[1]] if self.opcode in (2, 18, 144) else self.args
        return Operation._opcodes[self.opcode]['mnemonic'].format(*args)


class Stack:
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.pop()

    def top(self):
        return self._data[-1]
