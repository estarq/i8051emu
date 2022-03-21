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


def mcu_set_seqKeyPressed():
    m.mem.p3[2] = 1


def mcu_clr_seqKeyPressed():
    m.mem.p3[2] = 0


def mcu_update_window_currentAddr():
    window.currentAddr = int(m.pc)


def mcu_update_window_memCells():
    if window.memType == 'ROM':
        window.memCells = [
            {'addr': addr, 'value': m.rom[addr]} for addr in range(1000)
        ]
    elif window.memType == 'RAM':
        window.memCells = [
            {'addr': addr, 'value': int(m.mem[addr])} for addr in range(128)
        ]
    elif window.memType == 'SFR':
        window.memCells = [
            {'addr': addr, 'value': int(m.mem[addr])} for addr in range(128, 256)
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
        'ea': m.mem.ea,
        'es': m.mem.es,
        'et1': m.mem.et1,
        'ex1': m.mem.ex1,
        'et0': m.mem.et0,
        'ex0': m.mem.ex0,
        'ps': m.mem.ps,
        'pt1': m.mem.pt1,
        'px1': m.mem.px1,
        'pt0': m.mem.pt0,
        'px0': m.mem.px0,
        'c': m.mem.c,
        'ac': m.mem.ac,
        'f0': m.mem.f0,
        'rs1': m.mem.rs1,
        'rs0': m.mem.rs0,
        'ov': m.mem.ov,
        'f1': m.mem.f1,
        'p': m.mem.p,
        'tf1': m.mem.tf1,
        'tr1': m.mem.tr1,
        'tf0': m.mem.tf0,
        'tr0': m.mem.tr0,
        'ie1': m.mem.ie1,
        'it1': m.mem.it1,
        'ie0': m.mem.ie0,
        'it0': m.mem.it0,
        't1_gate': m.mem.t1_gate,
        't1_ct': m.mem.t1_ct,
        't1_m1': m.mem.t1_m1,
        't1_m0': m.mem.t1_m0,
        't0_gate': m.mem.t0_gate,
        't0_ct': m.mem.t0_ct,
        't0_m1': m.mem.t0_m1,
        't0_m0': m.mem.t0_m0,
    }


def mcu_update_window_extDevsRegs():
    window.extDevsRegs = [
        {'name': 'CSDS', 'bits': list(m.xmem.csds.bits)},
        {'name': 'CSDB', 'bits': list(m.xmem.csdb.bits)},
        {'name': 'CSKB0', 'bits': list(m.xmem.cskb0.bits)},
        {'name': 'CSKB1', 'bits': list(m.xmem.cskb1.bits)},
    ]


def mcu_update_window_ports():
    window.ports = [
        {'name': 'P0', 'bits': list(m.mem.p0.bits)},
        {'name': 'P1', 'bits': list(m.mem.p1.bits)},
        {'name': 'P2', 'bits': list(m.mem.p2.bits)},
        {'name': 'P3', 'bits': list(m.mem.p3.bits)},
    ]


def mcu_update_window_csds():
    window.csds = list(m.xmem.csds.bits)


def mcu_update_window_segments():
    window.segments = {
        name: bool(m.xmem.csdb[idx])
        for idx, name in enumerate(['dp', 'g', 'f', 'e', 'd', 'c', 'b', 'a'])
    }


def mcu_update_window_displayEnabled():
    window.displayEnabled = not m.mem.p1[1]


def mcu_update_window_buzzerEnabled():
    window.buzzerEnabled = not m.mem.p1[2]


def mcu_update_window_LEDEnabled():
    window.LEDEnabled = not m.mem.p1[0]


def mcu_update_window_all():
    mcu_update_window_currentAddr()
    mcu_update_window_memCells()
    mcu_update_window_keyRegs()
    mcu_update_window_flags()
    mcu_update_window_extDevsRegs()
    mcu_update_window_ports()
    mcu_update_window_csds()
    mcu_update_window_segments()
    mcu_update_window_displayEnabled()
    mcu_update_window_buzzerEnabled()
    mcu_update_window_LEDEnabled()


window.disassemble_to_window_assRows = disassemble_to_window_assRows
window.mcu_load_hex_file = mcu_load_hex_file
window.mcu_next_cycle = mcu_next_cycle
window.mcu_reset_rom = mcu_reset_rom
window.mcu_reset_ram = mcu_reset_ram
window.mcu_set_seqKeyPressed = mcu_set_seqKeyPressed
window.mcu_clr_seqKeyPressed = mcu_clr_seqKeyPressed
window.mcu_update_window_memCells = mcu_update_window_memCells
window.mcu_update_window_all = mcu_update_window_all
