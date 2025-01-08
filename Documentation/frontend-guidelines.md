Frontend Guidelines

Purpose:
- Provide a simple, intuitive interface for the drawback specialist to:
    - Upload multiple CBP error PDFs.
    - Upload the import record Excel file.
    - View progress or status messages.
    - Download the final processed Excel file with the matched records.

Design Style:
- General Look and Feel:
    - Keep the design clean, minimalistic, and easy to use.
    - Use a neutral color palette with clear visual hierarchy (e.g., white/gray background, blue buttons, etc.).
    - Display clear instructions at each step for ease of use.
- Styling Framework:
    - Use Bootstrap for quick and consistent styling.
    - Keep all custom styles in a single styles.css file or modular CSS files.

Structure:
- The React app should have the following structure:

File Structure:
src/
├── components/
│   ├── FileUpload.js        // Handles file uploads (drag-and-drop or button-based)
│   ├── ProgressTracker.js   // Shows status updates during processing
│   ├── DownloadButton.js    // Allows user to download the processed file
│   └── Header.js            // Displays app title and brief instructions
├── pages/
│   └── Home.js              // Main page containing all components
├── services/
│   └── api.js               // Handles API calls to the backend
├── App.js                   // Combines all components
├── index.js                 // Entry point
├── styles.css               // Global styles

Page Layout:
- Header: Displays the app title and a brief description of the tool.
- Main Section: Includes:
    - A file upload area for PDFs and the Excel file.
    - A status/progress tracker.
    - A button to download the final processed file.
- Footer: Include a small "Powered by [Your Name/Company]" message (optional).

Components:
- FileUpload.js
    - Purpose: Allow the user to upload multiple PDF files and one Excel file.
    - Features:
        - Drag-and-drop support using react-dropzone.
        - Separate sections for PDFs and the Excel file to avoid confusion.
        - File validation (e.g., allow only .pdf for error files and .xlsx for import records).

- ProgressTracker.js
    - Purpose: Show status updates (e.g., "Parsing PDFs...", "Matching records...", "Process complete").
    - Features:
        - Simple text updates or a progress bar.
        - Fetch progress status from the backend (if needed).

- DownloadButton.js
    - Purpose: Provide a button for downloading the processed Excel file.
    - Features:
        - Disables the button until the backend processing is complete.
        - Downloads the file as a .xlsx format.

- Header.js
    - Purpose: Display the app title and a brief description.
    - Features:
        - Display the app title and a brief description.

Frontend Behavior
1. File Upload:
    - Provide drag-and-drop support for both PDFs and the Excel file.
    - Validate files to ensure only the correct formats (.pdf for error reports and .xlsx for import records) are accepted.

2. Progress Tracking:
    - Show clear status messages for each step (e.g., "Parsing PDFs", "Processing Import Records").
    - Optionally, display an animated progress bar for visual feedback.

3. Error Handling:
    - Display descriptive error messages if:
        - Invalid file formats are uploaded.
        - Backend processing fails.
    - Ensure errors are user-friendly and actionable.

4. File Download:
    - Provide a clear button for downloading the processed Excel file once the backend has completed processing.
    - Ensure the download is initiated immediately upon clicking.

Testing
- Test the following scenarios:
    - Drag-and-drop functionality for PDFs and Excel files.
    - Validation of file formats.
    - Smooth progress tracking for multiple files.
    - Correct downloading of the processed Excel file.
    - Error messages for invalid uploads or failed backend responses.
