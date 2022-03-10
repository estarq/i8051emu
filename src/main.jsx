import * as React from 'react';
import ReactDOM from 'react-dom';
import {StyledEngineProvider} from '@mui/material/styles';
import {Box} from "@material-ui/core";
import TopBar from './TopBar';
import AssTable from './AssTable';
import MemTable from "./MemTable";

window.assRows = [];
window.currentAddr = 0;
window.memRows = [];
window.memType = 'ROM';

function App() {
    return (
        <StyledEngineProvider injectFirst>
            <TopBar/>
            <Box>
                <AssTable rows={window.assRows} currentAddr={window.currentAddr}/>
                <MemTable rows={window.memRows} memType={window.memType}/>
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
