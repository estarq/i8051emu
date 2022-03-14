from browser import window

import disassembler
import mcu

m = mcu.Microcontroller()


def disassemble(file_content):
    rows = []
    d = disassembler.disassemble(file_content)
    for addr, bytes_, opcode, args, mnemonic in d:
        arg1 = args[0] if args else '-'
        arg2 = args[1] if len(args) == 2 else '-'
        rows.append([addr, bytes_, opcode, arg1, arg2, mnemonic])
    return rows


def mcu_load_hex_file(file_content):
    m.load_hex_file(file_content)


def mcu_next_cycle():
    m.next_cycle()
    window.currentAddr = int(m.pc)
    mcu_update_window_memRows()
    mcu_update_window_keyRows()
    mcu_update_window_flags()


def mcu_reset_rom():
    m.reset_rom()


def mcu_reset_ram():
    m.reset_ram()


def mcu_update_window_rom():
    window.rom = [{'addr': addr, 'val': m.rom[addr]} for addr in range(1000)]


def mcu_update_window_ram():
    window.ram = [{'addr': addr, 'val': int(m.mem[addr])} for addr in range(256)]


def mcu_update_window_xram():
    window.xram = [{'addr': addr, 'val': int(m.xmem[addr])} for addr in range(1000)]


def mcu_update_window_memRows():
    if window.memType == 'ROM':
        mcu_update_window_rom()
        window.memRows = window.rom
    elif window.memType == 'RAM':
        mcu_update_window_ram()
        window.memRows = window.ram
    else:
        mcu_update_window_xram()
        window.memRows = window.xram


def mcu_update_window_keyRows():
    window.keyRows = [
        {'name': 'A', 'val': int(m.mem.a)},
        {'name': 'B', 'val': int(m.mem.b)},
        {'name': 'SP', 'val': int(m.mem.sp)},
        {'name': 'PC', 'val': int(m.pc)},
        {'name': 'DPTR', 'val': int(m.mem.dptr)},
        {'name': 'TH0', 'val': int(m.mem.th0)},
        {'name': 'TL0', 'val': int(m.mem.tl0)},
        {'name': 'TH1', 'val': int(m.mem.th1)},
        {'name': 'TL1', 'val': int(m.mem.tl1)},
        {'name': 'R0', 'val': int(m.mem.r0)},
        {'name': 'R1', 'val': int(m.mem.r1)},
        {'name': 'R2', 'val': int(m.mem.r2)},
        {'name': 'R3', 'val': int(m.mem.r3)},
        {'name': 'R4', 'val': int(m.mem.r4)},
        {'name': 'R5', 'val': int(m.mem.r5)},
        {'name': 'R6', 'val': int(m.mem.r6)},
        {'name': 'R7', 'val': int(m.mem.r7)}]


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
        'T0_M0': m.mem.t0_m0}


window.disassemble = disassemble
window.mcu_load_hex_file = mcu_load_hex_file
window.mcu_next_cycle = mcu_next_cycle
window.mcu_reset_rom = mcu_reset_rom
window.mcu_reset_ram = mcu_reset_ram
window.mcu_update_window_rom = mcu_update_window_rom
window.mcu_update_window_ram = mcu_update_window_ram
window.mcu_update_window_xram = mcu_update_window_xram
window.mcu_update_window_memRows = mcu_update_window_memRows
window.mcu_update_window_keyRows = mcu_update_window_keyRows
window.mcu_update_window_flags = mcu_update_window_flags
