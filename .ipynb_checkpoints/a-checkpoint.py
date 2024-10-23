import spacy
import pdfminer
from pdfminer.high_level import extract_text

# Load the pre-trained model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    return extract_text(pdf_path)

def extract_entities(text):
    """Extract entities like name, email, etc. from text using spacy."""
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities['name'] = ent.text
        elif ent.label_ == "EMAIL":
            entities['email'] = ent.text
    return entities

# Define skill keywords for different fields
ds_keywords = ['machine learning', 'data science', 'python', 'tensorflow', 'keras', 'pandas']
web_keywords = ['javascript', 'html', 'css', 'react', 'node.js', 'flask']
android_keywords = ['android', 'kotlin', 'java', 'flutter']
ios_keywords = ['ios', 'swift', 'xcode', 'objective-c']
uiux_keywords = ['figma', 'adobe xd', 'prototyping', 'wireframing']

# Recommend courses based on skills
def recommend_field_and_courses(skills):
    if any(skill in ds_keywords for skill in skills):
        return 'Data Science', ['Data Visualization', 'Predictive Analytics']
    elif any(skill in web_keywords for skill in skills):
        return 'Web Development', ['React', 'Node.js']
    elif any(skill in android_keywords for skill in skills):
        return 'Android Development', ['Kotlin', 'Flutter']
    elif any(skill in ios_keywords for skill in skills):
        return 'iOS Development', ['Swift', 'Xcode']
    elif any(skill in uiux_keywords for skill in skills):
        return 'UI/UX', ['Figma', 'Adobe XD']
    else:
        return 'Unknown', []

import mysql.connector
from mysql.connector import Error

# MySQL connection details
host = 'localhost'
database = 'sra'
user = 'root'
password = 'Gaurav#06'

def create_connection():
    """Create a database connection to the MySQL server."""
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

