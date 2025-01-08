import pytest
import json
import os
from io import BytesIO
import pandas as pd
from backend.main import create_app
from backend.config import UPLOAD_FOLDER

@pytest.fixture
def app():
    """Create and configure a test Flask application"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def sample_pdf():
    """Create a sample PDF file for testing"""
    content = b"%PDF-1.4\nSample PDF content\nE1 F551 [EXCESS DUTY CLAIMED] [GU660061040] [25]"
    return (BytesIO(content), 'test.pdf')

@pytest.fixture
def sample_excel():
    """Create a sample Excel file for testing"""
    df = pd.DataFrame({
        'Filer Code': ['GU6'],
        'Entry Number': ['60061040'],
        '7501 Line Number': ['25'],
        'Additional Data': ['test']
    })
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    return (excel_buffer, 'test.xlsx')

class TestEndpoints:
    def test_upload_pdfs_valid(self, client, sample_pdf):
        """Test uploading valid PDF files"""
        data = {
            'files': (sample_pdf[0], sample_pdf[1])
        }
        response = client.post(
            '/api/upload-pdfs',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'record_count' in data
        assert data['message'].startswith('Successfully processed')

    def test_upload_pdfs_no_file(self, client):
        """Test uploading with no PDF files"""
        response = client.post('/api/upload-pdfs')
        assert response.status_code == 400
        assert b'No files provided' in response.data

    def test_upload_import_valid(self, client, sample_excel):
        """Test uploading valid Excel file"""
        data = {
            'file': (sample_excel[0], sample_excel[1])
        }
        response = client.post(
            '/api/upload-import',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'record_count' in data
        assert data['message'] == 'Successfully processed import record file'

    def test_upload_import_invalid_type(self, client):
        """Test uploading invalid file type"""
        data = {
            'file': (BytesIO(b'test'), 'test.txt')
        }
        response = client.post(
            '/api/upload-import',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        assert b'Invalid file type' in response.data

    def test_process_data_without_files(self, client):
        """Test processing without uploading files first"""
        response = client.post('/api/process-data')
        assert response.status_code == 400
        assert b'Please upload both PDF and Excel files first' in response.data

    @pytest.mark.integration
    def test_full_workflow(self, client, sample_pdf, sample_excel):
        """Test the complete workflow from upload to download"""
        # Upload PDF
        pdf_response = client.post(
            '/api/upload-pdfs',
            data={'files': (sample_pdf[0], sample_pdf[1])},
            content_type='multipart/form-data'
        )
        assert pdf_response.status_code == 200

        # Upload Excel
        excel_response = client.post(
            '/api/upload-import',
            data={'file': (sample_excel[0], sample_excel[1])},
            content_type='multipart/form-data'
        )
        assert excel_response.status_code == 200

        # Process data
        process_response = client.post('/api/process-data')
        assert process_response.status_code == 200
        process_data = json.loads(process_response.data)
        assert 'output_file' in process_data

        # Download result
        download_response = client.get(f"/api/download/{process_data['output_file']}")
        assert download_response.status_code == 200
        assert download_response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Clean up uploaded files after each test"""
        yield
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
