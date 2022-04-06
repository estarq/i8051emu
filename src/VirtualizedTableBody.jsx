import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {TableBody} from '@material-ui/core';
import AutoSizer from 'react-virtualized/dist/commonjs/AutoSizer';
import MuiTable from 'mui-virtualized-table';

const useStyles = makeStyles({
    root: {
        '& .MuiTableCell-root': {
            backgroundColor: 'rgb(255, 255, 255)',
            borderTop: '1px solid rgb(224, 224, 224)',
        },
        '& .MuiTableCell-root:first-of-type, & .MuiTableCell-root:nth-of-type(2)': {
            borderTopWidth: '0px',
        },
        '& .MuiTable-cellContents-12': {
            position: 'relative',
            top: '-3px',
        },
        '& .ReactVirtualized__Grid': {
            overflowX: 'hidden !important',
        },
    },
});

export default function VirtualizedTableBody({data}) {
    return (
        <TableBody classes={useStyles()}>
            <AutoSizer>
                {() => (
                    <MuiTable
                        data={data}
                        width={140}
                        maxHeight={476}
                        rowHeight={28}
                        columns={[
                            {width: 72, cell: data => <div>{data.addr}</div>},
                            {width: 68, cell: data => <div>{data.value}</div>},
                        ]}
                    />
                )}
            </AutoSizer>
        </TableBody>
    );
}
