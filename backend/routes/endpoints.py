from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from typing import List
import pandas as pd

from modules.pdf_parser import PDFParser
from modules.excel_parser import ExcelParser
from modules.matcher import Matcher
from modules.file_handler import FileHandler
from config import UPLOAD_FOLDER

# Create blueprint for API routes
api = Blueprint('api', __name__)

# Store uploaded file paths in memory (in a real app, you might want to use a proper session management)
uploaded_files = {
    'pdfs': [],
    'excel': None
}

@api.route('/upload-pdfs', methods=['POST'])
def upload_pdfs():
    """Handle upload of CBP error report PDFs"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    try:
        # Save and process each PDF
        uploaded_files['pdfs'] = []
        error_dataframes = []
        
        for file in files:
            if FileHandler.allowed_file(file.filename, 'pdf'):
                # Save the file
                file_path = FileHandler.save_uploaded_file(file, 'pdf')
                uploaded_files['pdfs'].append(file_path)
                
                # Parse the PDF
                df = PDFParser.extract_error_data(file_path)
                error_dataframes.append(df)
            else:
                return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
        
        # Combine data from all PDFs
        if error_dataframes:
            combined_df = PDFParser.combine_pdf_data(error_dataframes)
            return jsonify({
                'message': f'Successfully processed {len(files)} PDF files',
                'record_count': len(combined_df)
            }), 200
        
        return jsonify({'error': 'No valid data found in PDFs'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/upload-import', methods=['POST'])
def upload_import():
    """Handle upload of import record Excel file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        if FileHandler.allowed_file(file.filename, 'excel'):
            # Save the file
            file_path = FileHandler.save_uploaded_file(file, 'excel')
            uploaded_files['excel'] = file_path
            
            # Validate and process the Excel file
            df = ExcelParser.read_import_file(file_path)
            df = ExcelParser.clean_data(df)
            
            return jsonify({
                'message': 'Successfully processed import record file',
                'record_count': len(df)
            }), 200
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/process-data', methods=['POST'])
def process_data():
    """Match error data with import records and generate output"""
    if not uploaded_files['pdfs'] or not uploaded_files['excel']:
        return jsonify({'error': 'Please upload both PDF and Excel files first'}), 400
    
    try:
        # Process PDFs
        error_dataframes = [
            PDFParser.extract_error_data(pdf_path)
            for pdf_path in uploaded_files['pdfs']
        ]
        error_df = PDFParser.combine_pdf_data(error_dataframes)
        
        # Process Excel
        import_df = ExcelParser.read_import_file(uploaded_files['excel'])
        import_df = ExcelParser.clean_data(import_df)
        
        # Match records
        matched_df = Matcher.match_records(error_df, import_df)
        formatted_df = Matcher.format_output(matched_df)
        
        # Generate output file
        output_path = FileHandler.generate_output_file(formatted_df)
        
        return jsonify({
            'message': 'Successfully processed data',
            'matched_records': len(formatted_df),
            'output_file': os.path.basename(output_path)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download the processed output file"""
    try:
        return send_file(
            os.path.join(UPLOAD_FOLDER, filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.after_request
def cleanup(response):
    """Clean up uploaded files after processing"""
    # TODO: Implement cleanup of old files
    return response
