import * as React from 'react';
import {useState} from 'react';
import {AppBar, IconButton, Toolbar, Typography} from '@material-ui/core';
import FileUploadOutlinedIcon from '@mui/icons-material/FileUploadOutlined';
import RefreshOutlinedIcon from '@mui/icons-material/RefreshOutlined';
import KeyboardArrowRightOutlinedIcon from '@mui/icons-material/KeyboardArrowRightOutlined';
import LastPageOutlinedIcon from '@mui/icons-material/LastPageOutlined';
import KeyboardDoubleArrowRightOutlinedIcon from '@mui/icons-material/KeyboardDoubleArrowRightOutlined';
import PauseOutlinedIcon from '@mui/icons-material/PauseOutlined';
import {makeStyles} from '@material-ui/core/styles';
import render from './main';

const useStyles = makeStyles({
    root: {
        backgroundColor: 'rgba(25, 118, 210, 0.7)',
        boxShadow: '0px 2px 0px -1px rgba(0, 0, 0, 0.2),'
            + '0px 2px 5px 0px rgba(0, 0, 0, 0.14),'
            + '0px 1px 10px 0px rgba(0, 0, 0, 0.12)',
        '& .MuiToolbar-regular': {
            minHeight: '60px',
        },
        '& .MuiTypography-root': {
            margin: '0px 10px 0px 5px',
        },
    },
});

export default function TopBar() {
    const [running, setRunning] = useState(false);
    const [intervalRef, setIntervalRef] = useState();

    function onFileUploaded(e) {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => {
            mcu_reset_rom();
            mcu_load_hex_file(reader.result);
            disassemble_to_window_assRows(reader.result);
            window.memType = 'ROM';
            document.getElementById('memTable').scrollTop = 0;
            mcu_update_window_all();
            render();
        }
    }

    function onRefreshClicked() {
        mcu_reset_ram();
        window.memType = 'ROM';
        document.getElementById('memTable').scrollTop = 0;
        mcu_update_window_all();
        render();
    }

    function onNextClicked() {
        if (window.assRows.length) {
            mcu_next_cycle();
            mcu_update_window_all();
            render();
        }
    }

    function onToSelectedClicked() {
        const intervalRef = setInterval(() => {
            if (window.currentAddr !== window.selectedAddr)
                onNextClicked();
            else
                clearInterval(intervalRef);
        }, 500);
    }

    function onRunClicked() {
        setIntervalRef(setInterval(onNextClicked, 500));
        setRunning(true);
    }

    function onPauseClicked() {
        clearInterval(intervalRef);
        setRunning(false);
    }

    return (
        <AppBar position="static" classes={useStyles()}>
            <Toolbar>
                <Typography variant="h6" color="inherit" component="div">
                    i8051emu
                </Typography>

                <IconButton variant="text" color="inherit" component="label">
                    <FileUploadOutlinedIcon/>
                    <input type="file" hidden onChange={onFileUploaded}/>
                </IconButton>

                <IconButton color="inherit" onClick={onRefreshClicked}>
                    <RefreshOutlinedIcon/>
                </IconButton>

                <IconButton color="inherit" onClick={onNextClicked}>
                    <KeyboardArrowRightOutlinedIcon/>
                </IconButton>
                <IconButton color="inherit" onClick={onToSelectedClicked}>
                    <LastPageOutlinedIcon/>
                </IconButton>
                <IconButton color="inherit" onClick={running ? onPauseClicked : onRunClicked}>
                    {running ? <PauseOutlinedIcon/> : <KeyboardDoubleArrowRightOutlinedIcon/>}
                </IconButton>
            </Toolbar>
        </AppBar>
    );
}
