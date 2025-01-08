import React, { useState } from 'react';
import FileUpload from '../Components/FileUpload';
import ProgressTracker from '../Components/ProgressTracker';
import DownloadButton from '../Components/DownloadButton';
import Header from '../Components/Header';
import { uploadPDFs, uploadImport, processData } from '../Services/api';

const Home = () => {
    const [status, setStatus] = useState('');
    const [error, setError] = useState(null);
    const [outputFile, setOutputFile] = useState(null);

    const handlePDFUpload = async (files) => {
        try {
            setStatus('Uploading PDF files...');
            setError(null);
            await uploadPDFs(files);
            setStatus(`Successfully processed ${files.length} PDF files`);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to upload PDF files');
        }
    };

    const handleImportUpload = async (files) => {
        try {
            setStatus('Uploading import record file...');
            setError(null);
            await uploadImport(files[0]);
            setStatus('Successfully processed import record file');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to upload import file');
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

    return (
        <div>
            <Header />
            <div className="container">
                <div className="row mb-4">
                    <div className="col-md-6">
                        <h3>Upload CBP Error PDFs</h3>
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
            </div>
        </div>
    );
};

export default Home;
