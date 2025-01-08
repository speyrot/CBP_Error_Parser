import os
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

class FileHandler:
    @staticmethod
    def allowed_file(filename: str, file_type: str) -> bool:
        """
        Check if the file extension is allowed
        
        Args:
            filename (str): Name of the file
            file_type (str): Type of file ('pdf' or 'excel')
            
        Returns:
            bool: True if file extension is allowed, False otherwise
        """
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

    @staticmethod
    def save_uploaded_file(file, file_type: str) -> str:
        """
        Save an uploaded file to the upload directory
        
        Args:
            file: File object from request
            file_type (str): Type of file ('pdf' or 'excel')
            
        Returns:
            str: Path to the saved file
            
        Raises:
            ValueError: If file type is not allowed
        """
        if file and FileHandler.allowed_file(file.filename, file_type):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to avoid conflicts
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(file_path)
            return file_path
        raise ValueError(f"Invalid file type. Allowed types for {file_type}: {ALLOWED_EXTENSIONS[file_type]}")

    @staticmethod
    def generate_output_file(df: pd.DataFrame) -> str:
        """
        Save the processed DataFrame as an Excel file
        
        Args:
            df (pd.DataFrame): Processed data to save
            
        Returns:
            str: Path to the generated Excel file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"processed_data_{timestamp}.xlsx"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        df.to_excel(output_path, index=False)
        return output_path

    @staticmethod
    def cleanup_old_files():
        """Remove files older than 1 hour from the upload directory"""
        # TODO: Implement cleanup logic for old files
        pass
