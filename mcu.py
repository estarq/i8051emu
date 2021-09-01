from typing import Union
import disassembler


class Microcontroller:
    def __init__(self):
        self._rom = [0] * 64000  # 64 KB
        self._mem = DataMemory()
        self._pc = DoubleByte()

    def __call__(self):
        while True:
            op = Operation(self._rom[self.pc])
            op.args = self._rom[self.pc + 1:self.pc + len(op)]
            self.pc += len(op)
            # Jump operations may override the PC
            exec(f'self._exec_{op.opcode}(*op.args)')

    @property
    def pc(self):
        return int(self._pc)

    @pc.setter
    def pc(self, value):
        self._pc.value = value

    def load_hex_file(self, filepath):
        for record in disassembler.IntelHexFile(filepath):
            for addr, byte in enumerate(record, record.first_byte_addr):
                self._rom[addr] = byte

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

    def _exec_52(self, immed):
        self._mem.a += self._mem.c + immed

    def _exec_53(self, direct):
        self._mem.a += self._mem.c + self._mem[direct]

    def _exec_54(self):
        self._mem.a += self._mem.c + self._mem[self._mem.r0]

    def _exec_55(self):
        self._mem.a += self._mem.c + self._mem[self._mem.r1]


class DataMemory:
    def __init__(self):
        self._data = [Byte() for _ in range(256)]
        self._dptr = DoubleByte()

    def __getitem__(self, addr):
        return self._data[int(addr)]

    def __setitem__(self, addr, value: int):
        self[addr].value = value

    @property
    def dptr(self):
        return int(self._dptr)

    @dptr.setter
    def dptr(self, value):
        self._dptr.value = value
        self[130].value = int(f'{value:016b}'[:8], 2)
        self[131].value = int(f'{value:016b}'[8:], 2)

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
    def c(self, value):
        self.psw[0] = value

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
    def selected_register_bank(self, value):
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

    def __getitem__(self, bit_number):
        return int(self.bits()[bit_number])

    def __setitem__(self, bit_number, bit_value: int):
        bits = self.bits()
        bits = bits[:bit_number] + str(bit_value) + bits[bit_number + 1:]
        self.value = int(bits, 2)

    def __setattr__(self, name, value: int):
        super(Byte, self).__setattr__(name, value % 256)

    def __repr__(self):
        return f'{self.__class__.__name__}({int(self)})'

    def __int__(self):
        return self.value

    def __eq__(self, other: int):
        return int(self) == other

    def __add__(self, other: Union[int, 'Byte']):
        return self.__class__(int(self) + int(other))

    def __radd__(self, other: int):
        return self.__add__(other)

    def __sub__(self, other: Union[int, 'Byte']):
        return self.__class__(int(self) - int(other))

    def __rsub__(self, other: int):
        return self.__class__(other - int(self))

    def __mod__(self, other: int):
        return int(self) % other

    def __divmod__(self, other: 'Byte'):
        return divmod(int(self), int(other))

    def bits(self):
        return f'{int(self):08b}'


class DoubleByte(Byte):
    def __init__(self, value=0):
        super().__init__(value)

    def __setattr__(self, name, value: int):
        super(Byte, self).__setattr__(name, value % 65536)

    def bits(self):
        return f'{int(self):016b}'


