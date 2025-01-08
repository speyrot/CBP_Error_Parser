// frontend/src/Components/FileUpload.js

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const FileUpload = ({ type, onUpload, multiple = false }) => {
    const onDrop = useCallback(acceptedFiles => {
        onUpload(acceptedFiles);
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        multiple,
        accept: type === 'pdf' 
            ? { 'application/pdf': ['.pdf'] }
            : { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'], 'application/vnd.ms-excel': ['.xls'] }
    });

    return (
        <div 
            {...getRootProps()} 
            className={`dropzone ${isDragActive ? 'active' : ''}`}
            style={{
                border: '2px dashed #cccccc',
                borderRadius: '4px',
                padding: '20px',
                textAlign: 'center',
                cursor: 'pointer',
                marginBottom: '20px',
                backgroundColor: isDragActive ? '#f8f9fa' : 'white'
            }}
        >
            <input {...getInputProps()} />
            {isDragActive ? (
                <p>Drop the {type === 'pdf' ? 'PDF files' : 'Excel file'} here...</p>
            ) : (
                <p>
                    Drag and drop {type === 'pdf' ? 'PDF files' : 'an Excel file'} here, or click to select
                    {type === 'pdf' ? ' files' : ' file'}
                </p>
            )}
        </div>
    );
};

export default FileUpload;