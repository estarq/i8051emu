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
import StateIcons from './StateIcons';
import SequentialKeyboard from './SequentialKeyboard';
import MatrixKeyboard from './MatrixKeyboard';

window.assRows = [];
window.currentAddr = 0;
window.selectedAddr = 0;
window.memCells = [];
window.memType = 'ROM';
window.keyRegs = [];
window.flags = {};
window.ports = [];
window.extDevsRegs = [];
window.csds = [];
window.segments = {};
window.displayEnabled = false;
window.buzzerEnabled = false;
window.LEDEnabled = false;

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
                    <PortsTable ports={window.ports}/>
                    <ExtDevsTable regs={window.extDevsRegs}/>
                </Box>
            </Box>
            <Box>
                <Display enabled={window.displayEnabled} csds={window.csds}/>
                <StateIcons displayEnabled={window.displayEnabled} buzzerEnabled={window.buzzerEnabled}
                            LEDEnabled={window.LEDEnabled}/>
                <SequentialKeyboard/>
                <MatrixKeyboard/>
            </Box>
        </Box>
    );
}
