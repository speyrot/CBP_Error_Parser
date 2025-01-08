// frontend/src/Components/ProgressTracker.js

import React from 'react';

const ProgressTracker = ({ status, message, error }) => {
    return (
        <div className="progress-tracker mb-4">
            {status && (
                <div className={`alert ${error ? 'alert-danger' : 'alert-info'}`} role="alert">
                    <div className="d-flex align-items-center">
                        {!error && (
                            <div className="spinner-border spinner-border-sm me-2" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                        )}
                        <span>{message}</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ProgressTracker;