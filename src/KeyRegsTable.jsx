import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles({
    root: {
        width: '155px',
        height: '543px',
        'overflow-y': 'hidden',
        'margin-left': '20px',
        border: '1px solid rgb(224, 224, 224)',
        'border-radius': '4px',
        '& .MuiTableCell-head': {
            height: '26px',
        },
        '& .MuiTableRow-head:last-of-type th': {
            padding: '4px 16px',
            height: '27px',
        },
        '& .MuiTableBody-root td': {
            'line-height': '23px',
        },
        '& .MuiTableRow-root:last-of-type td': {
            'border-bottom': 0,
        },
        '& .MuiTableCell-root': {
            'text-align': 'center',
        },
    },
});

export default function KeyRegsTable(props) {
    return (
        <TableContainer classes={useStyles()}>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={2}>Key Registers</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Value</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.rows.map((row) => (
                        <TableRow key={row.name}>
                            <TableCell>{row.name}</TableCell>
                            <TableCell>{row.val}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
