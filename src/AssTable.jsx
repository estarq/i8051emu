import * as React from 'react';
import {DataGrid} from '@mui/x-data-grid';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles({
    root: {
        height: '543px',
        width: '550px',
        margin: '20px',
        '& .MuiDataGrid-columnHeader:last-of-type .MuiDataGrid-iconSeparator': {
            display: 'none',
        },
        '& .MuiDataGrid-cell:focus, & .MuiDataGrid-columnHeader:focus': {
            outline: 'none',
        },
    },
});

const columns = [
    {field: 'addr', headerName: 'Addr', width: 70, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'bytes', headerName: 'Bytes', width: 70, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'opcode', headerName: 'Opcode', width: 90, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'arg1', headerName: 'Arg1', width: 70, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'arg2', headerName: 'Arg2', width: 70, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'mnemonic', headerName: 'Mnemonic', width: 175, headerAlign: 'center', align: 'center', sortable: false},
];

export default function AssTable(props) {
    return (
        <DataGrid
            classes={useStyles()}
            rows={props.rows}
            rowsPerPageOptions={[]}
            autoPageSize={true}
            getRowId={(row) => row.addr}
            columns={columns}
            disableColumnMenu={true}
            density={"compact"}
            hideFooterSelectedRowCount={true}
            selectionModel={props.currentAddr}
        />
    );
}
