from flask import Flask, request, render_template
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
# import PyPDF2
import nltk
from nltk.corpus import stopwords
import string
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text)
    clean_tokens = [token.text for token in doc if token.text.lower() not in stop_words and token.text not in string.punctuation]
    return " ".join(clean_tokens)

def extract_resume_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += "\n" + page_text

    text = text.lower()

    section_headers = [
        "skills",
        "technical skills and interests",
        "technical skills",
        "work experience",
        "experience",
        "professional experience",
        "education",
        "academic background",
        "projects",
        "project experience",
        "personal projects"
    ]

    pattern = r'(?P<header>' + '|'.join(re.escape(h) for h in section_headers) + r')\s*[:\n]?(?P<content>.*?)(?=\n(?:' + '|'.join(re.escape(h) for h in section_headers) + r')\s*[:\n]?|$)'
    matches = re.finditer(pattern, text, re.DOTALL)

    extracted = {
        "skills": "Not Found",
        "experience": "Not Found",
        "education": "Not Found",
        "projects": "Not Found"
    }

    for match in matches:
        header = match.group("header")
        content = match.group("content").strip()

        if "skill" in header:
            extracted["skills"] = content
        elif "experience" in header:
            extracted["experience"] = content
        elif "education" in header or "academic" in header:
            extracted["education"] = content
        elif "project" in header:
            extracted["projects"] = content

    formatted_text = ""
    for section in ["skills", "experience", "education", "projects"]:
        formatted_text += f"\n### {section.capitalize()} ###\n{extracted[section]}\n"

    return preprocess_text(formatted_text)

def extract_text_from_txt(txt_path: str) -> str:
    """Read a .txt file and preprocess."""
    with open(txt_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    return preprocess_text(raw)

def extract_text(path: str) -> str:
    """Dispatch based on extension."""
    if path.lower().endswith('.pdf'):
        return extract_resume_text(path)
    if path.lower().endswith('.txt'):
        return extract_text_from_txt(path)
    return ""

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        jd_raw = request.form['job_description']
        job_description = preprocess_text(jd_raw)
        resume_files = request.files.getlist('resumes')

        resumes = []
        filenames = []

        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            resumes.append(extract_text(filename))
            filenames.append(resume_file.filename)

        if not resumes or not job_description:
            return render_template('matchresume.html', message="Please upload resumes and enter a job description.")

        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        top_indices = similarities.argsort()[-5:][::-1]
        top_resumes = [filenames[i] for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        top1_index = top_indices[0]
        top1_parsed = resumes[top1_index]

        return render_template(
            'matchresume.html',
            message="Top matching resumes:",
            top_resumes=top_resumes,
            similarity_scores=similarity_scores,
            top_resume_content={'filename': filenames[top1_index], 'content': top1_parsed}
        )

    return render_template('matchresume.html')

@app.route("/matchjob")
def match_job_page():
    return render_template("matchjob.html")

@app.route("/jobmatcher", methods=["POST"])
def jobmatcher():
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    resume_file = request.files.get('resume')
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(resume_path)
    resume_text = extract_text(resume_path)

    job_texts = []
    job_names = []
    for jf in request.files.getlist('jobs'):
        path = os.path.join(app.config['UPLOAD_FOLDER'], jf.filename)
        jf.save(path)
        job_texts.append(extract_text(path))
        job_names.append(jf.filename)

    vecs = TfidfVectorizer().fit_transform([resume_text] + job_texts).toarray()
    sims = cosine_similarity([vecs[0]], vecs[1:])[0]

    idx = sims.argsort()[::-1]
    results = [(job_names[i], round(float(sims[i]), 2)) for i in idx]

    return render_template("matchjob.html", results=results)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
