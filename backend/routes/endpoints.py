from flask import Blueprint, request, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
import os
import logging
from typing import List
import pandas as pd

from modules.pdf_parser import PDFParser
from modules.excel_parser import ExcelParser
from modules.matcher import Matcher
from modules.file_handler import FileHandler
from config import UPLOAD_FOLDER

# Create blueprint for API routes
api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Store uploaded file paths in memory (in a real app, you might want to use a proper session management)
uploaded_files = {
    'pdfs': [],
    'excel': None
}

@api.route('/upload-pdfs', methods=['POST'])
def upload_pdfs():
    """Handle upload of CBP error report PDFs"""
    logger.info("Received PDF upload request")
    logger.debug(f"Request Files: {request.files}")
    logger.debug(f"Request Form: {request.form}")
    
    if 'files' not in request.files:
        logger.error("No files in request")
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    logger.debug(f"Received {len(files)} files")
    
    if not files or files[0].filename == '':
        logger.error("No files selected")
        return jsonify({'error': 'No files selected'}), 400
    
    try:
        # Save and process each PDF
        if 'pdfs' not in uploaded_files:
            uploaded_files['pdfs'] = []
        error_dataframes = []
        
        for file in files:
            logger.debug(f"Processing file: {file.filename}")
            if FileHandler.allowed_file(file.filename, 'pdf'):
                file_path = FileHandler.save_uploaded_file(file, 'pdf')
                uploaded_files['pdfs'].append(file_path)
                
                try:
                    df = PDFParser.extract_error_data(file_path)
                    error_dataframes.append(df)
                except ValueError as e:
                    logger.error(f"Error processing file {file.filename}: {str(e)}")
                    return jsonify({'error': f"Error in file {file.filename}: {str(e)}"}), 400
            else:
                logger.error(f"Invalid file type: {file.filename}")
                return jsonify({'error': f'Invalid file type: {file.filename}'}), 400
        
        # Combine all error dataframes
        if error_dataframes:
            combined_df = PDFParser.combine_pdf_data(error_dataframes)
            record_count = len(combined_df)
        else:
            record_count = 0
        
        logger.info("Successfully processed all PDF files")
        return jsonify({
            'message': f'Successfully processed {len(files)} PDF files',
            'record_count': record_count
        }), 200
        
    except Exception as e:
        logger.exception("Error processing PDF files")
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
        logger.debug(f"Download requested for file: {filename}")
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        
        logger.info(f"Sending file: {filename}")
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        logger.exception(f"Error downloading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.after_request
def cleanup(response):
    """Clean up uploaded files after processing"""
    # TODO: Implement cleanup of old files
    return response

@api.route('/view-processed', methods=['GET'])
def view_processed():
    """Return the currently processed PDF data"""
    try:
        if not uploaded_files['pdfs']:
            return jsonify({'error': 'No PDFs have been processed yet'}), 404
        
        all_records = []
        processed_files = []
        for pdf_path in uploaded_files['pdfs']:
            try:
                df = PDFParser.extract_error_data(pdf_path)
                records = df.to_dict('records')
                all_records.extend(records)
                processed_files.append(os.path.basename(pdf_path))
            except Exception as e:
                logger.error(f"Error processing {pdf_path}: {str(e)}")
        
        return jsonify({
            'records': all_records,
            'count': len(all_records),
            'processed_files': processed_files
        }), 200
        
    except Exception as e:
        logger.exception("Error retrieving processed data")
        return jsonify({'error': str(e)}), 500

@api.route('/clear', methods=['POST'])
def clear_uploads():
    """Clear all uploaded files"""
    try:
        uploaded_files['pdfs'] = []
        uploaded_files['excel'] = None
        return jsonify({'message': 'Successfully cleared all uploads'}), 200
    except Exception as e:
        logger.exception("Error clearing uploads")
        return jsonify({'error': str(e)}), 500
