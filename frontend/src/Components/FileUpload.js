// frontend/src/Components/FileUpload.js

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB in bytes

const FileUpload = ({ type, onUpload, multiple = false }) => {
    const onDrop = useCallback(acceptedFiles => {
        console.log('Files dropped:', acceptedFiles);
        // Check file sizes
        const oversizedFiles = acceptedFiles.filter(file => file.size > MAX_FILE_SIZE);
        if (oversizedFiles.length > 0) {
            console.error('Files too large:', oversizedFiles.map(f => f.name));
            alert(`Some files are too large. Maximum size is 100MB per file.`);
            return;
        }
        acceptedFiles.forEach(file => {
            console.log('File:', {
                name: file.name,
                type: file.type,
                size: file.size
            });
        });
        onUpload(acceptedFiles);
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        multiple,
        maxSize: MAX_FILE_SIZE,
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