def insert_data(name, email, score, timestamp, no_of_pages, reco_field, user_level, skills, recommended_skills, course):
    """Insert extracted data into the database."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO user_data (name, email, resume_score, timestamp, no_of_pages, predicted_field,
                                          user_level, actual_skills, recommended_skills, recommended_course)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (name, email, score, timestamp, no_of_pages, reco_field, user_level, skills, recommended_skills, course)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

import streamlit as st
import time

# Upload resume and extract text
st.title("Smart Resume Analyzer")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Extract text from the uploaded PDF
    resume_text = extract_text_from_pdf(uploaded_file)
    st.write("**Extracted Text from Resume**")
    st.write(resume_text)

    # Extract entities (name, email, etc.)
    resume_data = extract_entities(resume_text)
    st.write(f"**Name**: {resume_data.get('name')}")
    st.write(f"**Email**: {resume_data.get('email')}")

    # Extract skills and recommend field and courses
    skills = resume_text.lower().split()  # Simplified skill extraction
    reco_field, recommended_courses = recommend_field_and_courses(skills)
    st.write(f"**Recommended Field**: {reco_field}")
    st.write(f"**Recommended Courses**: {', '.join(recommended_courses)}")

    # Insert data into MySQL
    timestamp = time.strftime('%Y-%m-%d_%H:%M:%S')
    insert_data(resume_data.get('name', 'Unknown'), resume_data.get('email', 'Unknown'), 80, timestamp, 1, reco_field,
                'Intermediate', skills, recommended_courses, recommended_courses)
    
    st.success(f"Resume data inserted into database successfully!")

import plotly.express as px
import pandas as pd

def display_admin_panel():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    data = cursor.fetchall()

    # Display data
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'No. of Pages',
                                     'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                     'Recommended Course'])
    st.dataframe(df)

    # Pie chart for predicted fields
    field_counts = df['Predicted Field'].value_counts()
    fig = px.pie(names=field_counts.index, values=field_counts.values, title="Predicted Fields Distribution")
    st.plotly_chart(fig)

# Admin Login
st.sidebar.subheader("Admin Login")
admin_user = st.sidebar.text_input("Username")
admin_password = st.sidebar.text_input("Password", type="password")

if admin_user == "admin" and admin_password == "admin123":
    st.success("Logged in as Admin")
    display_admin_panel()



import streamlit as st
from pdfminer.high_level import extract_text
import re
import mysql.connector

# Database connection
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gaurav#06",  # Replace with your MySQL password
        database="sra"
    )
    return connection

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

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# Clean and process resume text
def clean_resume_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text

# Extract skills from resume text
def extract_skills(resume_text, skill_keywords):
    resume_text = resume_text.lower()
    extracted_skills = [skill for skill in skill_keywords if skill.lower() in resume_text]
    return extracted_skills

# Insert resume data into database
def insert_resume_data(name, email, score, skills):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO resumes (name, email, resume_score, skills) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, score, ', '.join(skills)))
    connection.commit()
    connection.close()

# Recommend courses based on skills
def recommend_courses(skills):
    courses = {
        'python': ['Python for Everybody', 'Learn Python Programming'],
        'java': ['Java Programming Masterclass', 'Object-Oriented Programming in Java'],
        'machine learning': ['Machine Learning by Stanford University', 'Deep Learning Specialization'],
        'data analysis': ['Data Analyst Nanodegree', 'SQL for Data Science'],
    }
    recommended_courses = []
    for skill in skills:
        if skill in courses:
            recommended_courses.extend(courses[skill])
    return recommended_courses

# Create UI layout
def main():
    # Define a session state variable for admin login
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    
    # Admin Login section
    if not st.session_state.admin_logged_in:
        st.title("Admin Login")
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'machine_learning_hub' and ad_password == 'mlhub123':
                st.success("Logged in as Admin")
                st.session_state.admin_logged_in = True
            else:
                st.error("Incorrect username or password")
    
    # If admin is logged in, display admin content
    if st.session_state.admin_logged_in:
        st.success("Welcome to Admin Dashboard!")
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute('''SELECT*FROM resumes''')
        data = cursor.fetchall()
        st.header("**User's Data**")
        df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Skills', 'Timestamp'])
        st.dataframe(df)
    
    else:
        # Smart Resume Analyzer section for users
        st.title("Smart Resume Analyzer")
        
        # File upload
        uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf", key="resume_uploader")
        
        if uploaded_file is not None:
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if resume_text:
                st.write("**Extracted Text from Resume**")
                st.write(resume_text)
                
                # Data Preparation
                cleaned_resume_text = clean_resume_text(resume_text)
                st.write("**Cleaned Resume Text**")
                st.write(cleaned_resume_text)
                
                # Extracting skills
                skill_keywords = ['python', 'java', 'machine learning', 'data analysis', 'sql', 'html', 'css']
                extracted_skills = extract_skills(cleaned_resume_text, skill_keywords)
                st.write("**Extracted Skills**")
                st.write(extracted_skills)

                # Resume Score calculation (based on presence of specific sections)
                resume_score = 0
                sections = ['objective', 'declaration', 'hobbies', 'achievements', 'projects']
                for section in sections:
                    if section in resume_text.lower():
                        resume_score += 20
                
                st.write(f"**Resume Score**: {resume_score}/100")
                
                # Database Insertion
                name = st.text_input("Enter your name", key="name_input")
                email = st.text_input("Enter your email", key="email_input")
                if st.button("Save Resume Data", key="save_button"):
                    if name and email:
                        insert_resume_data(name, email, resume_score, extracted_skills)
                        st.success("Resume data saved successfully!")
                    else:
                        st.error("Please enter your name and email")

                # Course Recommendations
                st.write("**Recommended Courses**")
                recommended_courses = recommend_courses(extracted_skills)
                st.write(recommended_courses)
                
            else:
                st.error("Could not extract text from the uploaded resume. Please try again.")
        else:
            st.info("Please upload a PDF resume to start the analysis.")

# Ensure database table exists
create_table()

if __name__ == "__main__":
    main()
