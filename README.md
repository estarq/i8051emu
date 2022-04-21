## i8051emu

![i8051emu](https://github.com/estarq/i8051emu/blob/master/.github/i8051emu.png)

A free and open-source Intel 8051 emulator built with Python (Brython) and React (with MUI) as a final thesis (BE).

## Building

Clone the repo ([Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)):<br>
`git clone https://github.com/estarq/i8051emu`

Change directory:<br>
`cd i8051emu`

### Docker ([Installing Docker](https://docs.docker.com/get-docker/))

Use Compose ([Installing Compose](https://docs.docker.com/compose/install/)):<br>
`docker compose up -d`

or

Build an image:<br>
`docker build -t i8051emu .`

Run as a container:<br>
`docker run -d -p 3000:3000 --name i8051emu i8051emu`

### Web

Install dependencies ([Installing Node.js](https://nodejs.dev/learn/how-to-install-nodejs)):<br>
`npm install --legacy-peer-deps`

Compile JSX, bundle up dependencies, optimize the output:<br>
`npm run build`

### Electron

Follow the steps for `Web`, then:

Change directory:<br>
`cd electron`

Install dependencies:<br>
`npm install`

Build for Mac (arm64, x64):<br>
`npm run distMac`

Build for Linux (AppImage):<br>
`npm run distLinux`

Build for Window:<br>
`npm run distWindows`

Executable files are saved to `electron/dist/`.

Webserver is required because of restrictions of the "file" protocol (Brython makes Ajax calls), thus Electron app utilizes [Express](https://expressjs.com/) to serve static content and the firewall may prompt to accept incoming network connections.

## Tests

Most of the python code is covered with unit tests (pytest).<br>
Please note that because of Brython, not everything that passes the tests is guaranteed to work, so it's necessary to test everything in a browser.

## Download

### Mac, Linux, Windows

Download [the latest release](https://github.com/estarq/i8051emu/releases).

### Docker ([Installing Docker](https://docs.docker.com/get-docker/))

Pull from Docker Hub:<br>
`docker pull estarq/i8051emu`
<br>Superuser privileges may be required.

## Installation

### Mac

Doubleclick on `.dmg` file and move `i8051emu.app` to `Applications`.

### Linux

Doubleclick on `.AppImage` file.<br>Make it executable if necessary:<br>
`chmod +x i8051emu-1.0.0.AppImage`

### Windows

Doubleclick on `.exe` file.

### Docker ([Installing Docker](https://docs.docker.com/get-docker/))

Download an image and run it as a container:<br>
`docker run -d -p 3000:3000 --name i8051emu estarq/i8051emu`
<br>Superuser privileges may be required.

## How to use

### App Bar Icons

1st - Loading an Intel HEX file from the disk<br>
2nd - Resetting the state of the microcontroller leaving the content of the ROM<br>
3rd - Execution of the next instruction<br>
4th - Execution of the program up to the clicked row<br>
5th - Automatic execution of the next instruction every 500 ms. When clicked, the icon turns into a pause button.

### Main Table

Each line represents one assembly instruction. The row highlighted in blue is next in the sequence of program execution.

Description of the columns:<br>
Addr - the ROM address where the instruction is stored<br>
Bytes - number of bytes (1-4) that the instruction occupies in the ROM memory<br>
Opcode - instruction machine code (0-255)<br>
Arg1, Arg2 - subsequent arguments of the instruction (0-255 each)<br>
Mnemonic - disassembled form of the instruction

All numbers except those ending with h (hexadecimal numbers) are decimal.

### Memory Table

Contains consecutive cells of the selected memory (RAM by default). The memory type can be changed by selecting the desired memory type from the drop-down list. Rendering is virtualized using react-virtualized and mui-virtualized-table, which causes errors in browsers not based on Chromium.

All numbers are decimal.

### Key Registers Table

Contains the most important registers of the microcontroller along with their values.

All numbers are decimal.

### Flags Table

Contains flags of IE, IP, PSW, TCON, and TMOD registers. The flag name in bold indicates that it is set.

### Ports Table

Contains consecutive bits (binary representations) of the P0-P3 ports.

### External Devices Table

Contains consecutive bits (binary representations) of the CSDS, CSDB, CSKB0, and CSKB1 registers.

### State Icons

1st - Seven-segment display<br>
2nd - Buzzer<br>
3rd - LED

The device icon in bold indicates that the device is on.

### Seven-segment Display

The digits (with dots) represent the state of the CSDS register. The segments represent the state of the CSDB register.

### Sequential Keyboard

This keyboard is associated with a seven-segment display and uses the CSDS register to determine whether to respond to a given key.

In continuous operation mode (next instruction every 500ms), hold the button for a while so that the microcontroller has enough time to notice the change.

### Matrix Keyboard

This keyboard is not associated with a seven-segment display. Clicking on the button changes the relevant bit in the CSKB0 or CSKB1 register.

In continuous operation mode (next instruction every 500ms), hold the button for a while so that the microcontroller has enough time to notice the change.

## License

Licensed under [the MIT license](https://github.com/estarq/i8051emu/blob/master/LICENSE).
