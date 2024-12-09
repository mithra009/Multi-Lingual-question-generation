# -*- coding: utf-8 -*-
"""Hindi_final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qKrMcCAp9sC1WBODvrZdtdKVSYm2u1c0
"""

!pip install pdfplumber
!pip install googletrans==4.0.0-rc1
!pip install pymupdf
import pandas as pd
from transformers import pipeline
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz
from tqdm import tqdm
from googletrans import Translator
import warnings
warnings.filterwarnings("ignore")

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            page_text = page.get_text()
            clean_text = page_text
            text += clean_text + "\n"
    return text

# Function to split text into manageable chunks
def split_text(text, max_length=1000):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Function to generate questions from Hindi sentences
def generate_question(sentence):
    location_rule = re.search(r'(.+?) (में|से|पर) (.+?) है।', sentence)
    if location_rule:
        location = location_rule.group(1)
        location_without_last_word = ' '.join(location.split()[:-1])
        return f"{location_without_last_word} कहाँ {location_rule.group(3)} है?"

    who_rule = re.search(r'(.+?) ने (.+?)।', sentence)
    if who_rule:
        return f"किसने {who_rule.group(2)}?"

    ki_rule = re.search(r'(.+?) की (.+?)।', sentence)
    if ki_rule:
        location = ki_rule.group(1)
        location_without_last_word = ' '.join(location.split()[:-1])
        return f"{location_without_last_word} किसकी {ki_rule.group(2)}?"

    return "Question generation rule not found."

# Function to process sentences and generate questions
def process_book(sentences):
    data = []

    for sentence in tqdm(sentences, desc="Generating Questions"):
        question = generate_question(sentence)
        if question:
            data.append({'Sentence': sentence, 'Question': question})

    df = pd.DataFrame(data, columns=['Sentence', 'Question'])
    return df

# Main function to process PDF and generate questions
def generate_questions_from_hindi_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    sentences = re.split(r'(?<=।)\s+', text)
    df = process_book(sentences)
    answers = df[df.Question != "Question generation rule not found."]
    questions = answers['Question'].tolist()
    return questions
