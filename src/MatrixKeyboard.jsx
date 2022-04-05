import * as React from 'react';
import {Box, IconButton} from '@material-ui/core';
import ArrowUpwardOutlinedIcon from '@mui/icons-material/ArrowUpwardOutlined';
import ArrowDownwardOutlinedIcon from '@mui/icons-material/ArrowDownwardOutlined';
import ArrowBackOutlinedIcon from '@mui/icons-material/ArrowBackOutlined';
import ArrowForwardOutlinedIcon from '@mui/icons-material/ArrowForwardOutlined';
import CloseOutlinedIcon from '@mui/icons-material/CloseOutlined';
import KeyboardReturnOutlinedIcon from '@mui/icons-material/KeyboardReturnOutlined';
import LooksOneOutlinedIcon from '@mui/icons-material/LooksOneOutlined';
import LooksTwoOutlinedIcon from '@mui/icons-material/LooksTwoOutlined';
import Looks3OutlinedIcon from '@mui/icons-material/Looks3Outlined';
import Looks4OutlinedIcon from '@mui/icons-material/Looks4Outlined';
import Looks5OutlinedIcon from '@mui/icons-material/Looks5Outlined';
import Looks6OutlinedIcon from '@mui/icons-material/Looks6Outlined';
import {makeStyles} from '@material-ui/core/styles';
import render from './main';

const useStyles = makeStyles({
    root: {
        marginLeft: '141px',
        position: 'relative',
        top: '-36px',
        '& .MuiIconButton-root': {
            height: '34px',
            padding: '5px',
        },
        '& .MuiSvgIcon-root': {
            fill: 'rgb(115, 115, 115)',
        },
        '& .MuiBox-root:first-of-type': {
            '& .MuiIconButton-root:first-of-type': {
                margin: '0 68px 0 34px',
            },
        },
        '& .MuiBox-root:nth-of-type(2)': {
            '& .MuiIconButton-root:nth-of-type(2)': {
                margin: '0 34px',
            },
        },
        '& .MuiBox-root:last-of-type': {
            '& .MuiIconButton-root:first-of-type': {
                margin: '0 68px 0 34px',
            },
        },
    },
});

export default function MatrixKeyboard() {
    function onMouseDown(register, bitNumber) {
        if (register === 'CSKB0')
            mcu_set_CSKB0_bit(bitNumber);
        else
            mcu_set_CSKB1_bit(bitNumber);
        mcu_update_window_all();
        render();
    }

    function onMouseUp(register, bitNumber) {
        if (register === 'CSKB0')
            mcu_clr_CSKB0_bit(bitNumber);
        else
            mcu_clr_CSKB1_bit(bitNumber);
        mcu_update_window_all();
        render();
    }

    return (
        <Box classes={useStyles()}>
            <Box>
                <IconButton>
                    <ArrowUpwardOutlinedIcon onMouseDown={() => onMouseDown('CSKB1', 3)}
                                             onMouseUp={() => onMouseUp('CSKB1', 3)}/>
                </IconButton>
                <IconButton onMouseDown={() => onMouseDown('CSKB0', 0)}
                            onMouseUp={() => onMouseUp('CSKB0', 0)}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgb(115, 115, 115)"
                         strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M10 8h4l-2 8"/>
                        <rect x="4" y="4" width="16" height="16" rx="2"/>
                    </svg>
                </IconButton>
                <IconButton onMouseDown={() => onMouseDown('CSKB1', 7)}
                            onMouseUp={() => onMouseUp('CSKB1', 7)}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgb(115, 115, 115)"
                         strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <circle cx="12" cy="10" r="2"/>
                        <circle cx="12" cy="14" r="2"/>
                        <rect x="4" y="4" width="16" height="16" rx="2"/>
                    </svg>
                </IconButton>
                <IconButton onMouseDown={() => onMouseDown('CSKB1', 6)}
                            onMouseUp={() => onMouseUp('CSKB1', 6)}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgb(115, 115, 115)"
                         strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <circle cx="12" cy="10" r="2"/>
                        <path d="M10 14a2 2 0 1 0 4 0v-4"/>
                        <rect x="4" y="4" width="16" height="16" rx="2"/>
                    </svg>
                </IconButton>
                <IconButton onMouseDown={() => onMouseDown('CSKB0', 7)}
                            onMouseUp={() => onMouseUp('CSKB0', 7)}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgb(115, 115, 115)"
                         strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                        <path d="M12 8a2 2 0 0 1 2 2v4a2 2 0 1 1 -4 0v-4a2 2 0 0 1 2 -2z"/>
                        <rect x="4" y="4" width="16" height="16" rx="2"/>
                    </svg>
                </IconButton>
            </Box>
            <Box>
                <IconButton>
                    <ArrowBackOutlinedIcon onMouseDown={() => onMouseDown('CSKB1', 5)}
                                           onMouseUp={() => onMouseUp('CSKB1', 5)}/>
                </IconButton>
                <IconButton>
                    <ArrowForwardOutlinedIcon onMouseDown={() => onMouseDown('CSKB1', 4)}
                                              onMouseUp={() => onMouseUp('CSKB1', 4)}/>
                </IconButton>
                <IconButton>
                    <Looks4OutlinedIcon onMouseDown={() => onMouseDown('CSKB0', 3)}
                                        onMouseUp={() => onMouseUp('CSKB0', 3)}/>
                </IconButton>
                <IconButton>
                    <Looks5OutlinedIcon onMouseDown={() => onMouseDown('CSKB0', 2)}
                                        onMouseUp={() => onMouseUp('CSKB0', 2)}/>
                </IconButton>
                <IconButton>
                    <Looks6OutlinedIcon onMouseDown={() => onMouseDown('CSKB0', 1)}
                                        onMouseUp={() => onMouseUp('CSKB0', 1)}/>
                </IconButton>
                <IconButton>
                    <CloseOutlinedIcon onMouseDown={() => onMouseDown('CSKB1', 1)}
                                       onMouseUp={() => onMouseUp('CSKB1', 1)}/>
                </IconButton>
            </Box>
            <Box>
                <IconButton>
                    <ArrowDownwardOutlinedIcon onMouseDown={() => onMouseDown('CSKB1', 2)}
                                               onMouseUp={() => onMouseUp('CSKB1', 2)}/>
                </IconButton>
                <IconButton>
                    <LooksOneOutlinedIcon onMouseDown={() => onMouseDown('CSKB0', 6)}
                                          onMouseUp={() => onMouseUp('CSKB0', 6)}/>
                </IconButton>
                <IconButton>
                    <LooksTwoOutlinedIcon onMouseDown={() => onMouseDown('CSKB0', 5)}
                                          onMouseUp={() => onMouseUp('CSKB0', 5)}/>
                </IconButton>
                <IconButton>
                    <Looks3OutlinedIcon onMouseDown={() => onMouseDown('CSKB0', 4)}
                                        onMouseUp={() => onMouseUp('CSKB0', 4)}/>
                </IconButton>
                <IconButton>
                    <KeyboardReturnOutlinedIcon onMouseDown={() => onMouseDown('CSKB1', 0)}
                                                onMouseUp={() => onMouseUp('CSKB1', 0)}/>
                </IconButton>
            </Box>
        </Box>
    );
}