class Operation:
    _opcodes = {
        0: {'length': 1, 'mnemonic': 'NOP'},
        1: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        2: {'length': 3, 'mnemonic': 'LJMP {:X}h'},
        3: {'length': 1, 'mnemonic': 'RR A'},
        4: {'length': 1, 'mnemonic': 'INC A'},
        5: {'length': 2, 'mnemonic': 'INC {:X}h'},
        6: {'length': 1, 'mnemonic': 'INC @R0'},
        7: {'length': 1, 'mnemonic': 'INC @R1'},
        8: {'length': 1, 'mnemonic': 'INC R0'},
        9: {'length': 1, 'mnemonic': 'INC R1'},
        10: {'length': 1, 'mnemonic': 'INC R2'},
        11: {'length': 1, 'mnemonic': 'INC R3'},
        12: {'length': 1, 'mnemonic': 'INC R4'},
        13: {'length': 1, 'mnemonic': 'INC R5'},
        14: {'length': 1, 'mnemonic': 'INC R6'},
        15: {'length': 1, 'mnemonic': 'INC R7'},
        16: {'length': 3, 'mnemonic': 'JBC {:X}h, {:X}h'},
        17: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        18: {'length': 3, 'mnemonic': 'LCALL {:X}h'},
        19: {'length': 1, 'mnemonic': 'RRC A'},
        20: {'length': 1, 'mnemonic': 'DEC A'},
        21: {'length': 2, 'mnemonic': 'DEC {:X}h'},
        22: {'length': 1, 'mnemonic': 'DEC @R0'},
        23: {'length': 1, 'mnemonic': 'DEC @R1'},
        24: {'length': 1, 'mnemonic': 'DEC R0'},
        25: {'length': 1, 'mnemonic': 'DEC R1'},
        26: {'length': 1, 'mnemonic': 'DEC R2'},
        27: {'length': 1, 'mnemonic': 'DEC R3'},
        28: {'length': 1, 'mnemonic': 'DEC R4'},
        29: {'length': 1, 'mnemonic': 'DEC R5'},
        30: {'length': 1, 'mnemonic': 'DEC R6'},
        31: {'length': 1, 'mnemonic': 'DEC R7'},
        32: {'length': 3, 'mnemonic': 'JB {:X}h, {:X}h'},
        33: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        34: {'length': 1, 'mnemonic': 'RET'},
        35: {'length': 1, 'mnemonic': 'RL A'},
        36: {'length': 2, 'mnemonic': 'ADD A, #{}'},
        37: {'length': 2, 'mnemonic': 'ADD A, {:X}h'},
        38: {'length': 1, 'mnemonic': 'ADD A, @R0'},
        39: {'length': 1, 'mnemonic': 'ADD A, @R1'},
        40: {'length': 1, 'mnemonic': 'ADD A, R0'},
        41: {'length': 1, 'mnemonic': 'ADD A, R1'},
        42: {'length': 1, 'mnemonic': 'ADD A, R2'},
        43: {'length': 1, 'mnemonic': 'ADD A, R3'},
        44: {'length': 1, 'mnemonic': 'ADD A, R4'},
        45: {'length': 1, 'mnemonic': 'ADD A, R5'},
        46: {'length': 1, 'mnemonic': 'ADD A, R6'},
        47: {'length': 1, 'mnemonic': 'ADD A, R7'},
        48: {'length': 3, 'mnemonic': 'JNB {:X}h, {:X}h'},
        49: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        50: {'length': 1, 'mnemonic': 'RETI'},
        51: {'length': 1, 'mnemonic': 'RLC A'},
        52: {'length': 2, 'mnemonic': 'ADDC A, #{}'},
        53: {'length': 2, 'mnemonic': 'ADDC A, {:X}h'},
        54: {'length': 1, 'mnemonic': 'ADDC A, @R0'},
        55: {'length': 1, 'mnemonic': 'ADDC A, @R1'},
        56: {'length': 1, 'mnemonic': 'ADDC A, R0'},
        57: {'length': 1, 'mnemonic': 'ADDC A, R1'},
        58: {'length': 1, 'mnemonic': 'ADDC A, R2'},
        59: {'length': 1, 'mnemonic': 'ADDC A, R3'},
        60: {'length': 1, 'mnemonic': 'ADDC A, R4'},
        61: {'length': 1, 'mnemonic': 'ADDC A, R5'},
        62: {'length': 1, 'mnemonic': 'ADDC A, R6'},
        63: {'length': 1, 'mnemonic': 'ADDC A, R7'},
        64: {'length': 2, 'mnemonic': 'JC {:X}h'},
        65: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        66: {'length': 2, 'mnemonic': 'ORL {:X}h, A'},
        67: {'length': 3, 'mnemonic': 'ORL {:X}h, #{}'},
        68: {'length': 2, 'mnemonic': 'ORL A, #{}'},
        69: {'length': 2, 'mnemonic': 'ORL A, {:X}h'},
        70: {'length': 1, 'mnemonic': 'ORL A, @R0'},
        71: {'length': 1, 'mnemonic': 'ORL A, @R1'},
        72: {'length': 1, 'mnemonic': 'ORL A, R0'},
        73: {'length': 1, 'mnemonic': 'ORL A, R1'},
        74: {'length': 1, 'mnemonic': 'ORL A, R2'},
        75: {'length': 1, 'mnemonic': 'ORL A, R3'},
        76: {'length': 1, 'mnemonic': 'ORL A, R4'},
        77: {'length': 1, 'mnemonic': 'ORL A, R5'},
        78: {'length': 1, 'mnemonic': 'ORL A, R6'},
        79: {'length': 1, 'mnemonic': 'ORL A, R7'},
        80: {'length': 2, 'mnemonic': 'JNC {:X}h'},
        81: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        82: {'length': 2, 'mnemonic': 'ANL {:X}h, A'},
        83: {'length': 3, 'mnemonic': 'ANL {:X}h, #{}'},
        84: {'length': 2, 'mnemonic': 'ANL A, #{}'},
        85: {'length': 2, 'mnemonic': 'ANL A, {:X}h'},
        86: {'length': 1, 'mnemonic': 'ANL A, @R0'},
        87: {'length': 1, 'mnemonic': 'ANL A, @R1'},
        88: {'length': 1, 'mnemonic': 'ANL A, R0'},
        89: {'length': 1, 'mnemonic': 'ANL A, R1'},
        90: {'length': 1, 'mnemonic': 'ANL A, R2'},
        91: {'length': 1, 'mnemonic': 'ANL A, R3'},
        92: {'length': 1, 'mnemonic': 'ANL A, R4'},
        93: {'length': 1, 'mnemonic': 'ANL A, R5'},
        94: {'length': 1, 'mnemonic': 'ANL A, R6'},
        95: {'length': 1, 'mnemonic': 'ANL A, R7'},
        96: {'length': 2, 'mnemonic': 'JZ {:X}h'},
        97: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        98: {'length': 2, 'mnemonic': 'XRL {:X}h, A'},
        99: {'length': 3, 'mnemonic': 'XRL {:X}h, #{}'},
        100: {'length': 2, 'mnemonic': 'XRL A, #{}'},
        101: {'length': 2, 'mnemonic': 'XRL A, {:X}h'},
        102: {'length': 1, 'mnemonic': 'XRL A, @R0'},
        103: {'length': 1, 'mnemonic': 'XRL A, @R1'},
        104: {'length': 1, 'mnemonic': 'XRL A, R0'},
        105: {'length': 1, 'mnemonic': 'XRL A, R1'},
        106: {'length': 1, 'mnemonic': 'XRL A, R2'},
        107: {'length': 1, 'mnemonic': 'XRL A, R3'},
        108: {'length': 1, 'mnemonic': 'XRL A, R4'},
        109: {'length': 1, 'mnemonic': 'XRL A, R5'},
        110: {'length': 1, 'mnemonic': 'XRL A, R6'},
        111: {'length': 1, 'mnemonic': 'XRL A, R7'},
        112: {'length': 2, 'mnemonic': 'JNZ {:X}h'},
        113: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        114: {'length': 2, 'mnemonic': 'ORL C, {:X}h'},
        115: {'length': 1, 'mnemonic': 'JMP @A+DPTR'},
        116: {'length': 2, 'mnemonic': 'MOV A, #{}'},
        117: {'length': 3, 'mnemonic': 'MOV {:X}h, #{}'},
        118: {'length': 2, 'mnemonic': 'MOV @R0, #{}'},
        119: {'length': 2, 'mnemonic': 'MOV @R1, #{}'},
        120: {'length': 2, 'mnemonic': 'MOV R0, #{}'},
        121: {'length': 2, 'mnemonic': 'MOV R1, #{}'},
        122: {'length': 2, 'mnemonic': 'MOV R2, #{}'},
        123: {'length': 2, 'mnemonic': 'MOV R3, #{}'},
        124: {'length': 2, 'mnemonic': 'MOV R4, #{}'},
        125: {'length': 2, 'mnemonic': 'MOV R5, #{}'},
        126: {'length': 2, 'mnemonic': 'MOV R6, #{}'},
        127: {'length': 2, 'mnemonic': 'MOV R7, #{}'},
        128: {'length': 2, 'mnemonic': 'SJMP {:X}h'},
        129: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        130: {'length': 2, 'mnemonic': 'ANL C, {:X}h'},
        131: {'length': 1, 'mnemonic': 'MOVC A, @A+PC'},
        132: {'length': 1, 'mnemonic': 'DIV AB'},
        133: {'length': 3, 'mnemonic': 'MOV {:X}h, {:X}h'},
        134: {'length': 2, 'mnemonic': 'MOV {:X}h, @R0'},
        135: {'length': 2, 'mnemonic': 'MOV {:X}h, @R1'},
        136: {'length': 2, 'mnemonic': 'MOV {:X}h, R0'},
        137: {'length': 2, 'mnemonic': 'MOV {:X}h, R1'},
        138: {'length': 2, 'mnemonic': 'MOV {:X}h, R2'},
        139: {'length': 2, 'mnemonic': 'MOV {:X}h, R3'},
        140: {'length': 2, 'mnemonic': 'MOV {:X}h, R4'},
        141: {'length': 2, 'mnemonic': 'MOV {:X}h, R5'},
        142: {'length': 2, 'mnemonic': 'MOV {:X}h, R6'},
        143: {'length': 2, 'mnemonic': 'MOV {:X}h, R7'},
        144: {'length': 3, 'mnemonic': 'MOV DPTR, #{}'},
        145: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        146: {'length': 2, 'mnemonic': 'MOV {:X}h, C'},
        147: {'length': 1, 'mnemonic': 'MOVC A, @A+DPTR'},
        148: {'length': 2, 'mnemonic': 'SUBB A, #{}'},
        149: {'length': 2, 'mnemonic': 'SUBB A, {:X}h'},
        150: {'length': 1, 'mnemonic': 'SUBB A, @R0'},
        151: {'length': 1, 'mnemonic': 'SUBB A, @R1'},
        152: {'length': 1, 'mnemonic': 'SUBB A, R0'},
        153: {'length': 1, 'mnemonic': 'SUBB A, R1'},
        154: {'length': 1, 'mnemonic': 'SUBB A, R2'},
        155: {'length': 1, 'mnemonic': 'SUBB A, R3'},
        156: {'length': 1, 'mnemonic': 'SUBB A, R4'},
        157: {'length': 1, 'mnemonic': 'SUBB A, R5'},
        158: {'length': 1, 'mnemonic': 'SUBB A, R6'},
        159: {'length': 1, 'mnemonic': 'SUBB A, R7'},
        160: {'length': 2, 'mnemonic': 'ORL C, /{:X}h'},
        161: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        162: {'length': 2, 'mnemonic': 'MOV C, {:X}h'},
        163: {'length': 1, 'mnemonic': 'INC DPTR'},
        164: {'length': 1, 'mnemonic': 'MUL AB'},
        165: {'length': 1, 'mnemonic': None},
        166: {'length': 2, 'mnemonic': 'MOV @R0, {:X}h'},
        167: {'length': 2, 'mnemonic': 'MOV @R1, {:X}h'},
        168: {'length': 2, 'mnemonic': 'MOV R0, {:X}h'},
        169: {'length': 2, 'mnemonic': 'MOV R1, {:X}h'},
        170: {'length': 2, 'mnemonic': 'MOV R2, {:X}h'},
        171: {'length': 2, 'mnemonic': 'MOV R3, {:X}h'},
        172: {'length': 2, 'mnemonic': 'MOV R4, {:X}h'},
        173: {'length': 2, 'mnemonic': 'MOV R5, {:X}h'},
        174: {'length': 2, 'mnemonic': 'MOV R6, {:X}h'},
        175: {'length': 2, 'mnemonic': 'MOV R7, {:X}h'},
        176: {'length': 2, 'mnemonic': 'ANL C, /{:X}h'},
        177: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        178: {'length': 2, 'mnemonic': 'CPL {:X}h'},
        179: {'length': 1, 'mnemonic': 'CPL C'},
        180: {'length': 3, 'mnemonic': 'CJNE A, #{}, {:X}h'},
        181: {'length': 3, 'mnemonic': 'CJNE A, {:X}h, {:X}h'},
        182: {'length': 3, 'mnemonic': 'CJNE @R0, #{}, {:X}h'},
        183: {'length': 3, 'mnemonic': 'CJNE @R1, #{}, {:X}h'},
        184: {'length': 3, 'mnemonic': 'CJNE R0, #{}, {:X}h'},
        185: {'length': 3, 'mnemonic': 'CJNE R1, #{}, {:X}h'},
        186: {'length': 3, 'mnemonic': 'CJNE R2, #{}, {:X}h'},
        187: {'length': 3, 'mnemonic': 'CJNE R3, #{}, {:X}h'},
        188: {'length': 3, 'mnemonic': 'CJNE R4, #{}, {:X}h'},
        189: {'length': 3, 'mnemonic': 'CJNE R5, #{}, {:X}h'},
        190: {'length': 3, 'mnemonic': 'CJNE R6, #{}, {:X}h'},
        191: {'length': 3, 'mnemonic': 'CJNE R7, #{}, {:X}h'},
        192: {'length': 2, 'mnemonic': 'PUSH {:X}h'},
        193: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        194: {'length': 2, 'mnemonic': 'CLR {:X}h'},
        195: {'length': 1, 'mnemonic': 'CLR C'},
        196: {'length': 1, 'mnemonic': 'SWAP A'},
        197: {'length': 2, 'mnemonic': 'XCH A, {:X}h'},
        198: {'length': 1, 'mnemonic': 'XCH A, @R0'},
        199: {'length': 1, 'mnemonic': 'XCH A, @R1'},
        200: {'length': 1, 'mnemonic': 'XCH A, R0'},
        201: {'length': 1, 'mnemonic': 'XCH A, R1'},
        202: {'length': 1, 'mnemonic': 'XCH A, R2'},
        203: {'length': 1, 'mnemonic': 'XCH A, R3'},
        204: {'length': 1, 'mnemonic': 'XCH A, R4'},
        205: {'length': 1, 'mnemonic': 'XCH A, R5'},
        206: {'length': 1, 'mnemonic': 'XCH A, R6'},
        207: {'length': 1, 'mnemonic': 'XCH A, R7'},
        208: {'length': 2, 'mnemonic': 'POP {:X}h'},
        209: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        210: {'length': 2, 'mnemonic': 'SETB {:X}h'},
        211: {'length': 1, 'mnemonic': 'SETB C'},
        212: {'length': 1, 'mnemonic': 'DA A'},
        213: {'length': 3, 'mnemonic': 'DJNZ {:X}h, {:X}h'},
        214: {'length': 1, 'mnemonic': 'XCHD A, @R0'},
        215: {'length': 1, 'mnemonic': 'XCHD A, @R1'},
        216: {'length': 2, 'mnemonic': 'DJNZ R0, {:X}h'},
        217: {'length': 2, 'mnemonic': 'DJNZ R1, {:X}h'},
        218: {'length': 2, 'mnemonic': 'DJNZ R2, {:X}h'},
        219: {'length': 2, 'mnemonic': 'DJNZ R3, {:X}h'},
        220: {'length': 2, 'mnemonic': 'DJNZ R4, {:X}h'},
        221: {'length': 2, 'mnemonic': 'DJNZ R5, {:X}h'},
        222: {'length': 2, 'mnemonic': 'DJNZ R6, {:X}h'},
        223: {'length': 2, 'mnemonic': 'DJNZ R7, {:X}h'},
        224: {'length': 1, 'mnemonic': 'MOVX A, @DPTR'},
        225: {'length': 2, 'mnemonic': 'AJMP {:X}h'},
        226: {'length': 1, 'mnemonic': 'MOVX A, @R0'},
        227: {'length': 1, 'mnemonic': 'MOVX A, @R1'},
        228: {'length': 1, 'mnemonic': 'CLR A'},
        229: {'length': 2, 'mnemonic': 'MOV A, {:X}h'},
        230: {'length': 1, 'mnemonic': 'MOV A, @R0'},
        231: {'length': 1, 'mnemonic': 'MOV A, @R1'},
        232: {'length': 1, 'mnemonic': 'MOV A, R0'},
        233: {'length': 1, 'mnemonic': 'MOV A, R1'},
        234: {'length': 1, 'mnemonic': 'MOV A, R2'},
        235: {'length': 1, 'mnemonic': 'MOV A, R3'},
        236: {'length': 1, 'mnemonic': 'MOV A, R4'},
        237: {'length': 1, 'mnemonic': 'MOV A, R5'},
        238: {'length': 1, 'mnemonic': 'MOV A, R6'},
        239: {'length': 1, 'mnemonic': 'MOV A, R7'},
        240: {'length': 1, 'mnemonic': 'MOVX @DPTR, A'},
        241: {'length': 2, 'mnemonic': 'ACALL {:X}h'},
        242: {'length': 1, 'mnemonic': 'MOVX @R0, A'},
        243: {'length': 1, 'mnemonic': 'MOVX @R1, A'},
        244: {'length': 1, 'mnemonic': 'CPL A'},
        245: {'length': 2, 'mnemonic': 'MOV {:X}h, A'},
        246: {'length': 1, 'mnemonic': 'MOV @R0, A'},
        247: {'length': 1, 'mnemonic': 'MOV @R1, A'},
        248: {'length': 1, 'mnemonic': 'MOV R0, A'},
        249: {'length': 1, 'mnemonic': 'MOV R1, A'},
        250: {'length': 1, 'mnemonic': 'MOV R2, A'},
        251: {'length': 1, 'mnemonic': 'MOV R3, A'},
        252: {'length': 1, 'mnemonic': 'MOV R4, A'},
        253: {'length': 1, 'mnemonic': 'MOV R5, A'},
        254: {'length': 1, 'mnemonic': 'MOV R6, A'},
        255: {'length': 1, 'mnemonic': 'MOV R7, A'}
    }

    def __init__(self, opcode: int, *args: int):
        self.opcode = opcode
        self.args = args

    def __len__(self):
        return self._opcodes[self.opcode]['length']

    def __str__(self):
        # Turn two one-byte arguments (as stored in a .hex file) into one two-byte argument
        # e.g. 0xAB = 171, 0xCD = 205; 171 * 16 ** 2 + 205 = 43981 = 0xABCD
        args = [self.args[0] * 16 ** 2 + self.args[1]] if self.opcode in (2, 18, 144) else self.args
        return Operation._opcodes[self.opcode]['mnemonic'].format(*args)
