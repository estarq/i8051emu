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
    if window.memType == 'ROM':
        mcu_update_window_rom()
        window.memRows = window.rom
    elif window.memType == 'RAM':
        mcu_update_window_ram()
        window.memRows = window.ram
    elif window.memType == 'XRAM':
        mcu_update_window_xram()
        window.memRows = window.xram


def mcu_update_window_rom():
    window.rom = [{'addr': addr, 'val': m.rom[addr]} for addr in range(1000)]


def mcu_update_window_ram():
    window.ram = [{'addr': addr, 'val': int(m.mem[addr])} for addr in range(256)]


def mcu_update_window_xram():
    window.xram = [{'addr': addr, 'val': int(m.xmem[addr])} for addr in range(1000)]


def mcu_reset_rom():
    m.reset_rom()


window.disassemble = disassemble
window.mcu_load_hex_file = mcu_load_hex_file
window.mcu_next_cycle = mcu_next_cycle
window.mcu_update_window_rom = mcu_update_window_rom
window.mcu_update_window_ram = mcu_update_window_ram
window.mcu_update_window_xram = mcu_update_window_xram
window.mcu_reset_rom = mcu_reset_rom
