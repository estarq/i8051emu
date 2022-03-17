import * as React from 'react';
import {DataGrid} from '@mui/x-data-grid';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles({
    root: {
        height: '531px',
        width: '442px',
        '& .MuiDataGrid-columnHeader': {
            padding: '0px',
        },
        '& .MuiDataGrid-columnSeparator': {
            display: 'none',
        },
        '& .MuiDataGrid-cell': {
            lineHeight: '15px',
        },
        '& .MuiDataGrid-cell:focus, & .MuiDataGrid-columnHeader:focus': {
            outline: 'none',
        },
    },
});

const columns = [
    {field: 'addr', headerName: 'Addr', width: 50, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'bytes', headerName: 'Bytes', width: 50, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'opcode', headerName: 'Opcode', width: 65, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'arg1', headerName: 'Arg1', width: 50, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'arg2', headerName: 'Arg2', width: 50, headerAlign: 'center', align: 'center', sortable: false},
    {field: 'mnemonic', headerName: 'Mnemonic', width: 175, headerAlign: 'center', align: 'center', sortable: false},
];

export default function AssTable({rows, currentAddr}) {
    return (
        <DataGrid
            classes={useStyles()}
            rows={rows}
            rowsPerPageOptions={[]}
            rowHeight={40}
            headerHeight={40}
            autoPageSize={true}
            getRowId={(row) => row.addr}
            columns={columns}
            disableColumnMenu={true}
            density={"compact"}
            hideFooterSelectedRowCount={true}
            selectionModel={currentAddr}
        />
    );
}
