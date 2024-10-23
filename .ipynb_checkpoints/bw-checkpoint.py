import streamlit as st
import time
from pdfminer.high_level import extract_text
import re
import mysql.connector

# ------------------------- 1. Data Collection -------------------------
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    return extract_text(pdf_path)

st.title("Smart Resume Analyzer")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
resume_text = None

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.write("**Extracted Text from Resume**")
    st.write(resume_text)

# ------------------------- 2. Data Preparation -------------------------
def clean_resume_text(text):
    """
    Clean and normalize resume text.
    Remove special characters, extra spaces, etc.
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_skills(resume_text, skill_keywords):
    """
    Extract skills from resume text based on a predefined list of keywords.
    """
    resume_text = resume_text.lower()
    extracted_skills = [skill for skill in skill_keywords if skill.lower() in resume_text]
    return extracted_skills

# Example skill keywords list (expand this as needed)
skill_keywords = ['python', 'java', 'machine learning', 'data analysis', 'sql', 'html', 'css']

# Apply the data preparation steps
if resume_text:
    cleaned_resume_text = clean_resume_text(resume_text)
    skills = extract_skills(cleaned_resume_text, skill_keywords)

    st.write("**Extracted Skills**")
    st.write(skills)

# ------------------------- 3. Database Connection -------------------------
def create_connection():
    """
    Establish a connection to the MySQL database.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",        # Replace with your MySQL username
        password="Gaurav#06",   # Replace with your MySQL password
        database="sra"  # Replace with your database name
    )
    return connection

# Create a table for storing resume data
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        email VARCHAR(100),
                        resume_score INT,
                        skills TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
    connection.commit()
    connection.close()

# Insert resume data into the table
def insert_resume_data(name, email, score, skills):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO resumes (name, email, resume_score, skills) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, score, ', '.join(skills)))
    connection.commit()
    connection.close()

# Ensure table exists
create_table()

# ------------------------- 4. Analysis & Recommendations -------------------------
# Calculate resume score based on the presence of key sections
def calculate_resume_score(resume_text):
    resume_score = 0
    if 'Objective' in resume_text:
        resume_score += 20
    if 'Declaration' in resume_text:
        resume_score += 20
    if 'Hobbies' in resume_text or 'Interests' in resume_text:
        resume_score += 20
    if 'Achievements' in resume_text:
        resume_score += 20
    if 'Projects' in resume_text:
        resume_score += 20
    return resume_score

# Data Collection: Skills to Course Mapping
courses = {
    'python': ['Python for Everybody', 'Learn Python Programming'],
    'java': ['Java Programming Masterclass', 'Object-Oriented Programming in Java'],
    'machine learning': ['Machine Learning by Stanford University', 'Deep Learning Specialization'],
    'data analysis': ['Data Analyst Nanodegree', 'SQL for Data Science'],
}

# Function to recommend courses based on extracted skills
def recommend_courses(skills):
    recommended_courses = []
    for skill in skills:
        if skill in courses:
            recommended_courses.extend(courses[skill])
    return recommended_courses


# ------------------------- 5. Display & User Interaction -------------------------
if resume_text:
    # Calculate and display resume score
    resume_score = calculate_resume_score(resume_text)
    st.subheader("**Resume Score📝**")
    my_bar = st.progress(0)
    for percent_complete in range(resume_score):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    st.success(f"** Your Resume Writing Score: {resume_score} **")
    
    # Insert analyzed resume data into the database
    name = "John Doe"  # Example, should extract from resume text
    email = "johndoe@example.com"  # Example, should extract from resume text
    insert_resume_data(name, email, resume_score, skills)
    st.success("Resume data successfully stored in the database.")
    
    # Display course recommendations
    recommended_courses = recommend_courses(skills)
    st.write("**Recommended Courses**")
    st.write(recommended_courses)
    
    st.warning("**Note: This score is calculated based on the content that you have added in your resume.**")
    st.balloons()
