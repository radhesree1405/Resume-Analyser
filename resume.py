import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load skills list
with open("skills.txt", "r") as f:
    skills_list = [line.strip().lower() for line in f.readlines()]

st.title("AI Resume Analyzer")

st.write("Upload a resume and compare it with a job description.")

# Upload resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("Paste Job Description Here")

# Function to extract text from PDF
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# Function to detect skills
def extract_skills(text):
    found_skills = []
    text_lower = text.lower()

    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))

# Function to calculate match score
def calculate_match(resume_skills, job_text):
    job_text = job_text.lower()
    matched = 0

    for skill in resume_skills:
        if skill in job_text:
            matched += 1

    if len(resume_skills) == 0:
        return 0

    score = (matched / len(resume_skills)) * 100
    return round(score, 2)

# Main processing
if resume_file:

    resume_text = extract_text(resume_file)

    st.subheader("Extracted Resume Text")
    st.write(resume_text[:800])

    detected_skills = extract_skills(resume_text)

    st.subheader("Detected Skills")
    st.write(detected_skills)

    # Show table
    df = pd.DataFrame(detected_skills, columns=["Skills Found"])
    st.dataframe(df)

    if job_description:

        score = calculate_match(detected_skills, job_description)

        st.subheader("Job Match Score")
        st.progress(int(score))

        st.write(f"Resume matches **{score}%** of the job description.")