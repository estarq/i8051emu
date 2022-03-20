import * as React from 'react';
import ReactDOM from 'react-dom';
import {StyledEngineProvider} from '@mui/material/styles';
import TopBar from './TopBar';
import MainWindow from './MainWindow';

function App() {
    return (
        <StyledEngineProvider injectFirst>
            <TopBar/>
            <MainWindow/>
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
