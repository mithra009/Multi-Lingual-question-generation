"""
Language-specific question generation modules.
"""

from .english import EnglishQuestionGenerator
from .hindi import HindiQuestionGenerator
from .sanskrit import SanskritQuestionGenerator

__all__ = [
    'EnglishQuestionGenerator',
    'HindiQuestionGenerator', 
    'SanskritQuestionGenerator'
] 