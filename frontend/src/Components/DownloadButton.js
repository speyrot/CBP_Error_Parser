import React from 'react';

const DownloadButton = ({ filename, disabled }) => {
    const handleDownload = () => {
        window.location.href = `http://localhost:5000/api/download/${filename}`;
    };

    return (
        <button
            className="btn btn-success"
            onClick={handleDownload}
            disabled={disabled}
        >
            Download Processed File
        </button>
    );
};

export default DownloadButton;
