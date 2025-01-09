import React from 'react';
import { API_BASE_URL } from '../Services/api';

const DownloadButton = ({ filename, disabled }) => {
    const handleDownload = () => {
        if (filename) {
            window.location.href = `${API_BASE_URL}/download/${filename}`;
        }
    };

    return (
        <button
            className="btn btn-success"
            onClick={handleDownload}
            disabled={disabled}
        >
            Download Results
        </button>
    );
};

export default DownloadButton;
