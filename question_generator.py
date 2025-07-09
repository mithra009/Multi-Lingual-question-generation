"""
Question generation utilities using transformer models.
"""
import logging
from typing import List, Optional, Dict, Any
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from tqdm import tqdm

from utils import clean_text, remove_duplicates_preserve_order, sanitize_question
from config import Config

logger = logging.getLogger(__name__)

class QuestionGenerator:
    """Handles question generation using transformer models."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the question generator.
        
        Args:
            model_name: Name of the transformer model to use
        """
        if model_name is None:
            model_name = Config.QUESTION_GENERATOR_MODEL
        
        try:
            # Try to load the model with error handling
            self.question_generator = pipeline(
                "text2text-generation", 
                model=model_name,
                device=-1  # Force CPU usage
            )
            logger.info(f"Question generator initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize question generator with {model_name}: {str(e)}")
            # Fallback to a simpler model if the main one fails
            try:
                logger.info("Attempting to use fallback model...")
                self.question_generator = pipeline(
                    "text2text-generation", 
                    model="google/flan-t5-base",
                    device=-1  # Force CPU usage
                )
                logger.info("Successfully initialized with fallback model: google/flan-t5-base")
            except Exception as fallback_error:
                logger.error(f"Fallback model also failed: {str(fallback_error)}")
                raise RuntimeError("Could not initialize any question generation model")
    
    def generate_questions_from_text(
        self, 
        text: str, 
        num_questions: int = None,
        max_length: int = 100,
        num_beams: int = 5
    ) -> List[str]:
        """
        Generate questions from a given text.
        
        Args:
            text: Input text to generate questions from
            num_questions: Number of questions to generate
            max_length: Maximum length of generated questions
            num_beams: Number of beams for beam search
            
        Returns:
            List[str]: List of generated questions
        """
        if num_questions is None:
            num_questions = Config.MAX_QUESTIONS_PER_CHUNK
        
        if not text or not text.strip():
            logger.warning("Empty text provided for question generation")
            return []
        
        try:
            # Use a more generic prompt for better compatibility
            formatted_text = f"Generate a question about: {text}"
            questions = self.question_generator(
                formatted_text, 
                max_length=max_length, 
                num_beams=num_beams, 
                num_return_sequences=num_questions,
                do_sample=True,
                temperature=0.7
            )
            
            # Extract and clean questions
            generated_questions = []
            for q in questions:
                question_text = q.get('generated_text', '')
                if question_text:
                    sanitized = sanitize_question(question_text)
                    if sanitized:
                        generated_questions.append(sanitized)
            
            # Remove duplicates while preserving order
            unique_questions = remove_duplicates_preserve_order(generated_questions)
            
            logger.info(f"Generated {len(unique_questions)} questions from text")
            return unique_questions
            
        except Exception as e:
            logger.error(f"Error generating questions from text: {str(e)}")
            return []
    
    def retrieve_relevant_chunks(
        self, 
        prompt: str, 
        text_chunks: List[str], 
        top_n: int = None
    ) -> List[str]:
        """
        Retrieve the most relevant text chunks based on a prompt using TF-IDF.
        
        Args:
            prompt: The search prompt
            text_chunks: List of text chunks to search through
            top_n: Number of top chunks to return
            
        Returns:
            List[str]: List of relevant text chunks
        """
        if top_n is None:
            top_n = Config.DEFAULT_TOP_N_CHUNKS
        
        if not text_chunks:
            logger.warning("No text chunks provided for retrieval")
            return []
        
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt provided for chunk retrieval")
            return text_chunks[:top_n]
        
        try:
            # Prepare documents for TF-IDF
            documents = [prompt] + text_chunks
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(documents)
            
            # Calculate cosine similarities
            cosine_similarities = cosine_similarity(
                tfidf_matrix[0:1], 
                tfidf_matrix[1:]
            ).flatten()
            
            # Get top N most similar chunks
            top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]
            relevant_chunks = [text_chunks[i] for i in top_n_indices]
            
            logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks")
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving relevant chunks: {str(e)}")
            return text_chunks[:top_n]
    
    def generate_questions_from_prompt_with_rag(
        self,
        prompt: str,
        text_chunks: List[str],
        total_questions: int = None,
        top_n_chunks: int = None,
        questions_per_chunk: int = None
    ) -> List[str]:
        """
        Generate questions using RAG (Retrieval-Augmented Generation) approach.
        
        Args:
            prompt: User prompt to guide question generation
            text_chunks: List of text chunks from PDF
            total_questions: Total number of questions to generate
            top_n_chunks: Number of top chunks to use
            questions_per_chunk: Number of questions per chunk
            
        Returns:
            List[str]: List of generated questions
        """
        if total_questions is None:
            total_questions = Config.DEFAULT_TOTAL_QUESTIONS
        if top_n_chunks is None:
            top_n_chunks = Config.DEFAULT_TOP_N_CHUNKS
        if questions_per_chunk is None:
            questions_per_chunk = Config.MAX_QUESTIONS_PER_CHUNK
        
        if not text_chunks:
            logger.warning("No text chunks provided for question generation")
            return []
        
        try:
            # Retrieve relevant chunks
            relevant_chunks = self.retrieve_relevant_chunks(
                prompt, 
                text_chunks, 
                top_n=top_n_chunks
            )
            
            if not relevant_chunks:
                logger.warning("No relevant chunks found")
                return []
            
            # Generate questions from each relevant chunk
            all_generated_questions = []
            
            for chunk in tqdm(relevant_chunks, desc="Generating questions"):
                chunk_questions = self.generate_questions_from_text(
                    chunk, 
                    num_questions=questions_per_chunk
                )
                all_generated_questions.extend(chunk_questions)
                
                # Stop if we have enough questions
                if len(all_generated_questions) >= total_questions:
                    break
            
            # Remove duplicates and limit to requested number
            unique_questions = remove_duplicates_preserve_order(all_generated_questions)
            final_questions = unique_questions[:total_questions]
            
            logger.info(f"Generated {len(final_questions)} questions using RAG")
            return final_questions
            
        except Exception as e:
            logger.error(f"Error in RAG question generation: {str(e)}")
            return []

# Global instance for backward compatibility
question_generator = QuestionGenerator()

# Legacy functions for backward compatibility
def generate_questions(text: str, num_questions: int = 15) -> List[str]:
    """
    Generate questions from text (legacy function).
    
    Args:
        text: Input text
        num_questions: Number of questions to generate
        
    Returns:
        List[str]: Generated questions
    """
    return question_generator.generate_questions_from_text(text, num_questions)

def retrieve_relevant_chunks(prompt: str, text_chunks: List[str], top_n: int = 5) -> List[str]:
    """
    Retrieve relevant chunks (legacy function).
    
    Args:
        prompt: Search prompt
        text_chunks: Text chunks to search
        top_n: Number of top chunks
        
    Returns:
        List[str]: Relevant chunks
    """
    return question_generator.retrieve_relevant_chunks(prompt, text_chunks, top_n)

def generate_questions_from_prompt_with_rag(
    prompt: str,
    text_chunks: List[str],
    total_questions: int = 20,
    top_n_chunks: int = 5,
    questions_per_chunk: int = 2
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
    return question_generator.generate_questions_from_prompt_with_rag(
        prompt, text_chunks, total_questions, top_n_chunks, questions_per_chunk
    ) 