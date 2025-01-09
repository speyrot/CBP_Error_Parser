import React, { useState } from 'react';
import FileUpload from '../Components/FileUpload';
import ProgressTracker from '../Components/ProgressTracker';
import DownloadButton from '../Components/DownloadButton';
import Header from '../Components/Header';
import ProcessedDataViewer from '../Components/ProcessedDataViewer';
import { uploadPDFs, uploadImport, processData, getProcessedData, clearUploads } from '../Services/api';

const Home = () => {
    const [status, setStatus] = useState('');
    const [error, setError] = useState(null);
    const [outputFile, setOutputFile] = useState(null);
    const [processedRecords, setProcessedRecords] = useState([]);
    const [uploadedPDFs, setUploadedPDFs] = useState([]);

    const handlePDFUpload = async (files) => {
        try {
            setStatus('Uploading PDF files...');
            setError(null);
            console.log('Attempting to upload files:', files.map(f => f.name));
            await uploadPDFs(files);
            setUploadedPDFs(prev => [...prev, ...files.map(f => f.name)]);
            const response = await getProcessedData();
            setProcessedRecords(response.records);
            setStatus(`Successfully processed ${files.length} PDF files`);
        } catch (err) {
            const errorMessage = err.response?.data?.error || err.message || 'Failed to upload PDF files';
            console.error('PDF Upload Error:', {
                message: errorMessage,
                response: err.response?.data,
                status: err.response?.status
            });
            setError(errorMessage);
        }
    };

    const handleImportUpload = async (files) => {
        try {
            setStatus('Uploading import record file...');
            setError(null);
            await uploadImport(files[0]);
            setStatus('Successfully processed import record file');
        } catch (err) {
            let errorMessage = 'Failed to upload import file';
            if (err.response?.status === 413) {
                errorMessage = 'File is too large. Maximum size is 100MB.';
            } else {
                errorMessage = err.response?.data?.error || errorMessage;
            }
            console.error('Import Upload Error:', {
                message: errorMessage,
                response: err.response?.data,
                status: err.response?.status
            });
            setError(errorMessage);
        }
    };

    const handleProcessData = async () => {
        try {
            setStatus('Processing data...');
            setError(null);
            const response = await processData();
            setOutputFile(response.output_file);
            setStatus('Data processing complete');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to process data');
        }
    };

    const handleClearAll = async () => {
        try {
            await clearUploads();
            setUploadedPDFs([]);
            setProcessedRecords([]);
            setOutputFile(null);
            setError(null);
            setStatus('');
        } catch (err) {
            setError('Failed to clear uploads');
        }
    };

    return (
        <div>
            <Header />
            <div className="container">
                <div className="row mb-4">
                    <div className="col-md-6">
                        <h3>Upload CBP Error PDFs</h3>
                        {uploadedPDFs.length > 0 && (
                            <div className="mb-2">
                                <h6>Uploaded PDFs:</h6>
                                <ul className="list-unstyled">
                                    {uploadedPDFs.map((filename, index) => (
                                        <li key={index} className="text-success">
                                            <i className="bi bi-check-circle me-2"></i>
                                            {filename}
                                        </li>
                                    ))}
                                </ul>
                                <button 
                                    className="btn btn-sm btn-outline-danger mb-2"
                                    onClick={handleClearAll}
                                >
                                    Clear All
                                </button>
                            </div>
                        )}
                        <FileUpload type="pdf" onUpload={handlePDFUpload} multiple={true} />
                    </div>
                    <div className="col-md-6">
                        <h3>Upload Import Record Excel</h3>
                        <FileUpload type="excel" onUpload={handleImportUpload} multiple={false} />
                    </div>
                </div>

                <ProgressTracker status={status} error={error} message={status || error} />

                <div className="d-grid gap-2 d-md-flex justify-content-md-center">
                    <button 
                        className="btn btn-primary me-md-2" 
                        onClick={handleProcessData}
                        disabled={!!error}
                    >
                        Process Data
                    </button>
                    <DownloadButton filename={outputFile} disabled={!outputFile} />
                </div>

                <ProcessedDataViewer records={processedRecords} />
            </div>
        </div>
    );
};

export default Home;
