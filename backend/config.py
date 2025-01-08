import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Upload directory for temporary file storage
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'pdf': {'pdf'},
    'excel': {'xlsx', 'xls'}
}

# Maximum file size (10 MB)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Create upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
