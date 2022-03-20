import * as React from 'react';
import {Box} from '@material-ui/core';
import Filter7OutlinedIcon from '@mui/icons-material/Filter7Outlined';
import NotificationsActiveOutlinedIcon from '@mui/icons-material/NotificationsActiveOutlined';
import WbIncandescentOutlinedIcon from '@mui/icons-material/WbIncandescentOutlined';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles({
    root: {
        display: 'inline-flex',
        justifyContent: 'space-between',
        width: '100px',
        margin: '20px 0px 0px 71px',
        '& .enabled': {
            color: 'rgb(87, 87, 87)',
        },
        '& .disabled': {
            color: 'rgb(215, 215, 215)',
        },
    },
});

export default function StateIcons({displayEnabled, buzzerEnabled, LEDEnabled}) {
    return (
        <Box classes={useStyles()}>
            <Filter7OutlinedIcon className={displayEnabled ? 'enabled' : 'disabled'}/>
            <NotificationsActiveOutlinedIcon className={buzzerEnabled ? 'enabled' : 'disabled'}/>
            <WbIncandescentOutlinedIcon className={LEDEnabled ? 'enabled' : 'disabled'}/>
        </Box>
    );
}
