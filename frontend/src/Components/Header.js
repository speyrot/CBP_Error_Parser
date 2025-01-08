import React from 'react';

const Header = () => {
    return (
        <header className="bg-light py-4 mb-4">
            <div className="container">
                <h1 className="mb-3">CBP Error Processor</h1>
                <p className="lead mb-0">
                    Upload CBP error PDFs and import records to identify and match problematic entries.
                </p>
            </div>
        </header>
    );
};

export default Header;
