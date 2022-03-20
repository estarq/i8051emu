import * as React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Box} from '@material-ui/core';
import AssTable from './AssTable';
import MemTable from './MemTable';
import KeyRegsTable from './KeyRegsTable';
import FlagsTable from './FlagsTable';
import ExtDevsTable from './ExtDevsTable';
import PortsTable from './PortsTable';
import Display from './Display';

window.assRows = [];
window.currentAddr = 0;
window.memCells = [];
window.memType = 'ROM';
window.keyRegs = [];
window.flags = {};
window.extDevsRegs = [];
window.ports = [];
window.csds = [];
window.segments = {};

const useStyles = makeStyles({
    root: {
        display: 'inline-flex',
        flexDirection: 'column',
        '& > .MuiBox-root:first-of-type': {
            display: 'inline-flex',
            margin: '20px',
            '& .MuiBox-root': {
                flexDirection: 'column',
            },
        },
        '& > .MuiBox-root:last-of-type': {
            display: 'inline-flex',
            margin: '0px 20px',
        },
    },
});

export default function MainWindow() {
    return (
        <Box classes={useStyles()}>
            <Box>
                <AssTable rows={window.assRows} currentAddr={window.currentAddr}/>
                <MemTable cells={window.memCells} memType={window.memType}/>
                <KeyRegsTable regs={window.keyRegs}/>
                <Box>
                    <FlagsTable flags={window.flags}/>
                    <ExtDevsTable regs={window.extDevsRegs}/>
                    <PortsTable ports={window.ports}/>
                </Box>
            </Box>
            <Box>
                <Display csds={window.csds}/>
            </Box>
        </Box>
    );
}
