Product Requirements Document (PRD)

Problem Description
The application solves the following problems:
-  Parsing CBP Error Report PDFs: Automatically extract key information from CBP error reports, including error codes, filer codes, entry numbers, and 7501 line numbers.
- Converting PDF Data to Excel: Structure the parsed error data into a well-organized Excel format for further analysis.
- Matching Error Records with Import Records: Compare parsed error data against an import record Excel file to isolate relevant entries causing issues.
- Aggregating and Generating Output: Generate an output file containing matched import records alongside the associated error information for further analysis and resolution.

User Stories
- As a drawback specialist, I need to upload multiple CBP error files and an import record file so that I can automatically isolate problematic entries and resolve errors efficiently.
- As a drawback specialist, I want the application to aggregate all problematic entries in one place so I can identify patterns in the errors and improve our processes.
- As a drawback specialist, I need the final output to include both the error details and the matched import record data so I can easily see all the necessary information in one view.

Acceptance Criteria
Parsing PDFs:
- The application must extract the following fields from the CBP error report PDF:
    - Error description (e.g., "EXCESS DUTY CLAIMED").
    - Filer code and entry number (e.g., "GU660061040").
    - 7501 line number (e.g., "25").
- The parser should correctly handle the error formats and patterns found in CBP error reports, such as:
    - E1 F551 [EXCESS DUTY CLAIMED] [GU660061040] [25] GU6 88888838
- If the PDF is malformed or contains unexpected formats, the application must return a descriptive error message.

Excel Conversion
- The parsed data must be converted into an Excel file with the following columns:
    - Error Description
    - Error Description
    - Filer Code (first 3 digits of the filer + entry number field)
    - Entry Number (remaining digits of the filer + entry number field)
    - 7501 Line Number
- The Excel file should be well-formatted and easy to read.

Matching Logic
- The application must compare the parsed error data against the import record Excel file using the following critical matching criteria (in order):
    - Filer Code
    - Entry Number
    - 7501 Line Number
- Only matching records should be returned in the output. If no matches are found, a descriptive error message should be generated.

Output Requirements
- The output file must:
    - Include matched import records with the error details appended as a preceding row.
    - Be formatted as a new Excel file.
    - The output should provide only the relevant matched records, removing unmatched data.

Performance Expectations
- The application should prioritize accuracy over speed.
- Processing time for 100 error records and a large import record file (tens of thousands of entries) is not a primary concern, but it should remain reasonable.

Edge Cases
- For malformed PDFs or incomplete import record Excel files, return a clear descriptive error message (e.g., "PDF format not supported" or "Missing critical column in import file").
- If no matches are found, return a descriptive error message such as "No matching records found in the import base."

Scope Exclusions
- The application will not handle modifications to the import record file or the creation of new import records.
- It will not attempt to predict or resolve errors beyond isolating relevant records.
