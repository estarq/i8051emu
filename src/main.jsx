import * as React from 'react';
import ReactDOM from 'react-dom';
import {StyledEngineProvider} from '@mui/material/styles';
import {makeStyles} from '@material-ui/core/styles';
import {Box} from '@material-ui/core';
import TopBar from './TopBar';
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

const mainStyles = makeStyles({
    root: {
        display: 'inline-flex',
        margin: '20px',
        '& .MuiBox-root': {
            flexDirection: 'column',
        },
    },
});

const devsStyles = makeStyles({
    root: {
        display: 'inline-flex',
        margin: '0px 20px',
    },
});

function App() {
    return (
        <StyledEngineProvider injectFirst>
            <TopBar/>
            <Box classes={mainStyles()}>
                <AssTable rows={window.assRows} currentAddr={window.currentAddr}/>
                <MemTable cells={window.memCells} memType={window.memType}/>
                <KeyRegsTable regs={window.keyRegs}/>
                <Box>
                    <FlagsTable flags={window.flags}/>
                    <ExtDevsTable regs={window.extDevsRegs}/>
                    <PortsTable ports={window.ports}/>
                </Box>
            </Box>
            <Box classes={devsStyles()}>
                <Display csds={window.csds}/>
            </Box>
        </StyledEngineProvider>
    );
}

export default function render() {
    ReactDOM.render(
        <App/>,
        document.getElementById('root')
    );
}

render();
