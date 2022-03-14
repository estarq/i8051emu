import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import {Box} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles({
    root: {
        width: '454px',
        height: '168px',
        overflow: 'hidden',
        margin: '0 0 26px 20px',
        border: '1px solid rgb(224, 224, 224)',
        borderRadius: '4px',
        '& .MuiTableCell-head': {
            position: 'relative',
            left: '6px',
        },
        '& .MuiTableCell-root': {
            textAlign: 'center',
            padding: '6px 10px',
            lineHeight: '15px',
        },
        '& .MuiTableRow-root:last-of-type .MuiTableCell-body': {
            borderBottomWidth: 0,
        },
        '& .MuiBox-root': {
            display: 'inline-flex',
            textDecoration: 'overline',
        },
        '& .set': {
            color: 'rgba(25, 118, 210, 0.7)',
        },
    },
});

export default function FlagsTable(props) {
    return (
        <TableContainer classes={useStyles()}>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={9}>Flags</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow key={"IE"}>
                        <TableCell>IE</TableCell>
                        <TableCell className={props.flags['EA'] ? 'set' : ''}>EA</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell className={props.flags['ES'] ? 'set' : ''}>ES</TableCell>
                        <TableCell className={props.flags['ET1'] ? 'set' : ''}>ET1</TableCell>
                        <TableCell className={props.flags['EX1'] ? 'set' : ''}>EX1</TableCell>
                        <TableCell className={props.flags['ET0'] ? 'set' : ''}>ET0</TableCell>
                        <TableCell className={props.flags['EX0'] ? 'set' : ''}>EX0</TableCell>
                    </TableRow>
                    <TableRow key={"IP"}>
                        <TableCell>IP</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell className={props.flags['PS'] ? 'set' : ''}>PS</TableCell>
                        <TableCell className={props.flags['PT1'] ? 'set' : ''}>PT1</TableCell>
                        <TableCell className={props.flags['PX1'] ? 'set' : ''}>PX1</TableCell>
                        <TableCell className={props.flags['PT0'] ? 'set' : ''}>PT0</TableCell>
                        <TableCell className={props.flags['PX0'] ? 'set' : ''}>PX0</TableCell>
                    </TableRow>
                    <TableRow key={"PSW"}>
                        <TableCell>PSW</TableCell>
                        <TableCell className={props.flags['C'] ? 'set' : ''}>C</TableCell>
                        <TableCell className={props.flags['AC'] ? 'set' : ''}>AC</TableCell>
                        <TableCell className={props.flags['F0'] ? 'set' : ''}>F0</TableCell>
                        <TableCell className={props.flags['RS1'] ? 'set' : ''}>RS1</TableCell>
                        <TableCell className={props.flags['RS0'] ? 'set' : ''}>RS0</TableCell>
                        <TableCell className={props.flags['OV'] ? 'set' : ''}>OV</TableCell>
                        <TableCell className={props.flags['F1'] ? 'set' : ''}>F1</TableCell>
                        <TableCell className={props.flags['P'] ? 'set' : ''}>P</TableCell>
                    </TableRow>
                    <TableRow key={"TCON"}>
                        <TableCell>TCON</TableCell>
                        <TableCell className={props.flags['TF1'] ? 'set' : ''}>TF1</TableCell>
                        <TableCell className={props.flags['TR1'] ? 'set' : ''}>TR1</TableCell>
                        <TableCell className={props.flags['TF0'] ? 'set' : ''}>TF0</TableCell>
                        <TableCell className={props.flags['TR0'] ? 'set' : ''}>TR0</TableCell>
                        <TableCell className={props.flags['IE1'] ? 'set' : ''}>IE1</TableCell>
                        <TableCell className={props.flags['IT1'] ? 'set' : ''}>IT1</TableCell>
                        <TableCell className={props.flags['IE0'] ? 'set' : ''}>IE0</TableCell>
                        <TableCell className={props.flags['IT0'] ? 'set' : ''}>IT0</TableCell>
                    </TableRow>
                    <TableRow key={"TMOD"}>
                        <TableCell>TMOD</TableCell>
                        <TableCell className={props.flags['T1_GATE'] ? 'set' : ''}>GATE</TableCell>
                        <TableCell className={props.flags['T1_CT'] ? 'set' : ''}>C/T</TableCell>
                        <TableCell className={props.flags['T1_M1'] ? 'set' : ''}>M1</TableCell>
                        <TableCell className={props.flags['T1_M0'] ? 'set' : ''}>M0</TableCell>
                        <TableCell className={props.flags['T0_GATE'] ? 'set' : ''}>GATE</TableCell>
                        <TableCell className={props.flags['T0_CT'] ? 'set' : ''}>
                            C/<Box>T</Box>
                        </TableCell>
                        <TableCell className={props.flags['T0_M1'] ? 'set' : ''}>M1</TableCell>
                        <TableCell className={props.flags['T0_M0'] ? 'set' : ''}>M0</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    );
}
