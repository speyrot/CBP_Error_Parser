from flask import Flask
from flask_cors import CORS
import os
import logging
from routes.endpoints import api
from config import UPLOAD_FOLDER, MAX_CONTENT_LENGTH

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    
    # Configure upload folder and max content length
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.logger.info('Starting Flask server...')
    app.run(host='0.0.0.0', port=5001, debug=True) 