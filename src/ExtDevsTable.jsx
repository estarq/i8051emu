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
        width: '454px',
        height: '139px',
        overflow: 'hidden',
        marginLeft: '20px',
        border: '1px solid rgb(224, 224, 224)',
        borderRadius: '4px',
        '& .MuiTableCell-head': {
            position: 'relative',
            left: '7px',
        },
        '& .MuiTableCell-root': {
            textAlign: 'center',
            padding: '6px 10px',
            lineHeight: '15px',
        },
        '& .MuiTableCell-body:first-of-type': {
            width: '65px',
            padding: '6px 0px',
        },
        '& .MuiTableRow-root:last-of-type': {
            '& .MuiTableCell-body': {
                borderBottomWidth: '0px',
            },
        },
    },
});

export default function ExtDevsTable({regs}) {
    return (
        <TableContainer classes={useStyles()}>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={9}>External Devices</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {regs.map((reg) => (
                        <TableRow key={reg.name}>
                            <TableCell>{reg.name}</TableCell>
                            {reg.bits.map((bit, idx) => (
                                <TableCell key={idx}>{bit}</TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
