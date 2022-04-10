import * as React from 'react';
import Stack from '@mui/material/Stack';
import InfoAlert from './InfoAlert';

export default function InfoAlerts() {
    return (
        <Stack id={"info-alerts"} spacing={1}>
            <InfoAlert
                text={"Click on a row and then click on the >| icon to execute a program up to that row."}/>
            <InfoAlert
                text={"For the best user experience, use Chromium or a Chromium-based web browser such as Brave, Chrome, Edge, or Opera."}/>
        </Stack>
    );
}
