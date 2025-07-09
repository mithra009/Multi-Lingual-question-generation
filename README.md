#  Multi-Lingual Question Generator

A modern, AI-powered web application that generates insightful and relevant questions from textual content in various languages, including **Sanskrit, Hindi, and English**. This tool processes user-uploaded PDF files and creates personalized quizzes based on user prompts using advanced NLP techniques and transformer models.

---

##  Features

- **Multi-Language Support**: Generate questions from English, Hindi, and Sanskrit text
- **PDF Processing**: Upload and extract content from PDF files with high accuracy
- **AI-Powered Generation**: Utilizes transformer models for intelligent question generation
- **Custom Prompts**: Guide generation with specific topics or keywords
- **Modern UI**: Clean, responsive interface with drag-and-drop support
- **Export Options**: Download, copy to clipboard, or print generated questions
- **Security**: Secure file handling with upload validation and cleanup
- **Robust Error Handling**: Clear user feedback and exception handling

---

##  Architecture

```
Multi-Lingual-question-generation/
├── app.py                 # Main Flask app
├── config.py              # App configuration
├── utils.py               # Utility functions
├── pdf_processor.py       # PDF text extraction logic
├── question_generator.py  # Core QG engine
├── languages/             # Language-specific generation logic
│   ├── __init__.py
│   ├── english.py
│   ├── hindi.py
│   └── sanskrit.py
├── templates/             # Jinja2 HTML templates
│   ├── index.html
│   ├── upload.html
│   ├── result.html
│   └── error.html
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

##  Quick Start

###  Prerequisites

- Python 3.8 or higher
- `pip` package manager
- (Recommended) Virtual environment tool like `venv`

### 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Multi-Lingual-question-generation.git
   cd Multi-Lingual-question-generation
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables (optional)**:
   ```bash
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "FLASK_ENV=development" >> .env
   echo "DEBUG=True" >> .env
   ```

5. **Run the app**:
   ```bash
   python app.py
   ```

6. **Access in browser**:
   Open `http://localhost:5000` in your browser.

---

## 📖 Usage

### Step-by-Step Workflow

1. **Select Language**: Choose from English, Hindi, or Sanskrit
2. **Upload PDF**: Upload the document to process
3. **Enter Prompt**: Provide topics or keywords for relevance
4. **Configure**: Choose number of questions, type, and settings
5. **Generate**: Generate questions using AI
6. **Export**: Download or copy the output as needed

---

###  Supported Languages

- **English**: Uses transformer models with Retrieval-Augmented Generation (RAG)
- **Hindi**: Uses rule-based logic and pattern matching
- **Sanskrit**: Translation-assisted via Google Translate API

---

## ⚙️ Configuration (`config.py`)

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    ALLOWED_EXTENSIONS = {'pdf'}

    QUESTION_GENERATOR_MODEL = "valhalla/t5-small-qa-qg-hl"
    DEFAULT_TOTAL_QUESTIONS = 20
    DEFAULT_TOP_N_CHUNKS = 5
    CHUNK_SIZE = 1000
```

---

##  Development Notes

###  Project Structure

- Modular and extensible for new languages
- Type annotations throughout
- Logging and exception management
- Test-ready structure

###  Adding New Languages

1. Create a file in the `languages/` directory.
2. Implement logic for that language.
3. Register the new language in config and UI.
4. Update HTML templates accordingly.

---

## 🛠 Dependencies

### Core

- `Flask` – Web framework  
- `transformers` – Hugging Face models  
- `pdfplumber` / `PyMuPDF` – PDF parsing  
- `scikit-learn` – Machine learning utilities  
- `googletrans` – Translation API for Sanskrit

### Development

- `pytest` – Testing
- `black` – Code formatter
- `flake8` – Linter
- `mypy` – Type checker

---

##  Security Features

- Strict file type validation
- Sanitized file uploads
- Robust input validation
- No sensitive info leakage in error messages
- Auto-cleanup of uploaded files

---

##  Deployment

###  Production Deployment

```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
export DEBUG=False
```

Use **Gunicorn** for production:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Example Nginx reverse proxy config:
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

---

###  Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

##  Contributing

1. Fork the repo  
2. Create a new branch:  
   `git checkout -b feature/my-feature`
3. Commit and push:  
   `git commit -m "Add my feature"`  
   `git push origin feature/my-feature`
4. Open a pull request 

###  Guidelines

- Follow PEP 8
- Use type hints
- Write docstrings
- Cover code with tests
- Update documentation as needed

---

##  License

Licensed under the [MIT License](LICENSE).

---

##  Acknowledgments

- [Hugging Face](https://huggingface.co/) for transformer models  
- [Google Translate API](https://cloud.google.com/translate) for Sanskrit support  
- [Bootstrap](https://getbootstrap.com/) for UI  
- The open-source Python community 

---


