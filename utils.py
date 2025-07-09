"""
Utility functions for the Multi-Lingual Question Generation application.
"""
import os
import re
import logging
from typing import List, Optional, Set
from werkzeug.utils import secure_filename
from config import Config

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def secure_file_upload(file) -> Optional[str]:
    """
    Securely handle file upload and return the saved file path.
    
    Args:
        file: The uploaded file object
        
    Returns:
        Optional[str]: Path to the saved file, or None if upload failed
    """
    try:
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            # Ensure upload directory exists
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            file.save(file_path)
            logger.info(f"File uploaded successfully: {filename}")
            return file_path
        else:
            logger.warning("Invalid file upload attempt")
            return None
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        return None

def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing unwanted patterns and extra whitespace.
    
    Args:
        text: Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove URLs and file paths
    text = re.sub(r'http\S+|www\S+|file:\S+|\S+\.html', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
    
    return text.strip()

def split_text_into_chunks(text: str, chunk_size: int = None) -> List[str]:
    """
    Split text into chunks of specified size.
    
    Args:
        text: Text to split
        chunk_size: Size of each chunk (defaults to Config.CHUNK_SIZE)
        
    Returns:
        List[str]: List of text chunks
    """
    if chunk_size is None:
        chunk_size = Config.CHUNK_SIZE
    
    if not text:
        return []
    
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk.strip())
    
    return chunks

def validate_language(language: str) -> bool:
    """
    Validate if the provided language is supported.
    
    Args:
        language: Language to validate
        
    Returns:
        bool: True if language is supported, False otherwise
    """
    return language.lower() in Config.SUPPORTED_LANGUAGES

def get_language_code(language: str) -> Optional[str]:
    """
    Get the language code for a given language name.
    
    Args:
        language: Language name
        
    Returns:
        Optional[str]: Language code or None if not supported
    """
    return Config.SUPPORTED_LANGUAGES.get(language.lower())

def remove_duplicates_preserve_order(items: List[str]) -> List[str]:
    """
    Remove duplicates from a list while preserving order.
    
    Args:
        items: List of items to deduplicate
        
    Returns:
        List[str]: List with duplicates removed
    """
    seen: Set[str] = set()
    result = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

def sanitize_question(question: str, min_length: int = 15) -> Optional[str]:
    """
    Sanitize and validate a generated question.
    
    Args:
        question: Raw question text
        min_length: Minimum acceptable length for a question
        
    Returns:
        Optional[str]: Sanitized question or None if invalid
    """
    if not question:
        return None
    
    # Clean the question
    cleaned = clean_text(question)
    
    # Check minimum length
    if len(cleaned) < min_length:
        return None
    
    # Remove questions that are too generic
    generic_patterns = [
        r'^what is$',
        r'^who is$',
        r'^where is$',
        r'^when is$',
        r'^how is$'
    ]
    
    for pattern in generic_patterns:
        if re.match(pattern, cleaned.lower()):
            return None
    
    return cleaned 