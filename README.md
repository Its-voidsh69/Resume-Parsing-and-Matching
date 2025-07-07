# 🧠 Resume and Job Description Matching System

A simple and effective resume-job matcher built with Python, Flask, and basic NLP techniques. This project matches resumes to job descriptions (and vice versa) using TF-IDF vectorization and cosine similarity.

## 🔍 Features

- ✅ **Resume-to-Job Matching**: Upload a resume and compare it with multiple job descriptions (in `.txt` format) to find the best-fit jobs.
- ✅ **Job-to-Resume Matching**: Upload multiple resumes and compare them with a job description to find the top matching candidates.
- 📄 **Resume Parsing**: Extracts sections like Skills, Experience, Education, and Projects using simple regex.
- ✨ Clean and responsive Bootstrap-based UI with improved styling and file upload support.

## 📂 Project Structure
.
├── app.py # Flask application
├── templates/
│ ├── matchresume.html # UI for job → resume matching
│ └── matchjob.html # UI for resume → job matching
├── uploads/ # Temporarily stores uploaded files
└── README.md

## 🚀 How It Works

1. **Job-to-Resume Matching**
   - User enters a job description and uploads multiple resumes.
   - Resumes are parsed and cleaned.
   - TF-IDF is used to vectorize text.
   - Cosine similarity ranks top 5 matching resumes.

2. **Resume-to-Job Matching**
   - User uploads a resume and multiple `.txt` job description files.
   - The resume is compared with each job description.
   - Returns a ranked list of best-fit jobs.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **NLP**: spaCy, NLTK, scikit-learn
- **Parsing**: PyPDF2 for PDF, regex-based section extraction
- **Frontend**: HTML, CSS (Bootstrap), Jinja2

## 📦 Requirements

Install the dependencies via pip:

```bash
pip install -r requirements.txt

🖥️ Running the App
python app.py
Visit http://localhost:5000 in your browser.

For Job → Resume: go to /

For Resume → Job: go to /matchjob
