"""
Sanskrit question generation module.
"""
import logging
import re
from typing import List, Optional
from googletrans import Translator
from tqdm import tqdm

from pdf_processor import extract_clean_text_chunks_from_pdf
from question_generator import QuestionGenerator
from utils import clean_text, sanitize_question, remove_duplicates_preserve_order
from config import Config

logger = logging.getLogger(__name__)

class SanskritQuestionGenerator:
    """Handles Sanskrit question generation using translation approach."""
    
    def __init__(self):
        """Initialize the Sanskrit question generator."""
        try:
            self.translator = Translator()
            self.question_generator = QuestionGenerator()
            logger.info("Initialized Sanskrit question generator")
        except Exception as e:
            logger.error(f"Failed to initialize Sanskrit question generator: {str(e)}")
            raise
    
    def safe_translate(self, text: str, src: str, dest: str) -> Optional[str]:
        """
        Safely translate text with error handling.
        
        Args:
            text: Text to translate
            src: Source language code
            dest: Destination language code
            
        Returns:
            Optional[str]: Translated text or None if translation failed
        """
        if not text or not text.strip():
            return None
        
        try:
            result = self.translator.translate(text, src=src, dest=dest)
            return result.text if result and result.text else None
        except Exception as e:
            logger.warning(f"Translation failed for text: {text[:50]}... Error: {str(e)}")
            return None
    
    def retrieve_relevant_chunks(self, prompt: str, text_chunks: List[str], top_n: int = 5) -> List[str]:
        """
        Retrieve relevant chunks using TF-IDF (inherited from base class).
        
        Args:
            prompt: Search prompt
            text_chunks: Text chunks to search
            top_n: Number of top chunks
            
        Returns:
            List[str]: Relevant chunks
        """
        return self.question_generator.retrieve_relevant_chunks(prompt, text_chunks, top_n)
    
    def generate_questions_from_prompt_with_rag(
        self,
        prompt: str,
        text_chunks: List[str],
        total_questions: int = 10,
        top_n_chunks: int = 5,
        questions_per_chunk: int = 3
    ) -> List[str]:
        """
        Generate Sanskrit questions using RAG with translation.
        
        Args:
            prompt: User prompt to guide question generation
            text_chunks: List of text chunks from PDF
            total_questions: Total number of questions to generate
            top_n_chunks: Number of top chunks to use
            questions_per_chunk: Number of questions per chunk
            
        Returns:
            List[str]: List of generated questions in Sanskrit
        """
        try:
            logger.info("Generating Sanskrit questions using RAG with translation")
            
            # Translate Sanskrit prompt to English
            translated_prompt = self.safe_translate(prompt, src='sa', dest='en')
            if not translated_prompt:
                logger.warning("Failed to translate prompt to English")
                return []
            
            # Retrieve relevant chunks
            relevant_chunks = self.retrieve_relevant_chunks(
                translated_prompt, 
                text_chunks, 
                top_n=top_n_chunks
            )
            
            if not relevant_chunks:
                logger.warning("No relevant chunks found")
                return []
            
            # Generate questions from each relevant chunk
            all_generated_questions = []
            
            for chunk in tqdm(relevant_chunks, desc="Generating Sanskrit questions"):
                # Translate Sanskrit chunk to English
                translated_chunk = self.safe_translate(chunk, src='sa', dest='en')
                if not translated_chunk:
                    continue
                
                # Generate questions in English
                english_questions = self.question_generator.generate_questions_from_text(
                    translated_chunk, 
                    num_questions=questions_per_chunk
                )
                
                # Translate questions back to Sanskrit
                for question in english_questions:
                    sanskrit_question = self.safe_translate(question, src='en', dest='sa')
                    if sanskrit_question:
                        sanitized = sanitize_question(sanskrit_question, min_length=10)
                        if sanitized:
                            all_generated_questions.append(sanitized)
                
                # Stop if we have enough questions
                if len(all_generated_questions) >= total_questions:
                    break
            
            # Remove duplicates and limit to requested number
            unique_questions = remove_duplicates_preserve_order(all_generated_questions)
            final_questions = unique_questions[:total_questions]
            
            logger.info(f"Generated {len(final_questions)} Sanskrit questions")
            return final_questions
            
        except Exception as e:
            logger.error(f"Error generating Sanskrit questions: {str(e)}")
            return []
    
    def generate_questions_from_pdf(
        self,
        pdf_path: str,
        prompt: str,
        total_questions: int = 10,
        top_n_chunks: int = 5,
        questions_per_chunk: int = 3
    ) -> List[str]:
        """
        Generate Sanskrit questions from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            prompt: User prompt to guide question generation
            total_questions: Total number of questions to generate
            top_n_chunks: Number of top chunks to use
            questions_per_chunk: Number of questions per chunk
            
        Returns:
            List[str]: List of generated questions
        """
        try:
            logger.info(f"Generating Sanskrit questions from PDF: {pdf_path}")
            
            # Extract text chunks from PDF
            text_chunks = extract_clean_text_chunks_from_pdf(pdf_path)
            
            if not text_chunks:
                logger.warning("No text chunks extracted from PDF")
                return []
            
            # Generate questions using RAG with translation
            questions = self.generate_questions_from_prompt_with_rag(
                prompt=prompt,
                text_chunks=text_chunks,
                total_questions=total_questions,
                top_n_chunks=top_n_chunks,
                questions_per_chunk=questions_per_chunk
            )
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating Sanskrit questions from PDF: {str(e)}")
            return []

# Global instance for backward compatibility
sanskrit_generator = SanskritQuestionGenerator()

# Legacy functions for backward compatibility
def generate_questions_from_prompt_with_rag(
    prompt: str,
    text_chunks: List[str],
    total_questions: int = 10,
    top_n_chunks: int = 5,
    questions_per_chunk: int = 3
) -> List[str]:
    """
    Generate questions using RAG (legacy function).
    
    Args:
        prompt: User prompt
        text_chunks: Text chunks from PDF
        total_questions: Total questions to generate
        top_n_chunks: Top chunks to use
        questions_per_chunk: Questions per chunk
        
    Returns:
        List[str]: Generated questions
    """
    return sanskrit_generator.generate_questions_from_prompt_with_rag(
        prompt, text_chunks, total_questions, top_n_chunks, questions_per_chunk
    ) 