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
        margin: '0px 0px 26px 20px',
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
        '& .MuiTableRow-root:last-of-type': {
            '& .MuiTableCell-body': {
                borderBottomWidth: '0px',
            },
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

export default function FlagsTable({flags}) {
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
                        <TableCell className={flags.ea ? 'set' : ''}>EA</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell className={flags.es ? 'set' : ''}>ES</TableCell>
                        <TableCell className={flags.et1 ? 'set' : ''}>ET1</TableCell>
                        <TableCell className={flags.ex1 ? 'set' : ''}>EX1</TableCell>
                        <TableCell className={flags.et0 ? 'set' : ''}>ET0</TableCell>
                        <TableCell className={flags.ex0 ? 'set' : ''}>EX0</TableCell>
                    </TableRow>
                    <TableRow key={"IP"}>
                        <TableCell>IP</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell>-</TableCell>
                        <TableCell className={flags.ps ? 'set' : ''}>PS</TableCell>
                        <TableCell className={flags.pt1 ? 'set' : ''}>PT1</TableCell>
                        <TableCell className={flags.px1 ? 'set' : ''}>PX1</TableCell>
                        <TableCell className={flags.pt0 ? 'set' : ''}>PT0</TableCell>
                        <TableCell className={flags.px0 ? 'set' : ''}>PX0</TableCell>
                    </TableRow>
                    <TableRow key={"PSW"}>
                        <TableCell>PSW</TableCell>
                        <TableCell className={flags.c ? 'set' : ''}>C</TableCell>
                        <TableCell className={flags.ac ? 'set' : ''}>AC</TableCell>
                        <TableCell className={flags.f0 ? 'set' : ''}>F0</TableCell>
                        <TableCell className={flags.rs1 ? 'set' : ''}>RS1</TableCell>
                        <TableCell className={flags.rs0 ? 'set' : ''}>RS0</TableCell>
                        <TableCell className={flags.ov ? 'set' : ''}>OV</TableCell>
                        <TableCell className={flags.f1 ? 'set' : ''}>F1</TableCell>
                        <TableCell className={flags.p ? 'set' : ''}>P</TableCell>
                    </TableRow>
                    <TableRow key={"TCON"}>
                        <TableCell>TCON</TableCell>
                        <TableCell className={flags.tf1 ? 'set' : ''}>TF1</TableCell>
                        <TableCell className={flags.tr1 ? 'set' : ''}>TR1</TableCell>
                        <TableCell className={flags.tf0 ? 'set' : ''}>TF0</TableCell>
                        <TableCell className={flags.tr0 ? 'set' : ''}>TR0</TableCell>
                        <TableCell className={flags.ie1 ? 'set' : ''}>IE1</TableCell>
                        <TableCell className={flags.it1 ? 'set' : ''}>IT1</TableCell>
                        <TableCell className={flags.ie0 ? 'set' : ''}>IE0</TableCell>
                        <TableCell className={flags.it0 ? 'set' : ''}>IT0</TableCell>
                    </TableRow>
                    <TableRow key={"TMOD"}>
                        <TableCell>TMOD</TableCell>
                        <TableCell className={flags.t1_gate ? 'set' : ''}>GATE</TableCell>
                        <TableCell className={flags.t1_ct ? 'set' : ''}>C/T</TableCell>
                        <TableCell className={flags.t1_m1 ? 'set' : ''}>M1</TableCell>
                        <TableCell className={flags.t1_m0 ? 'set' : ''}>M0</TableCell>
                        <TableCell className={flags.t0_gate ? 'set' : ''}>GATE</TableCell>
                        <TableCell className={flags.t0_ct ? 'set' : ''}>
                            C/<Box>T</Box>
                        </TableCell>
                        <TableCell className={flags.t0_m1 ? 'set' : ''}>M1</TableCell>
                        <TableCell className={flags.t0_m0 ? 'set' : ''}>M0</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    );
}
