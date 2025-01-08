import pytest
import pandas as pd
from backend.modules.excel_parser import ExcelParser

# Test data
SAMPLE_DATA = {
    'Filer Code': ['ABC', 'DEF'],
    'Entry Number': ['12345', '67890'],
    '7501 Line Number': ['1', '2'],
    'Extra Column': ['data1', 'data2']
}

class TestExcelParser:
    def test_validate_columns_valid(self):
        """Test validation with valid columns"""
        df = pd.DataFrame(SAMPLE_DATA)
        ExcelParser._validate_columns(df)  # Should not raise exception

    def test_validate_columns_missing(self):
        """Test validation with missing columns"""
        df = pd.DataFrame({'Filer Code': [], 'Entry Number': []})  # Missing 7501 Line Number
        with pytest.raises(ValueError, match="Import file is missing required columns"):
            ExcelParser._validate_columns(df)

    def test_clean_data(self):
        """Test data cleaning functionality"""
        # Create DataFrame with spaces and duplicates
        df = pd.DataFrame({
            'Filer Code': [' ABC ', 'ABC'],  # Duplicate with spaces
            'Entry Number': ['12345', '12345'],
            '7501 Line Number': ['1', '1']
        })
        
        result = ExcelParser.clean_data(df)
        assert len(result) == 1  # Should remove duplicate
        assert result['Filer Code'].iloc[0] == 'ABC'  # Should strip spaces

    @pytest.mark.integration
    def test_read_import_file(self, tmp_path):
        """Integration test for Excel file reading"""
        # Create a temporary Excel file
        df = pd.DataFrame(SAMPLE_DATA)
        file_path = tmp_path / "test_import.xlsx"
        df.to_excel(file_path, index=False)
        
        result = ExcelParser.read_import_file(str(file_path))
        assert len(result) == len(SAMPLE_DATA['Filer Code'])
        assert all(col in result.columns for col in ExcelParser.REQUIRED_COLUMNS)
