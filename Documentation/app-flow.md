App Flow Doc

1. User Journey
- Upload CBP Error Report PDFs
    - The user uploads one or more PDF files containing CBP error data.
    - If the PDF format is unsupported or malformed, the system returns a descriptive error message.

2. Parse PDFs to Extract Error Information
    - The application parses each uploaded PDF and extracts the following fields from the error reports:
        - Error Description (e.g., "EXCESS DUTY CLAIMED")
        - Filer Code (first 3 digits of the filer + entry number field)
        - Entry Number (remaining digits of the filer + entry number field)
        - 7501 Line Number
    - If parsing fails due to unexpected formats or incomplete data, the system provides a clear error message.

3. Convert Parsed Data to an Excel File
    - The extracted data is organized into an Excel file with the following columns:
        - Error Description
        - Filer Code
        - Entry Number
        - 7501 Line Number
    - The Excel file is saved in a designated output location or returned to memory for further processing.

4. Upload Import Record Excel File
    - The user uploads an Excel file containing the import records.
    - The system validates the file to ensure it contains the required columns (e.g., Filer Code, Entry Number, 7501 Line Number).
    - If the file is invalid or missing required columns, the system returns a descriptive error message.

5. Filter for Entries Matching the Errors
    - The application compares the parsed error data against the import records using the following matching criteria:
        1. Filer Code
        2. Entry Number
        3. 7501 Line Number
    - The application isolates matching import records and appends the corresponding error details.

6. Output Final Filtered List
    - The final output is an Excel file that includes:
        - Matched import records
        - Preceding rows containing the associated error details
    - If no matches are found, the system generates a descriptive error message (e.g., "No matching records found in the import base").
    - The user can download the output Excel file for further analysis.