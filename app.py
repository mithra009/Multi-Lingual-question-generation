"""
Multi-Lingual Question Generation Flask Application.
"""
import os
import logging
from typing import Optional, List
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.exceptions import RequestEntityTooLarge

from config import config
from utils import secure_file_upload, validate_language
from languages.english import EnglishQuestionGenerator
from languages.hindi import HindiQuestionGenerator
from languages.sanskrit import SanskritQuestionGenerator

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.getenv('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# Set up logging
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format=app.config['LOG_FORMAT']
)
logger = logging.getLogger(__name__)

# Initialize language generators
language_generators = {
    'english': EnglishQuestionGenerator(),
    'hindi': HindiQuestionGenerator(),
    'sanskrit': SanskritQuestionGenerator()
}

@app.route('/')
def index():
    """Render the main page for language selection."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return "Internal server error", 500

@app.route('/upload', methods=['POST'])
def upload():
    """Handle language selection and redirect to upload page."""
    try:
        language = request.form.get('language', '').lower()
        
        if not validate_language(language):
            flash('Invalid language selected.', 'error')
            return redirect(url_for('index'))
        
        session['language'] = language
        logger.info(f"Language selected: {language}")
        
        return render_template('upload.html', language=language)
        
    except Exception as e:
        logger.error(f"Error in upload route: {str(e)}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/process', methods=['POST'])
def process():
    """Process PDF upload and generate questions."""
    try:
        # Get form data
        prompt = request.form.get('prompt', '').strip()
        language = session.get('language', '').lower()
        total_questions = int(request.form.get('total_questions', 15))
        
        # Validate inputs
        if not prompt:
            flash('Please provide a prompt for question generation.', 'error')
            return redirect(url_for('index'))
        
        if not validate_language(language):
            flash('Invalid language selected.', 'error')
            return redirect(url_for('index'))
        
        # Handle file upload
        if 'file' not in request.files:
            flash('No file uploaded.', 'error')
            return redirect(url_for('index'))
        
        pdf_file = request.files['file']
        if not pdf_file or pdf_file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('index'))
        
        # Secure file upload
        file_path = secure_file_upload(pdf_file)
        if not file_path:
            flash('Invalid file type. Please upload a PDF file.', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Processing PDF: {file_path} for language: {language}")
        
        # Generate questions based on language
        questions = generate_questions_for_language(
            language, file_path, prompt, total_questions
        )
        
        if not questions:
            flash('No questions could be generated. Please try with different content or settings.', 'warning')
            return redirect(url_for('index'))
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
            logger.info(f"Cleaned up uploaded file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up file {file_path}: {str(e)}")
        
        logger.info(f"Generated {len(questions)} questions for {language}")
        return render_template('result.html', questions=questions, language=language)
        
    except RequestEntityTooLarge:
        flash('File too large. Please upload a smaller PDF file.', 'error')
        return redirect(url_for('index'))
    except ValueError:
        flash('Invalid number of questions specified.', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        flash('An error occurred while processing your request. Please try again.', 'error')
        return redirect(url_for('index'))

def generate_questions_for_language(
    language: str, 
    pdf_path: str, 
    prompt: str, 
    total_questions: int
) -> List[str]:
    """
    Generate questions for a specific language.
    
    Args:
        language: Language to generate questions for
        pdf_path: Path to the PDF file
        prompt: User prompt for question generation
        total_questions: Number of questions to generate
        
    Returns:
        List[str]: Generated questions
    """
    try:
        generator = language_generators.get(language)
        if not generator:
            logger.error(f"No generator found for language: {language}")
            return []
        
        if language == 'english':
            return generator.generate_questions_from_pdf(
                pdf_path=pdf_path,
                prompt=prompt,
                total_questions=total_questions
            )
        elif language == 'hindi':
            return generator.generate_questions_from_pdf(
                pdf_path=pdf_path,
                prompt=prompt,
                total_questions=total_questions
            )
        elif language == 'sanskrit':
            return generator.generate_questions_from_pdf(
                pdf_path=pdf_path,
                prompt=prompt,
                total_questions=total_questions
            )
        else:
            logger.error(f"Unsupported language: {language}")
            return []
            
    except Exception as e:
        logger.error(f"Error generating questions for {language}: {str(e)}")
        return []

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('error.html', error_code=404, message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('error.html', error_code=500, message="Internal server error"), 500

@app.errorhandler(413)
def too_large_error(error):
    """Handle file too large errors."""
    flash('File too large. Please upload a smaller file.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    logger.info("Starting Multi-Lingual Question Generator application")
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG']
    )