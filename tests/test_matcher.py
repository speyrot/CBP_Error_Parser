import pytest
import pandas as pd
from backend.modules.matcher import Matcher

# Test data
ERROR_DATA = {
    'Error Description': ['EXCESS DUTY CLAIMED', 'INVALID HTS CODE'],
    'Filer Code': ['ABC', 'DEF'],
    'Entry Number': ['12345', '67890'],
    '7501 Line Number': ['1', '2']
}

IMPORT_DATA = {
    'Filer Code': ['ABC', 'DEF', 'GHI'],
    'Entry Number': ['12345', '67890', '11111'],
    '7501 Line Number': ['1', '2', '3'],
    'Additional Data': ['data1', 'data2', 'data3']
}

class TestMatcher:
    def test_match_records_valid(self):
        """Test matching with valid records that should have matches"""
        error_df = pd.DataFrame(ERROR_DATA)
        import_df = pd.DataFrame(IMPORT_DATA)
        
        result = Matcher.match_records(error_df, import_df)
        assert len(result) == 2  # Should find two matches
        assert 'Error Description' in result.columns
        assert 'Additional Data' in result.columns

    def test_match_records_no_matches(self):
        """Test matching with no matching records"""
        error_df = pd.DataFrame({
            'Error Description': ['TEST'],
            'Filer Code': ['XXX'],
            'Entry Number': ['99999'],
            '7501 Line Number': ['9']
        })
        import_df = pd.DataFrame(IMPORT_DATA)
        
        with pytest.raises(ValueError, match="No matching records found"):
            Matcher.match_records(error_df, import_df)

    def test_format_output(self):
        """Test output formatting"""
        # Create a merged DataFrame with mixed column order
        merged_data = {
            'Additional Data': ['data1'],
            'Error Description': ['ERROR'],
            'Random Column': ['random'],
            'Filer Code': ['ABC'],
            'Entry Number': ['12345'],
            '7501 Line Number': ['1']
        }
        df = pd.DataFrame(merged_data)
        
        result = Matcher.format_output(df)
        
        # Check if error information columns come first
        first_columns = list(result.columns)[:4]
        expected_first = ['Error Description', 'Filer Code', 'Entry Number', '7501 Line Number']
        assert first_columns == expected_first

    def test_data_type_conversion(self):
        """Test that numeric values are handled correctly"""
        error_df = pd.DataFrame({
            'Error Description': ['ERROR'],
            'Filer Code': ['ABC'],
            'Entry Number': [12345],  # Numeric
            '7501 Line Number': [1]   # Numeric
        })
        
        import_df = pd.DataFrame({
            'Filer Code': ['ABC'],
            'Entry Number': ['12345'],  # String
            '7501 Line Number': ['1'],  # String
            'Additional Data': ['data']
        })
        
        result = Matcher.match_records(error_df, import_df)
        assert len(result) == 1  # Should match despite different data types
