"""
English question generation module.
"""
import logging
from typing import List, Optional
from pdf_processor import extract_clean_text_chunks_from_pdf
from question_generator import generate_questions_from_prompt_with_rag as core_generate_questions_from_prompt_with_rag

logger = logging.getLogger(__name__)

class EnglishQuestionGenerator:
    """Handles English question generation."""
    
    def __init__(self):
        """Initialize the English question generator."""
        logger.info("Initialized English question generator")
    
    def generate_questions_from_pdf(
        self,
        pdf_path: str,
        prompt: str,
        total_questions: int = 20,
        top_n_chunks: int = 5,
        questions_per_chunk: int = 2
    ) -> List[str]:
        """
        Generate English questions from a PDF file.
        
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
            logger.info(f"Generating English questions from PDF: {pdf_path}")
            
            # Extract text chunks from PDF
            text_chunks = extract_clean_text_chunks_from_pdf(pdf_path)
            
            if not text_chunks:
                logger.warning("No text chunks extracted from PDF")
                return []
            
            # Generate questions using RAG
            questions = core_generate_questions_from_prompt_with_rag(
                prompt=prompt,
                text_chunks=text_chunks,
                total_questions=total_questions,
                top_n_chunks=top_n_chunks,
                questions_per_chunk=questions_per_chunk
            )
            
            logger.info(f"Generated {len(questions)} English questions")
            return questions
            
        except Exception as e:
            logger.error(f"Error generating English questions: {str(e)}")
            return []

# Global instance for backward compatibility
english_generator = EnglishQuestionGenerator()

# Legacy function for backward compatibility
def generate_questions_from_prompt_with_rag(
    prompt: str,
    text_chunks: List[str],
    total_questions: int = 20,
    top_n_chunks: int = 5,
    questions_per_chunk: int = 2
) -> List[str]:
    """
    Generate questions from prompt with RAG (legacy function).
    
    Args:
        prompt: User prompt
        text_chunks: Text chunks from PDF
        total_questions: Total questions to generate
        top_n_chunks: Top chunks to use
        questions_per_chunk: Questions per chunk
        
    Returns:
        List[str]: Generated questions
    """
    return core_generate_questions_from_prompt_with_rag(
        prompt=prompt,
        text_chunks=text_chunks,
        total_questions=total_questions,
        top_n_chunks=top_n_chunks,
        questions_per_chunk=questions_per_chunk
    )