import pandas as pd
import logging

logger = logging.getLogger(__name__)

class ExcelParser:
    # Define column mappings (Excel column name -> Internal column name)
    COLUMN_MAPPINGS = {
        'Filer': 'Filer Code',
        'Entry No.': 'Entry Number',
        '7501 Line Number': '7501 Line Number'  # This one matches already
    }
    
    # Required columns in the import record Excel file (using Excel column names)
    REQUIRED_COLUMNS = {'Filer', 'Entry No.', '7501 Line Number'}
    
    # Date columns that need special handling
    DATE_COLUMNS = ['Import Date', 'Arrival Date', 'Liq. Date']
    
    @staticmethod
    def read_import_file(file_path: str) -> pd.DataFrame:
        """Read and validate the import record Excel file"""
        try:
            logger.debug(f"Reading Excel file: {file_path}")
            # Parse dates when reading Excel file
            df = pd.read_excel(file_path, parse_dates=ExcelParser.DATE_COLUMNS)
            logger.debug(f"Excel columns found: {list(df.columns)}")
            
            # Validate columns
            ExcelParser._validate_columns(df)
            
            # Rename columns to match internal names
            df = ExcelParser._rename_columns(df)
            
            # Clean and standardize data
            df = ExcelParser.clean_data(df)
            
            logger.info(f"Successfully processed Excel file with {len(df)} records")
            return df
            
        except Exception as e:
            logger.exception(f"Error processing Excel file: {str(e)}")
            raise ValueError(f"Failed to process Excel file: {str(e)}")

    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> None:
        """Validate that the DataFrame contains all required columns"""
        logger.debug("Validating Excel columns...")
        current_columns = set(df.columns)
        missing_columns = ExcelParser.REQUIRED_COLUMNS - current_columns
        
        if missing_columns:
            error_msg = f"Import file is missing required columns: {', '.join(missing_columns)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.debug("Column validation successful")

    @staticmethod
    def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Rename Excel columns to match internal column names"""
        logger.debug("Renaming columns to match internal names...")
        return df.rename(columns=ExcelParser.COLUMN_MAPPINGS)

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize the import record data"""
        logger.debug("Cleaning Excel data...")
        # Create a copy to avoid modifying the original
        cleaned_df = df.copy()
        
        # Remove any leading/trailing whitespace from string columns
        for col in cleaned_df.columns:
            if cleaned_df[col].dtype == 'object':
                cleaned_df[col] = cleaned_df[col].str.strip()
        
        # Handle missing values
        cleaned_df['7501 Line Number'] = cleaned_df['7501 Line Number'].fillna('')
        cleaned_df['Filer Code'] = cleaned_df['Filer Code'].fillna('')
        cleaned_df['Entry Number'] = cleaned_df['Entry Number'].fillna('')
        
        # Format date columns
        for date_col in ExcelParser.DATE_COLUMNS:
            if date_col in cleaned_df.columns:
                cleaned_df[date_col] = pd.to_datetime(cleaned_df[date_col], errors='coerce')
                # Format dates as strings in a consistent format
                cleaned_df[date_col] = cleaned_df[date_col].dt.strftime('%Y-%m-%d')
        
        # Remove any duplicate records
        cleaned_df = cleaned_df.drop_duplicates()
        
        # Reset the index after cleaning
        cleaned_df = cleaned_df.reset_index(drop=True)
        
        logger.debug(f"Data cleaning complete. {len(cleaned_df)} records remaining")
        return cleaned_df
