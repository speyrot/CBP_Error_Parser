import pytest
import pandas as pd
import os
from backend.modules.file_handler import FileHandler
from werkzeug.datastructures import FileStorage
from io import BytesIO

class TestFileHandler:
    def test_allowed_file_pdf(self):
        """Test PDF file validation"""
        assert FileHandler.allowed_file('test.pdf', 'pdf') == True
        assert FileHandler.allowed_file('test.txt', 'pdf') == False

    def test_allowed_file_excel(self):
        """Test Excel file validation"""
        assert FileHandler.allowed_file('test.xlsx', 'excel') == True
        assert FileHandler.allowed_file('test.xls', 'excel') == True
        assert FileHandler.allowed_file('test.csv', 'excel') == False

    @pytest.mark.integration
    def test_save_uploaded_file(self, tmp_path):
        """Test saving an uploaded file"""
        # Create a mock file
        content = b"test content"
        file = FileStorage(
            stream=BytesIO(content),
            filename="test.pdf",
            content_type="application/pdf",
        )
        
        # Test saving the file
        file_path = FileHandler.save_uploaded_file(file, 'pdf')
        assert os.path.exists(file_path)
        assert file_path.endswith('.pdf')

    def test_generate_output_file(self, tmp_path):
        """Test generating output Excel file"""
        df = pd.DataFrame({
            'Test Column': ['test data']
        })
        
        output_path = FileHandler.generate_output_file(df)
        assert os.path.exists(output_path)
        assert output_path.endswith('.xlsx')
        
        # Verify the file can be read back
        df_read = pd.read_excel(output_path)
        assert len(df_read) == len(df)
        assert list(df_read.columns) == list(df.columns) 