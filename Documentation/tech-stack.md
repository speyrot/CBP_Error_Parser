Tech Stack Doc
Frontend
- Framework: React.js
    - Purpose: Provide a simple user interface for uploading files and downloading results.
    - Key Features: Drag-and-drop file upload, a minimal status/progress tracker, and a button for downloading the final Excel file.
- Styling:
    - Bootstrap: Keep styling simple and lightweight.
- Frontend Libraries:
    - Axios: For making API requests to the backend.
    - React Dropzone: For handling file uploads via drag-and-drop.
- Build Tool:
    - Create React App: A quick and straightforward way to set up the React app.

Backend
- Programming Language: Python 3.9+
    - Purpose: Handle PDF parsing, Excel processing, and matching logic.
- Framework: Flask
    - Advantages: Easy to set up and maintain for small projects.
- Key Python Libraries:
    - PDF Parsing: pdfplumber: For extracting structured text from CBP error report PDFs.
    - Data Manipulation: pandas: For processing and manipulating error data and import records.
    - Excel Handling: openpyxl: For reading and writing Excel files.
    - Validation: pydantic (optional): For simple input validation.

Deployment
- Frontend Deployment:
    - Netlify: Quick and easy deployment of the React frontend.
- Backend Deployment:
    - Local Execution: Run the Flask server locally on the user's machine.

Dependencies
- Frontend:
    - react
    - react-dom
    - react-dropzone
    - axios
    - bootstrap (if used)
- Backend:
    - flask
    - pdfplumber
    - pandas
    - openpyxl

System Requirements
- Frontend:
    - Node.js (LTS version): For building and running the React app.
    - npm or yarn: For managing dependencies.
- Backend:
    - Python 3.9+.
    - pip: For installing Python packages.

Simplified Flow
1. The frontend React app handles file uploads and sends the files to the Flask backend via REST API.

2. The Flask backend processes the files:
- Parses the PDF to extract error data.
- Matches error data with the import records.
- Returns a final Excel file with the results.

3. The user downloads the processed Excel file from the frontend.
