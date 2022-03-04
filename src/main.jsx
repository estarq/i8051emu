import * as React from 'react';
import ReactDOM from 'react-dom';
import {StyledEngineProvider} from '@mui/material/styles';
import TopBar from './TopBar';
import AssTable from './AssTable';

window.assRows = [];
window.currentAddr = 0;

function App() {
    return (
        <StyledEngineProvider injectFirst>
            <TopBar/>
            <AssTable rows={window.assRows} currentAddr={window.currentAddr}/>
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
