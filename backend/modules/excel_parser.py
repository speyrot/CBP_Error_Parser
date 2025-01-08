import pandas as pd
from typing import List, Set

class ExcelParser:
    # Required columns in the import record Excel file
    REQUIRED_COLUMNS = {'Filer Code', 'Entry Number', '7501 Line Number'}
    
    @staticmethod
    def read_import_file(file_path: str) -> pd.DataFrame:
        """
        Read and validate the import record Excel file
        
        Args:
            file_path (str): Path to the Excel file
            
        Returns:
            pd.DataFrame: Validated DataFrame containing import records
            
        Raises:
            ValueError: If file is invalid or missing required columns
        """
        try:
            df = pd.read_excel(file_path)
            ExcelParser._validate_columns(df)
            
            # Convert numeric columns to string for consistent matching
            df['Entry Number'] = df['Entry Number'].astype(str)
            df['7501 Line Number'] = df['7501 Line Number'].astype(str)
            
            return df
            
        except Exception as e:
            raise ValueError(f"Failed to process Excel file: {str(e)}")

    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> None:
        """
        Validate that the DataFrame contains all required columns
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            
        Raises:
            ValueError: If any required columns are missing
        """
        missing_columns = ExcelParser.REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"Import file is missing required columns: {', '.join(missing_columns)}"
            )

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize the import record data
        
        Args:
            df (pd.DataFrame): DataFrame to clean
            
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        # Create a copy to avoid modifying the original
        cleaned_df = df.copy()
        
        # Remove any leading/trailing whitespace
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                cleaned_df[col] = cleaned_df[col].str.strip()
        
        # Remove any duplicate records
        cleaned_df = cleaned_df.drop_duplicates()
        
        # Reset the index after cleaning
        return cleaned_df.reset_index(drop=True)
