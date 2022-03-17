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
        width: '139px',
        height: '531px',
        overflowY: 'hidden',
        marginLeft: '20px',
        border: '1px solid rgb(224, 224, 224)',
        borderRadius: '4px',
        '& .MuiTableRow-root:last-of-type .MuiTableCell-body': {
            borderBottomWidth: '0px',
        },
        '& .MuiTableCell-root': {
            textAlign: 'center',
            lineHeight: '15px',
        },
    },
});

export default function KeyRegsTable({regs}) {
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
                    {regs.map((reg) => (
                        <TableRow key={reg.name}>
                            <TableCell>{reg.name}</TableCell>
                            <TableCell>{reg.value}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
