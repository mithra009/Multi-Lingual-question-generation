"""
Tests for utility functions.
"""
import pytest
from utils import (
    allowed_file, 
    clean_text, 
    validate_language, 
    get_language_code,
    remove_duplicates_preserve_order,
    sanitize_question
)


class TestFileValidation:
    """Test file validation functions."""
    
    def test_allowed_file_valid_pdf(self):
        """Test that valid PDF files are allowed."""
        assert allowed_file("document.pdf") is True
        assert allowed_file("test.PDF") is True
    
    def test_allowed_file_invalid_extensions(self):
        """Test that non-PDF files are rejected."""
        assert allowed_file("document.txt") is False
        assert allowed_file("image.jpg") is False
        assert allowed_file("script.py") is False
    
    def test_allowed_file_no_extension(self):
        """Test files without extensions."""
        assert allowed_file("document") is False


class TestTextProcessing:
    """Test text processing functions."""
    
    def test_clean_text_normal(self):
        """Test normal text cleaning."""
        text = "  Hello   world!  "
        result = clean_text(text)
        assert result == "Hello world!"
    
    def test_clean_text_with_urls(self):
        """Test text cleaning with URLs."""
        text = "Check this link: http://example.com and www.test.com"
        result = clean_text(text)
        assert "http://example.com" not in result
        assert "www.test.com" not in result
    
    def test_clean_text_empty(self):
        """Test cleaning empty text."""
        assert clean_text("") == ""
        assert clean_text(None) == ""


class TestLanguageValidation:
    """Test language validation functions."""
    
    def test_validate_language_valid(self):
        """Test valid language validation."""
        assert validate_language("english") is True
        assert validate_language("hindi") is True
        assert validate_language("sanskrit") is True
    
    def test_validate_language_invalid(self):
        """Test invalid language validation."""
        assert validate_language("french") is False
        assert validate_language("") is False
        assert validate_language("ENGLISH") is True  # Case insensitive
    
    def test_get_language_code(self):
        """Test language code retrieval."""
        assert get_language_code("english") == "en"
        assert get_language_code("hindi") == "hi"
        assert get_language_code("sanskrit") == "sa"
        assert get_language_code("french") is None


class TestQuestionSanitization:
    """Test question sanitization functions."""
    
    def test_sanitize_question_valid(self):
        """Test valid question sanitization."""
        question = "What is the capital of France?"
        result = sanitize_question(question)
        assert result == question
    
    def test_sanitize_question_too_short(self):
        """Test question that's too short."""
        question = "What?"
        result = sanitize_question(question, min_length=10)
        assert result is None
    
    def test_sanitize_question_generic(self):
        """Test generic questions are filtered out."""
        question = "what is"
        result = sanitize_question(question)
        assert result is None


class TestDuplicateRemoval:
    """Test duplicate removal functions."""
    
    def test_remove_duplicates_preserve_order(self):
        """Test duplicate removal while preserving order."""
        items = ["a", "b", "a", "c", "b", "d"]
        result = remove_duplicates_preserve_order(items)
        assert result == ["a", "b", "c", "d"]
    
    def test_remove_duplicates_no_duplicates(self):
        """Test list with no duplicates."""
        items = ["a", "b", "c"]
        result = remove_duplicates_preserve_order(items)
        assert result == items
    
    def test_remove_duplicates_empty(self):
        """Test empty list."""
        result = remove_duplicates_preserve_order([])
        assert result == [] 