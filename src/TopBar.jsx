import * as React from 'react';
import {AppBar, IconButton, Toolbar, Typography} from "@material-ui/core";
import FileUploadOutlinedIcon from '@mui/icons-material/FileUploadOutlined';
import KeyboardArrowRightOutlinedIcon from '@mui/icons-material/KeyboardArrowRightOutlined';
import KeyboardDoubleArrowRightOutlinedIcon from '@mui/icons-material/KeyboardDoubleArrowRightOutlined';
import {makeStyles} from "@material-ui/core/styles";
import render from "./main";

const useStyles = makeStyles({
    root: {
        'background-color': 'rgba(25, 118, 210, 0.7)',
    },
});

function onFileUpload(e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = () => {
        mcu_reset_rom();
        window.currentAddr = 0;
        window.assRows = [];
        const disassembled = disassemble(reader.result);
        disassembled.forEach(function (elem, idx, arr) {
            assRows.push({
                addr: arr[idx][0],
                bytes: arr[idx][1],
                opcode: arr[idx][2],
                arg1: arr[idx][3],
                arg2: arr[idx][4],
                mnemonic: arr[idx][5],
            })
        })
        mcu_load_hex_file(reader.result);
        render();
    }
}

export default function TopBar() {
    return (
        <AppBar position="static" classes={useStyles()}>
            <Toolbar>
                <Typography variant="h6" color="inherit" component="div">
                    i8051emu
                </Typography>

                <IconButton variant="text" color="inherit" component="label">
                    <FileUploadOutlinedIcon/>
                    <input type="file" hidden onChange={onFileUpload}/>
                </IconButton>

                <IconButton color="inherit" onClick={() => {
                    if (window.assRows.length) {
                        mcu_next_cycle();
                        render();
                    }
                }}>
                    <KeyboardArrowRightOutlinedIcon/>
                </IconButton>
                <IconButton color="inherit" onClick={() => {
                    if (window.assRows.length) {
                        setInterval(() => {
                            mcu_next_cycle();
                            render();
                        }, 500);
                    }
                }}>
                    <KeyboardDoubleArrowRightOutlinedIcon/>
                </IconButton>
            </Toolbar>
        </AppBar>
    );
}
