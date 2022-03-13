import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import {makeStyles} from '@material-ui/core/styles';
import {FormControl, MenuItem, Select} from '@material-ui/core';
import render from './main';

const useStyles = makeStyles({
    root: {
        width: '139px',
        height: '531px',
        'margin-left': '20px',
        border: '1px solid rgb(224, 224, 224)',
        'border-radius': '4px',
        'scrollbar-width': 'thin',
        '& .MuiTableRow-head:last-of-type .MuiTableCell-head': {
            top: '28px',
        },
        '& .MuiTableRow-root:last-of-type .MuiTableCell-body': {
            'border-bottom-width': 0,
        },
        '& .MuiTableCell-head:first-of-type': {
            padding: '4px 16px',
        },
        '& .MuiTableCell-root': {
            'text-align': 'center',
            'line-height': '15px',
        },
        '& .MuiInputBase-input': {
            padding: '0 15px 0 0',
            'font-size': '15px',
        },
        '& .MuiSelect-select:focus': {
            'background-color': 'inherit',
        },
        '& .MuiSelect-icon': {
            right: '15px',
        },
    },
});

function handleChange(e) {
    window.memType = e.target.value;
    mcu_update_window_memRows();
    render();
}

export default function MemTable(props) {
    return (
        <TableContainer id="memTable" classes={useStyles()}>
            <Table stickyHeader size="small">
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={2}>
                            <FormControl fullWidth>
                                <Select value={props.memType} onChange={handleChange} disableUnderline>
                                    <MenuItem value={"ROM"}>ROM</MenuItem>
                                    <MenuItem value={"RAM"}>RAM</MenuItem>
                                    <MenuItem value={"XRAM"}>XRAM</MenuItem>
                                </Select>
                            </FormControl>
                        </TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Addr</TableCell>
                        <TableCell>Value</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {props.rows.map((row) => (
                        <TableRow key={row.addr}>
                            <TableCell>{row.addr}</TableCell>
                            <TableCell>{row.val}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
