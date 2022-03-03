import './Table.css';

const Table = (props) => {
    const { columnNames, rowData } = props;

    return (
        <>
        <div class="tbl-header">
            <table cellpadding="0" cellspacing="0" border="0">
            <thead>
                <tr>
                {
                    columnNames.map(col => <th>{ col }</th>)
                }
                </tr>
            </thead>
            </table>
        </div>
        <div class="tbl-content">
            <table cellpadding="0" cellspacing="0" border="0">
            <tbody>
                {
                    rowData.map(row => 
                        <tr>
                            { columnNames.map( col => <td>{ row[col] }</td>)}
                        </tr>)
                }
            </tbody>
            </table>
        </div>
    </>
    )
}


export default Table;