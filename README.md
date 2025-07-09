# Multi-Lingual Question Generator

A modern, AI-powered web application that generates insightful and relevant questions from textual content in various languages, including Sanskrit, Hindi, and English. This application processes user-uploaded PDF files and creates personalized quizzes based on user prompts using advanced natural language processing (NLP) techniques and transformer models.

## 🌟 Features

- **Multi-Language Support**: Generate questions from text in English, Hindi, and Sanskrit
- **PDF Processing**: Upload and process PDF files with advanced text extraction
- **AI-Powered Generation**: Uses state-of-the-art transformer models for high-quality questions
- **Custom Prompts**: Provide specific topics or keywords to guide question generation
- **Modern UI**: Beautiful, responsive web interface with drag-and-drop functionality
- **Export Options**: Download questions as text files, copy to clipboard, or print
- **Security**: Secure file uploads with validation and cleanup
- **Error Handling**: Comprehensive error handling and user feedback

## 🏗️ Architecture

The application follows industry-standard practices with a modular, maintainable architecture:

```
Multi-Lingual-question-generation/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── utils.py              # Utility functions
├── pdf_processor.py      # PDF text extraction
├── question_generator.py # Core question generation logic
├── languages/            # Language-specific modules
│   ├── __init__.py
│   ├── english.py        # English question generation
│   ├── hindi.py          # Hindi question generation
│   └── sanskrit.py       # Sanskrit question generation
├── templates/            # HTML templates
│   ├── index.html        # Language selection page
│   ├── upload.html       # File upload page
│   ├── result.html       # Results display page
│   └── error.html        # Error handling page
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or later
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the Repository**
   ```bash
git clone https://github.com/your-username/Multi-Lingual-question-generation.git
cd Multi-Lingual-question-generation
   ```

2. **Set Up Virtual Environment**
   ```bash
python -m venv venv
   
   # On Windows
venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
pip install -r requirements.txt
   ```

4. **Set Environment Variables** (Optional)
   ```bash
   # Create a .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "FLASK_ENV=development" >> .env
   echo "DEBUG=True" >> .env
   ```

5. **Run the Application**
   ```bash
python app.py
   ```

6. **Access the Application**
   Open your browser and navigate to `http://localhost:5000`

## 📖 Usage

### Step-by-Step Guide

1. **Select Language**: Choose from English, Hindi, or Sanskrit
2. **Upload PDF**: Drag and drop or browse for a PDF file
3. **Enter Prompt**: Provide a specific topic or keyword to guide generation
4. **Configure Settings**: Set number of questions and question type
5. **Generate**: Click "Generate Questions" to process your document
6. **Export**: Download, copy, or print your generated questions

### Supported Languages

- **English**: Uses advanced transformer models with RAG (Retrieval-Augmented Generation)
- **Hindi**: Rule-based question generation with pattern matching
- **Sanskrit**: Translation-assisted generation using Google Translate API

## ⚙️ Configuration

The application uses a flexible configuration system. Key settings can be modified in `config.py`:

```python
class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Model settings
    QUESTION_GENERATOR_MODEL = "valhalla/t5-small-qa-qg-hl"
    DEFAULT_TOTAL_QUESTIONS = 20
    DEFAULT_TOP_N_CHUNKS = 5
    CHUNK_SIZE = 1000
```

## 🔧 Development

### Project Structure

- **Modular Design**: Each language has its own module for easy maintenance
- **Type Hints**: Full type annotation for better code quality
- **Error Handling**: Comprehensive exception handling throughout
- **Logging**: Structured logging for debugging and monitoring
- **Testing**: Ready for unit and integration tests

### Adding New Languages

1. Create a new file in `languages/` directory
2. Implement the language-specific question generation logic
3. Add the language to the configuration
4. Update the language selection UI

### Code Quality

The project follows industry standards:
- **PEP 8**: Python style guide compliance
- **Type Hints**: Full type annotation
- **Docstrings**: Comprehensive documentation
- **Error Handling**: Robust exception management
- **Security**: Input validation and secure file handling

## 🛠️ Dependencies

### Core Dependencies
- **Flask**: Web framework
- **transformers**: Hugging Face transformer models
- **pdfplumber**: PDF text extraction
- **PyMuPDF**: Alternative PDF processing
- **scikit-learn**: Machine learning utilities
- **googletrans**: Translation services

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## 🔒 Security Features

- **File Validation**: Strict PDF file type checking
- **Secure Uploads**: Sanitized filenames and secure file handling
- **Input Validation**: Comprehensive input sanitization
- **Error Handling**: Secure error messages without information leakage
- **File Cleanup**: Automatic cleanup of uploaded files

## 🚀 Deployment

### Production Deployment

1. **Set Production Environment**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   export DEBUG=False
   ```

2. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set Up Reverse Proxy** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Write unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- Google Translate API for translation services
- Bootstrap for the modern UI framework
- The open-source community for various libraries and tools

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Note**: This application is designed for educational and research purposes. Please ensure you have the right to process any documents you upload.
