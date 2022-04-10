import * as React from 'react';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';

export default function InfoAlert({text}) {
    const [open, setOpen] = React.useState(true);

    return (
        <Box>
            <Collapse in={open}>
                <Alert severity="info" action={
                    <IconButton color="inherit" size="small" onClick={() => {
                        setOpen(false);
                    }}>
                        <CloseIcon fontSize="inherit"/>
                    </IconButton>
                }>
                    {text}
                </Alert>
            </Collapse>
        </Box>
    );
}
