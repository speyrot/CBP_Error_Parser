import pytest
import pandas as pd
from backend.modules.pdf_parser import PDFParser
import os

# Test data
SAMPLE_ERROR_LINE = "E1 F551 [EXCESS DUTY CLAIMED] [GU660061040] [25]"
EXPECTED_PARSED_DATA = {
    'Error Description': 'EXCESS DUTY CLAIMED',
    'Filer Code': 'GU6',
    'Entry Number': '60061040',
    '7501 Line Number': '25'
}

class TestPDFParser:
    def test_parse_error_line_valid(self):
        """Test parsing a valid error line"""
        result = PDFParser._parse_error_line(SAMPLE_ERROR_LINE)
        assert result == EXPECTED_PARSED_DATA

    def test_parse_error_line_invalid(self):
        """Test parsing an invalid error line"""
        result = PDFParser._parse_error_line("Invalid line format")
        assert result is None

    def test_combine_pdf_data_valid(self):
        """Test combining multiple DataFrames"""
        df1 = pd.DataFrame([EXPECTED_PARSED_DATA])
        df2 = pd.DataFrame([EXPECTED_PARSED_DATA])
        
        result = PDFParser.combine_pdf_data([df1, df2])
        assert len(result) == 2
        assert list(result.columns) == list(EXPECTED_PARSED_DATA.keys())

    def test_combine_pdf_data_empty(self):
        """Test combining with empty list of DataFrames"""
        with pytest.raises(ValueError, match="No DataFrames provided to combine"):
            PDFParser.combine_pdf_data([])

    @pytest.mark.integration
    def test_extract_error_data(self, tmp_path):
        """Integration test for PDF parsing (requires sample PDF)"""
        # TODO: Create a sample PDF file for testing
        pass
