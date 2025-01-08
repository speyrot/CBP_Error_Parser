Backend Structure Doc

Purpose:
The backend will handle:
1. Parsing CBP error report PDFs to extract relevant data.
2. Converting the parsed data into a structured Excel file.
3. Comparing the parsed error data with an uploaded import record Excel file to isolate matching records.
4. Returning the final processed Excel file to the frontend.

Module Structure:
The backend will be divided into the following modules for maintainability and clear separation of concerns:
1. pdf_parser Module
    - Purpose: Extract relevant data (e.g., error description, filer code, entry number, 7501 line number) from CBP error report PDFs.
    - Functions:
        - parse_pdf(file_path: str) -> pd.DataFrame
            - Input: Path to the uploaded PDF.
            - Output: A pandas DataFrame with extracted fields:
                - Error Description
                - Filer Code
                - Entry Number
                - 7501 Line Number
        - Dependencies: pdfplumber, pandas

2. excel_parser Module
    - Purpose: Handle operations related to the import record Excel file.
    - Functions:
        - read_import_excel(file_path: str) -> pd.DataFrame
            - Input: Path to the uploaded Excel file.
            - Output: A pandas DataFrame with validated import record data.
        - validate_import_file(df: pd.DataFrame) -> bool
            - Input: A DataFrame of the import records.
            - Output: True if the required columns exist; otherwise, raise a validation error.
        - Dependencies: pandas, openpyxl

3. matcher Module
    - Purpose: Match parsed error data with the import record data and generate the final output.
    - Functions:
        - match_errors_to_imports(errors_df: pd.DataFrame, imports_df: pd.DataFrame) -> pd.DataFrame
            - Input: DataFrames of parsed error data and import records.
            - Output: A DataFrame of matched records with error details prepended to the rows.
        - Dependencies: pandas

4. file_handler Module
    - Purpose: Manage file operations, including saving uploaded files and serving the final processed file.
    - Functions:
        - save_uploaded_file(file, file_type: str) -> str
            - Input: File object and its type (pdf or excel).
            - Output: Path to the saved file.
        - generate_output_file(df: pd.DataFrame, output_path: str)
            - Input: The processed DataFrame and output file path.
            - Output: Saves the DataFrame as an Excel file at the specified location.
        - Dependencies: os, pandas, openpyxl

5. api Module
    - Purpose: Define REST API endpoints for frontend-backend communication.
    - Endpoints:
        - POST /upload-pdfs
            - Input: One or more CBP error report PDFs.
            - Output: Status message indicating success or failure.
        - POST /upload-import
            - Input: The import record Excel file.
            - Output: Status message indicating success or failure.
        - POST /process-data
            - Input: Triggers the matching logic between parsed errors and import records.
            - Output: Status message and a downloadable link to the processed Excel file.
        - GET /download
            - Input: Request for the processed file.
            - Output: Serves the processed Excel file for download.
    - Dependencies: Flask, uvicorn

Data Flow
1. PDF Upload and Parsing:
    - The user uploads one or more PDFs via the /upload-pdfs endpoint.
    - The pdf_parser module processes each file and extracts error data into a DataFrame.

2. Import Record Upload:
    - The user uploads an import record Excel file via the /upload-import endpoint.
    - The excel_parser module reads and validates the file, converting it into a DataFrame.

3. Matching Logic:
    - When the user triggers the /process-data endpoint, the backend:
        - Matches the parsed error data with the import record data using the matcher module.
        - Generates a final DataFrame containing the matched records.

4. Output File Generation:
    - The file_handler module saves the final DataFrame as an Excel file.
    - The /download endpoint serves the file to the user.

Endpoints
- POST /upload-pdfs: Accepts one or more CBP error report PDFs and parses them.
- POST /upload-import: Accepts the import record Excel file and validates it.
- POST /process-data: Matches error data with import records and generates the output file.
- GET /download: Provides a link to download the processed Excel file.

Additional Notes
- Error Handling: 
    - Ensure that descriptive errors are returned for:
        - Malformed or unsupported PDFs.
        - Missing required columns in the import record file.
        - No matching records found during processing.
    - Return errors as JSON objects with appropriate HTTP status codes (e.g., 400 for validation errors, 500 for internal errors).

- Performance: 
    - Since this is a single-user tool, prioritize accuracy and simplicity over performance optimizations.

- Testing: 
    - Unit tests: 
        - Test PDF parsing for edge cases (e.g., malformed data, unexpected formats). 
        - Test Excel file validation and matching logic. 
    - Integration tests: 
        - Test end-to-end functionality of all API endpoints.

Example Workflow
1. User uploads 2 CBP error PDFs via /upload-pdfs.
    - Backend saves files, parses them, and returns a success message.

2. User uploads 1 import record Excel file via /upload-import.
    - Backend saves and validates the file, returning a success message.

3. User triggers /process-data.
    - Backend matches the error data to import records, saves the final Excel, and provides a success message with a download link.

4. User accesses /download to retrieve the final processed Excel file.
