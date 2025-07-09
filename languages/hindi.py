"""
Hindi question generation module.
"""
import logging
import re
from typing import List, Optional
import pandas as pd
from tqdm import tqdm
import fitz  # PyMuPDF

from utils import clean_text, sanitize_question
from config import Config

logger = logging.getLogger(__name__)

class HindiQuestionGenerator:
    """Handles Hindi question generation using rule-based approach."""
    
    def __init__(self):
        """Initialize the Hindi question generator."""
        logger.info("Initialized Hindi question generator")
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF using PyMuPDF.
        
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
                        text += clean_text(page_text) + "\n"
            
            return text.strip() if text else None
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            return None
    
    def split_text_into_sentences(self, text: str) -> List[str]:
        """
        Split Hindi text into sentences.
        
        Args:
            text: Hindi text to split
            
        Returns:
            List[str]: List of sentences
        """
        if not text:
            return []
        
        # Split by Hindi sentence endings
        sentences = re.split(r'(?<=।)\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def generate_question_from_sentence(self, sentence: str) -> Optional[str]:
        """
        Generate a question from a Hindi sentence using rule-based patterns.
        
        Args:
            sentence: Hindi sentence to generate question from
            
        Returns:
            Optional[str]: Generated question or None if no pattern matches
        """
        if not sentence or not sentence.strip():
            return None
        
        # Pattern 1: Location-based questions (में/से/पर)
        location_match = re.search(r'(.+?) (में|से|पर) (.+?) है।', sentence)
        if location_match:
            location = location_match.group(1)
            location_words = location.split()
            if len(location_words) > 1:
                location_without_last = ' '.join(location_words[:-1])
                return f"{location_without_last} कहाँ {location_match.group(3)} है?"
        
        # Pattern 2: Who did something (ने)
        who_match = re.search(r'(.+?) ने (.+?)।', sentence)
        if who_match:
            return f"किसने {who_match.group(2)}?"
        
        # Pattern 3: Possession questions (की)
        possession_match = re.search(r'(.+?) की (.+?)।', sentence)
        if possession_match:
            location = possession_match.group(1)
            location_words = location.split()
            if len(location_words) > 1:
                location_without_last = ' '.join(location_words[:-1])
                return f"{location_without_last} किसकी {possession_match.group(2)}?"
        
        # Pattern 4: What is questions
        what_is_match = re.search(r'(.+?) एक (.+?) है।', sentence)
        if what_is_match:
            return f"{what_is_match.group(1)} क्या है?"
        
        # Pattern 5: When questions
        when_match = re.search(r'(.+?) में (.+?) हुआ।', sentence)
        if when_match:
            return f"{when_match.group(1)} कब हुआ?"
        
        return None
    
    def process_sentences(self, sentences: List[str]) -> List[str]:
        """
        Process sentences and generate questions.
        
        Args:
            sentences: List of Hindi sentences
            
        Returns:
            List[str]: List of generated questions
        """
        questions = []
        
        for sentence in tqdm(sentences, desc="Generating Hindi questions"):
            question = self.generate_question_from_sentence(sentence)
            if question:
                sanitized = sanitize_question(question, min_length=10)
                if sanitized:
                    questions.append(sanitized)
        
        return questions
    
    def generate_questions_from_pdf(
        self,
        pdf_path: str,
        prompt: str = "",
        total_questions: int = 20
    ) -> List[str]:
        """
        Generate Hindi questions from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            prompt: User prompt (not used in Hindi generation)
            total_questions: Total number of questions to generate
            
        Returns:
            List[str]: List of generated questions
        """
        try:
            logger.info(f"Generating Hindi questions from PDF: {pdf_path}")
            
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_path)
            if not text:
                logger.warning("No text extracted from PDF")
                return []
            
            # Split into sentences
            sentences = self.split_text_into_sentences(text)
            if not sentences:
                logger.warning("No sentences found in text")
                return []
            
            # Generate questions
            questions = self.process_sentences(sentences)
            
            # Limit to requested number
            final_questions = questions[:total_questions]
            
            logger.info(f"Generated {len(final_questions)} Hindi questions")
            return final_questions
            
        except Exception as e:
            logger.error(f"Error generating Hindi questions: {str(e)}")
            return []

# Global instance for backward compatibility
hindi_generator = HindiQuestionGenerator()

# Legacy function for backward compatibility
def process_hindi_pdf(prompt: str, pdf_path: str) -> List[str]:
    """
    Process Hindi PDF and generate questions (legacy function).
    
    Args:
        prompt: User prompt
        pdf_path: Path to PDF file
        
    Returns:
        List[str]: Generated questions
    """
    return hindi_generator.generate_questions_from_pdf(pdf_path, prompt) 