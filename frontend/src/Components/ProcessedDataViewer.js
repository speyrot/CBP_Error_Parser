import React from 'react';

const ProcessedDataViewer = ({ records }) => {
    if (!records || records.length === 0) {
        return null;
    }

    // Group records by Entry Number to show errors by file
    const groupedRecords = records.reduce((acc, record) => {
        const key = record['Entry Number'];
        if (!acc[key]) {
            acc[key] = [];
        }
        acc[key].push(record);
        return acc;
    }, {});

    return (
        <div className="mt-4">
            <h4>Processed Errors (Total: {records.length})</h4>
            <div className="mb-3">
                <h6>Summary:</h6>
                {Object.entries(groupedRecords).map(([entryNum, entries]) => (
                    <div key={entryNum} className="mb-2">
                        <strong>Entry {entryNum}:</strong> {entries.length} errors
                    </div>
                ))}
            </div>
            <div className="table-responsive">
                <table className="table table-striped table-bordered">
                    <thead>
                        <tr>
                            <th>Error Code</th>
                            <th>Error Description</th>
                            <th>Filer Code</th>
                            <th>Entry Number</th>
                            <th>7501 Line Number</th>
                        </tr>
                    </thead>
                    <tbody>
                        {records.map((record, index) => (
                            <tr key={index}>
                                <td>{record['Error Code']}</td>
                                <td>{record['Error Description']}</td>
                                <td>{record['Filer Code']}</td>
                                <td>{record['Entry Number']}</td>
                                <td>{record['7501 Line Number']}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ProcessedDataViewer; 