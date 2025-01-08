import pdfplumber
import pandas as pd
import re
from typing import List, Dict

class PDFParser:
    @staticmethod
    def extract_error_data(file_path: str) -> pd.DataFrame:
        """
        Extract error information from a CBP error report PDF
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            pd.DataFrame: DataFrame containing extracted error data with columns:
                - Error Description
                - Filer Code
                - Entry Number
                - 7501 Line Number
                
        Raises:
            ValueError: If PDF parsing fails or required data cannot be extracted
        """
        error_records = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    # Process each line of the page
                    for line in text.split('\n'):
                        error_data = PDFParser._parse_error_line(line)
                        if error_data:
                            error_records.append(error_data)
            
            if not error_records:
                raise ValueError("No valid error records found in PDF")
            
            return pd.DataFrame(error_records)
        
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def _parse_error_line(line: str) -> Dict[str, str]:
        """
        Parse a single line from the PDF to extract error information
        
        Args:
            line (str): Single line of text from the PDF
            
        Returns:
            dict: Dictionary containing extracted fields, or None if line doesn't match expected format
        """
        # Example pattern: E1 F551 [EXCESS DUTY CLAIMED] [GU660061040] [25]
        pattern = r'\[(.*?)\]\s*\[([A-Z0-9]+)\]\s*\[(\d+)\]'
        
        match = re.search(pattern, line)
        if match:
            error_desc, entry_full, line_num = match.groups()
            
            # Split entry number into filer code (first 3) and entry number (rest)
            filer_code = entry_full[:3]
            entry_number = entry_full[3:]
            
            return {
                'Error Description': error_desc.strip(),
                'Filer Code': filer_code,
                'Entry Number': entry_number,
                '7501 Line Number': line_num
            }
        
        return None

    @staticmethod
    def combine_pdf_data(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Combine data from multiple PDFs into a single DataFrame
        
        Args:
            dataframes (List[pd.DataFrame]): List of DataFrames from individual PDFs
            
        Returns:
            pd.DataFrame: Combined DataFrame with all error records
        """
        if not dataframes:
            raise ValueError("No DataFrames provided to combine")
        
        return pd.concat(dataframes, ignore_index=True)
