import pdfplumber
import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    # Updated pattern to correctly capture entry number from GU6 number
    ERROR_PATTERN = r'E1\s+F(\d{3})\s+([^G]+?)(?:GU6(\d+)\s+(\d+)\s+)?GU6\s+\d+'

    @staticmethod
    def extract_error_data(pdf_path: str) -> pd.DataFrame:
        """
        Extract error data from a CBP error report PDF
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            pd.DataFrame: DataFrame containing extracted error data
            
        Raises:
            ValueError: If no valid error records are found or if PDF parsing fails
        """
        try:
            logger.debug(f"Opening PDF file: {pdf_path}")
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    logger.debug(f"Page {page_num} text:\n{page_text}")
                    text += page_text + "\n"
            
            # Log the full text for debugging
            logger.debug("Full extracted text:")
            logger.debug(text)
            
            # Find all error records using regex
            matches = list(re.finditer(PDFParser.ERROR_PATTERN, text))
            logger.debug(f"Found {len(matches)} matches")
            
            if not matches:
                raise ValueError("No valid error records found in PDF")
            
            records = []
            for match in matches:
                error_code, error_desc, entry_number, line_number = match.groups()
                logger.debug(f"Matched groups: {match.groups()}")
                
                # If entry_number is None, try to extract it from the last GU6 number
                if entry_number is None:
                    # Look for the last GU6 number in the error description
                    last_gu6_match = re.search(r'GU6(\d+)(?:\s|$)', match.group(0))
                    if last_gu6_match:
                        entry_number = last_gu6_match.group(1)
                
                record = {
                    'Error Code': f'F{error_code}',
                    'Error Description': error_desc.strip(),
                    'Filer Code': 'GU6',
                    'Entry Number': entry_number.strip() if entry_number else '',
                    '7501 Line Number': line_number.strip() if line_number else ''
                }
                logger.debug(f"Created record: {record}")
                records.append(record)
            
            logger.info(f"Successfully found {len(records)} records")
            logger.debug(f"All records: {records}")
            return pd.DataFrame(records)
            
        except Exception as e:
            logger.exception(f"Error parsing PDF: {str(e)}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def combine_pdf_data(dataframes: list) -> pd.DataFrame:
        """
        Combine data from multiple PDFs into a single DataFrame
        
        Args:
            dataframes (list): List of DataFrames from individual PDFs
            
        Returns:
            pd.DataFrame: Combined DataFrame
        """
        if not dataframes:
            raise ValueError("No DataFrames provided")
            
        return pd.concat(dataframes, ignore_index=True)
