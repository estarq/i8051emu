import * as React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Box} from '@material-ui/core';
import Digit from './Digit';

const useStyles = makeStyles({
    root: {
        display: 'inline-flex',
        justifyContent: 'space-between',
        width: '380px',
        marginLeft: '31px',
    },
});

export default function Display({csds}) {
    return (
        <Box classes={useStyles()}>
            {csds.reverse().map((bit, idx) => (
                <Digit key={idx} enabled={Boolean(parseInt(bit))} segments={window.segments}/>
            ))}
        </Box>
    );
}
