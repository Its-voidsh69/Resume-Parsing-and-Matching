# 🤖 Resume Parser & Job Matching System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/-Machine%20Learning-orange)]()
[![NLP](https://img.shields.io/badge/-NLP-green)]()

A comprehensive resume parsing and job recommendation system that intelligently matches candidates with job listings based on their **skills**, **education**, and **experience**.

---

## 🚀 Overview

This project implements an end-to-end solution for:

- 📄 Extracting key information from resumes using NLP
- 💼 Matching candidates with suitable job positions
- 📊 Predicting job categories using machine learning
- ✅ Providing detailed similarity & match scores

**Techniques Used:**
- TF-IDF Vectorization
- Cosine Similarity
- Content-Based Filtering
- Random Forest Classification (for category prediction)

---

## ✨ Key Features

- 🔍 **Resume Parsing:** Extracts structured info like skills, education, experience.
- 📈 **Job Matching:** Finds top 5 matching jobs with similarity scores.
- 🧠 **Detailed Score:** Compares resumes with job requirements on skills, education, and experience.
- 🧮 **Category Prediction:** Uses ML to classify resumes into job roles like Data Scientist, DevOps.
- 📊 **Evaluation Support:** Includes precision, recall, and F1-Score metrics.
---

## 🛠️ How It Works

### Step-by-Step Pipeline

#### 🧪 1. Data Input
```text
Resume: "Skills: Python, SQL, Machine Learning. Education: BS CS. Experience: 4 years"
Job:    "Data Scientist: Needs Python, ML, Statistics. Requires BS CS. Min 3 years"

🔧 2. Text Preprocessing
Before: "Required Skills: Python, Machine Learning!"
After:  "required skills python machine learning"

📊 3. Vectorization
Converts text into TF-IDF vectors.
TF-IDF: Python → 0.85, Machine Learning → 0.90

🧠 4. Similarity Scoring
Uses cosine similarity to compare resumes with jobs.
Resume-Job Similarity: 0.87

🎯 5. Detailed Matching
Computes percentage match:

Skills:     67% (2/3 matched)
Education:  100%
Experience: 100% (4 > 3 yrs)
Similarity: 87%
Final Score: 81.4%

📌 6. Category Prediction
Predicts job category using Random Forest:

Predicted Category: Data Science
