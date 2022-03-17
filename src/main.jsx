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

window.assRows = [];
window.currentAddr = 0;
window.memCells = [];
window.memType = 'ROM';
window.keyRegs = [];
window.flags = {};

const useStyles = makeStyles({
    root: {
        display: 'inline-flex',
        margin: '20px',
    },
});

function App() {
    return (
        <StyledEngineProvider injectFirst>
            <TopBar/>
            <Box classes={useStyles()}>
                <AssTable rows={window.assRows} currentAddr={window.currentAddr}/>
                <MemTable cells={window.memCells} memType={window.memType}/>
                <KeyRegsTable regs={window.keyRegs}/>
                <FlagsTable flags={window.flags}/>
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
