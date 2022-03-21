import * as React from 'react';
import {Box, IconButton} from '@material-ui/core';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';
import ArrowUpwardOutlinedIcon from '@mui/icons-material/ArrowUpwardOutlined';
import KeyboardReturnOutlinedIcon from '@mui/icons-material/KeyboardReturnOutlined';
import ArrowBackOutlinedIcon from '@mui/icons-material/ArrowBackOutlined';
import ArrowDownwardOutlinedIcon from '@mui/icons-material/ArrowDownwardOutlined';
import ArrowForwardOutlinedIcon from '@mui/icons-material/ArrowForwardOutlined';
import {makeStyles} from '@material-ui/core/styles';
import render from './main';

const useStyles = makeStyles({
    root: {
        marginLeft: '61px',
        '& .MuiIconButton-root': {
            height: '34px',
            padding: '5px',
        },
        '& .MuiSvgIcon-root': {
            fill: 'rgb(115, 115, 115)',
        },
    },
});

export default function SequentialKeyboard() {
    function onMouseDown(bitNumber) {
        if (Boolean(parseInt(window.csds[bitNumber]))) {
            mcu_set_seqKeyPressed();
            mcu_update_window_all();
            render();
        }
    }

    function onMouseUp(bitNumber) {
        if (Boolean(parseInt(window.csds[bitNumber]))) {
            mcu_clr_seqKeyPressed();
            mcu_update_window_all();
            render();
        }
    }

    return (
        <Box classes={useStyles()}>
            <Box>
                <IconButton>
                    <CloseOutlinedIcon onMouseDown={() => onMouseDown(6)} onMouseUp={() => onMouseUp(6)}/>
                </IconButton>
                <IconButton>
                    <ArrowUpwardOutlinedIcon onMouseDown={() => onMouseDown(4)} onMouseUp={() => onMouseUp(4)}/>
                </IconButton>
                <IconButton>
                    <KeyboardReturnOutlinedIcon onMouseDown={() => onMouseDown(7)} onMouseUp={() => onMouseUp(7)}/>
                </IconButton>
            </Box>
            <Box>
                <IconButton>
                    <ArrowBackOutlinedIcon onMouseDown={() => onMouseDown(2)} onMouseUp={() => onMouseUp(2)}/>
                </IconButton>
                <IconButton>
                    <ArrowDownwardOutlinedIcon onMouseDown={() => onMouseDown(3)} onMouseUp={() => onMouseUp(3)}/>
                </IconButton>
                <IconButton>
                    <ArrowForwardOutlinedIcon onMouseDown={() => onMouseDown(5)} onMouseUp={() => onMouseUp(5)}/>
                </IconButton>
            </Box>
        </Box>
    );
}
