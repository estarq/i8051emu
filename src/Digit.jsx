import * as React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Box} from '@material-ui/core';

const useStyles = makeStyles({
    root: {
        width: '40px',
    },
});

const onColor = 'rgb(87, 87, 87)';
const offColor = 'rgb(215, 215, 215)';

export default function Digit({enabled, segments}) {
    return (
        <Box classes={useStyles()}>
            <svg viewBox="0 0 100 160">
                <path d="m 70,0 8,8 -8,8 H 18 L 10,8 18,0 Z"
                      fill={enabled && segments.a ? onColor : offColor}/>
                <path d="m 72,18 8,-8 8,8 v 52 l -8,8 -8,-8 z"
                      fill={enabled && segments.b ? onColor : offColor}/>
                <path d="m 72,90 8,-8 8,8 v 52 l -8,8 -8,-8 z"
                      fill={enabled && segments.c ? onColor : offColor}/>
                <path d="m 70,144 8,8 -8,8 H 18 L 10,152 18,144 Z"
                      fill={enabled && segments.d ? onColor : offColor}/>
                <path d="m 0,90 8,-8 8,8 v 52 l -8,8 -8,-8 z"
                      fill={enabled && segments.e ? onColor : offColor}/>
                <path d="m 0,18 8,-8 8,8 V 70 L 8,78 0,70 Z"
                      fill={enabled && segments.f ? onColor : offColor}/>
                <path d="m 70,72 8,8 -8,8 H 18 L 10,80 18,72 Z"
                      fill={enabled && segments.g ? onColor : offColor}/>
                <circle cx="94" cy="152" r="6"
                        fill={enabled && segments.dp ? onColor : offColor}/>
            </svg>
        </Box>
    );
}
