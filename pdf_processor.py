"""
PDF processing utilities for extracting and cleaning text from PDF files.
"""
import logging
from typing import List, Optional
import pdfplumber
import fitz  # PyMuPDF
from utils import clean_text, split_text_into_chunks
from config import Config

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF text extraction and processing."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.chunk_size = Config.CHUNK_SIZE
    
    def extract_text_with_pdfplumber(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using pdfplumber library.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Optional[str]: Extracted text or None if extraction failed
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return clean_text(text) if text else None
            
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber from {pdf_path}: {str(e)}")
            return None
    
    def extract_text_with_pymupdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using PyMuPDF library.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Optional[str]: Extracted text or None if extraction failed
        """
        try:
            text = ""
            with fitz.open(pdf_path) as pdf:
                for page in pdf:
                    page_text = page.get_text()
                    if page_text:
                        text += page_text + "\n"
            
            return clean_text(text) if text else None
            
        except Exception as e:
            logger.error(f"Error extracting text with PyMuPDF from {pdf_path}: {str(e)}")
            return None
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using the best available method.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Optional[str]: Extracted text or None if extraction failed
        """
        # Try pdfplumber first
        text = self.extract_text_with_pdfplumber(pdf_path)
        
        # If pdfplumber fails, try PyMuPDF
        if not text:
            text = self.extract_text_with_pymupdf(pdf_path)
        
        if text:
            logger.info(f"Successfully extracted text from {pdf_path}")
        else:
            logger.error(f"Failed to extract text from {pdf_path}")
        
        return text
    
    def extract_text_chunks(self, pdf_path: str, chunk_size: int = None) -> List[str]:
        """
        Extract text from PDF and split into chunks.
        
        Args:
            pdf_path: Path to the PDF file
            chunk_size: Size of each chunk (defaults to Config.CHUNK_SIZE)
            
        Returns:
            List[str]: List of text chunks
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        
        text = self.extract_text(pdf_path)
        if not text:
            return []
        
        chunks = split_text_into_chunks(text, chunk_size)
        logger.info(f"Extracted {len(chunks)} text chunks from {pdf_path}")
        
        return chunks
    
    def extract_clean_text_chunks_from_pdf(self, pdf_path: str, chunk_size: int = None) -> List[str]:
        """
        Legacy method for backward compatibility.
        
        Args:
            pdf_path: Path to the PDF file
            chunk_size: Size of each chunk
            
        Returns:
            List[str]: List of text chunks
        """
        return self.extract_text_chunks(pdf_path, chunk_size)

# Global instance for backward compatibility
pdf_processor = PDFProcessor()

# Legacy function for backward compatibility
def extract_clean_text_chunks_from_pdf(pdf_path: str, chunk_size: int = None) -> List[str]:
    """
    Extract and clean text chunks from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        chunk_size: Size of each chunk
        
    Returns:
        List[str]: List of cleaned text chunks
    """
    return pdf_processor.extract_text_chunks(pdf_path, chunk_size) 