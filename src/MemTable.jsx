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
        marginLeft: '20px',
        border: '1px solid rgb(224, 224, 224)',
        borderRadius: '4px',
        scrollbarWidth: 'thin',
        overflowX: 'hidden',
        '& .MuiTableRow-head:last-of-type': {
            '& .MuiTableCell-head': {
                top: '28px',
            },
        },
        '& .MuiTableRow-root:last-of-type': {
            '& .MuiTableCell-body': {
                borderBottomWidth: '0px',
            },
        },
        '& .MuiTableCell-head:first-of-type': {
            padding: '4px 16px',
        },
        '& .MuiTableCell-root': {
            textAlign: 'center',
            lineHeight: '15px',
        },
        '& .MuiInputBase-input': {
            padding: '0px 15px 0px 0px',
            fontSize: '15px',
        },
        '& .MuiSelect-select:focus': {
            backgroundColor: 'inherit',
        },
        '& .MuiSelect-icon': {
            right: '15px',
        },
    },
});

export default function MemTable({cells, memType}) {
    function onMemoryTypeChanged(e) {
        window.memType = e.target.value;
        document.getElementById('memTable').scrollTop = 0;
        mcu_update_window_memCells();
        render();
    }

    return (
        <TableContainer id="memTable" classes={useStyles()}>
            <Table stickyHeader size="small">
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={2}>
                            <FormControl fullWidth>
                                <Select value={memType} onChange={onMemoryTypeChanged} disableUnderline>
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
                    {cells.map((cell) => (
                        <TableRow key={cell.addr}>
                            <TableCell>{cell.addr}</TableCell>
                            <TableCell>{cell.value}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
