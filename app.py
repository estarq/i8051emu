from browser import window

import disassembler
import mcu

m = mcu.Microcontroller()


def disassemble_to_window_assRows(file_content):
    window.assRows = [
        {
            'addr': addr,
            'bytes': bytes_,
            'opcode': opcode,
            'arg1': args[0] if args else '-',
            'arg2': args[1] if len(args) == 2 else '-',
            'mnemonic': mnemonic
        }
        for addr, bytes_, opcode, args, mnemonic
        in disassembler.disassemble(file_content)
    ]


def mcu_load_hex_file(file_content):
    m.load_hex_file(file_content)


def mcu_next_cycle():
    m.next_cycle()


def mcu_reset_rom():
    m.reset_rom()


def mcu_reset_ram():
    m.reset_ram()


def mcu_update_window_currentAddr():
    window.currentAddr = int(m.pc)


def mcu_update_window_memCells():
    if window.memType == 'ROM':
        window.memCells = [
            {'addr': addr, 'value': m.rom[addr]} for addr in range(1000)
        ]
    elif window.memType == 'RAM':
        window.memCells = [
            {'addr': addr, 'value': int(m.mem[addr])} for addr in range(256)
        ]
    elif window.memType == 'XRAM':
        window.memCells = [
            {'addr': addr, 'value': int(m.xmem[addr])} for addr in range(1000)
        ]


def mcu_update_window_keyRegs():
    window.keyRegs = [
        {'name': 'A', 'value': int(m.mem.a)},
        {'name': 'B', 'value': int(m.mem.b)},
        {'name': 'SP', 'value': int(m.mem.sp)},
        {'name': 'PC', 'value': int(m.pc)},
        {'name': 'DPTR', 'value': int(m.mem.dptr)},
        {'name': 'TH0', 'value': int(m.mem.th0)},
        {'name': 'TL0', 'value': int(m.mem.tl0)},
        {'name': 'TH1', 'value': int(m.mem.th1)},
        {'name': 'TL1', 'value': int(m.mem.tl1)},
        {'name': 'R0', 'value': int(m.mem.r0)},
        {'name': 'R1', 'value': int(m.mem.r1)},
        {'name': 'R2', 'value': int(m.mem.r2)},
        {'name': 'R3', 'value': int(m.mem.r3)},
        {'name': 'R4', 'value': int(m.mem.r4)},
        {'name': 'R5', 'value': int(m.mem.r5)},
        {'name': 'R6', 'value': int(m.mem.r6)},
        {'name': 'R7', 'value': int(m.mem.r7)},
    ]


def mcu_update_window_flags():
    window.flags = {
        'EA': m.mem.ea,
        'ES': m.mem.es,
        'ET1': m.mem.et1,
        'EX1': m.mem.ex1,
        'ET0': m.mem.et0,
        'EX0': m.mem.ex0,
        'PS': m.mem.ps,
        'PT1': m.mem.pt1,
        'PX1': m.mem.px1,
        'PT0': m.mem.pt0,
        'PX0': m.mem.px0,
        'C': m.mem.c,
        'AC': m.mem.ac,
        'F0': m.mem.f0,
        'RS1': m.mem.rs1,
        'RS0': m.mem.rs0,
        'OV': m.mem.ov,
        'F1': m.mem.f1,
        'P': m.mem.p,
        'TF1': m.mem.tf1,
        'TR1': m.mem.tr1,
        'TF0': m.mem.tf0,
        'TR0': m.mem.tr0,
        'IE1': m.mem.ie1,
        'IT1': m.mem.it1,
        'IE0': m.mem.ie0,
        'IT0': m.mem.it0,
        'T1_GATE': m.mem.t1_gate,
        'T1_CT': m.mem.t1_ct,
        'T1_M1': m.mem.t1_m1,
        'T1_M0': m.mem.t1_m0,
        'T0_GATE': m.mem.t0_gate,
        'T0_CT': m.mem.t0_ct,
        'T0_M1': m.mem.t0_m1,
        'T0_M0': m.mem.t0_m0,
    }


def mcu_update_window_extDevsRegs():
    window.extDevsRegs = [
        {'name': 'CSDS', 'bits': list(m.xmem.csds.bits)},
        {'name': 'CSDB', 'bits': list(m.xmem.csdb.bits)},
        {'name': 'CSKB0', 'bits': list(m.xmem.cskb0.bits)},
        {'name': 'CSKB1', 'bits': list(m.xmem.cskb1.bits)},
    ]


def mcu_update_window_all():
    mcu_update_window_currentAddr()
    mcu_update_window_memCells()
    mcu_update_window_keyRegs()
    mcu_update_window_flags()
    mcu_update_window_extDevsRegs()


window.disassemble_to_window_assRows = disassemble_to_window_assRows
window.mcu_load_hex_file = mcu_load_hex_file
window.mcu_next_cycle = mcu_next_cycle
window.mcu_reset_rom = mcu_reset_rom
window.mcu_reset_ram = mcu_reset_ram
window.mcu_update_window_memCells = mcu_update_window_memCells
window.mcu_update_window_all = mcu_update_window_all
