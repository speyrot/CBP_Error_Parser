import axios from 'axios';

export const API_BASE_URL = 'http://localhost:5001/api';

export const uploadPDFs = async (files) => {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });
    console.log('Uploading files:', files);
    
    const response = await axios.post(`${API_BASE_URL}/upload-pdfs`, formData);
    return response.data;
};

export const uploadImport = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API_BASE_URL}/upload-import`, formData);
    return response.data;
};

export const processData = async () => {
    const response = await axios.post(`${API_BASE_URL}/process-data`);
    return response.data;
};

export const getProcessedData = async () => {
    const response = await axios.get(`${API_BASE_URL}/view-processed`);
    return response.data;
};

export const clearUploads = async () => {
    const response = await axios.post(`${API_BASE_URL}/clear`);
    return response.data;
};
