from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import base64
import io
import pymysql
from PIL import Image
import streamlit as st
from pdfminer.high_level import extract_text
import random
import time
import pafy
import plotly.express as px
import yt_dlp


# Function to fetch YouTube video details using yt-dlp
def fetch_yt_video(link):
    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        video_title = info_dict.get('title', None)  # Extract video title
        return video_title


# Database Connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Gaurav#06',
    database='sra'
)
cursor = connection.cursor()



def pdf_reader(file):
    # Extract text using pdfminer
    text = extract_text(file)

    # Extract number of pages using PyPDF2
    pdf_reader = PdfReader(file)
    num_pages = len(pdf_reader.pages)

    # Print extracted text and page count for debugging
    st.write("Extracted Text:")
    st.write(text)
    st.write(f"Number of Pages: {num_pages}")

    return text, num_pages

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    save_path = './Uploaded_Resumes/' + uploaded_file.name
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path




import spacy
import pandas as pd
import random
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy
import plotly.express as px

import re
import spacy

# Load SpaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Define a comprehensive list of skills for extraction
skill_list = [
    'Basics of C', 'Python', 'Networking', 'Switching & Routing', 'PCB Designing',
    'Adaptability', 'Strong Work Ethic', 'Collaboration', 'Problem Solving',
    'C language (Code Chef)', 'Introduction to Programming with MATLAB', 'Embedded IoT',
    'Active Listening', 'Java', 'Javascript', 'Matlab', 'R', 'Data Mining',
    'Data Analysis', 'Machine Learning', 'Sphinx', 'LaTeX', 'Mathematica', 'Maple', 'GIT',
    'CVS', 'HTCondor', 'Cyber Security', 'C++', 'SQL', 'Swift', 'Objective-C', 'XCode',
    'Cocoa Touch', 'Sqlite', 'Plist', 'NSUserDefaults', 'XML', 'JSON', 'REST', 'SOAP',
    'Adobe Creative Cloud', 'Photoshop', 'Illustrator', 'InDesign', 'Premiere Pro',
    'After Effects', 'HTML', 'CSS', 'SASS', 'WordPress', 'Letterpress printing',
    'Prototyping', 'Invision', 'Axure'
]

# Update the extract_resume_data function to check for skills
def extract_resume_data(resume_text):
    doc = nlp(resume_text)

    # Define regex patterns for email and phone number extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\+?\d{1,4}[-.\s]?)?(?!0+\s+,?$)\d{10,13}'

    # Extract name, email, and phone
    extracted_data = {
        'Name': '',
        'Email': '',
        'Phone': '',
        'Skills': []
    }
    
    # Extract Name using SpaCy's NER
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            extracted_data['Name'] = ent.text
            break  # Capture the first person name

    # Fallback to extract the first line as the name if SpaCy fails
    if not extracted_data['Name']:
        lines = resume_text.splitlines()
        # Fallback: Use the first non-empty line as the name
        for line in lines:
            if line.strip():
                extracted_data['Name'] = line.strip()
                break

    # Extract Email using regex
    email_match = re.search(email_pattern, resume_text)
    if email_match:
        extracted_data['Email'] = email_match.group(0)

    # Extract Phone number using regex
    phone_match = re.search(phone_pattern, resume_text)
    if phone_match:
        extracted_data['Phone'] = phone_match.group(0)

    # Extract Skills by checking for each skill in the resume text
    for skill in skill_list:
        if skill.lower() in resume_text.lower():
            extracted_data['Skills'].append(skill)

    return extracted_data


def determine_career_level(no_of_pages):
    if no_of_pages == 1:
        return "You are at Fresher level!"
    elif no_of_pages == 2:
        return "You are at Intermediate level!"
    else:
        return "You are at Experienced level!"




import streamlit as st
from streamlit_tags import st_tags  # Import st_tags from streamlit-tags
import random

def recommend_courses(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    
    for c_name, c_link in course_list:
        st.markdown(f"- [{c_name}]({c_link})")  # Display as markdown links
        rec_course.append(c_name)
        if len(rec_course) == no_of_reco:
            break
    return rec_course

def recommend_skills(user_skills):
    ds_keywords = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning','python', 'data mining', 'data analysis', 'machine learning', 'r', 'matlab','sql','streamlit','deep Learning', 'flask']
    web_keywords = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress','javascript', 'angular js', 'c#', 'flask']
    android_keywords =['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
    ios_keywords = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
    uiux_keywords = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes','storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator','illustrator', 'adobe after effects', 'after effects', 'adobe premier pro','premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp','user research', 'user experience']

    recommended_skills = []
    reco_field = ''
    rec_courses = []

    for skill in user_skills:
        if skill.lower() in ds_keywords:
            reco_field = 'Data Science'
            recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling','r','sql','python','deep learning','Data Mining', 'Clustering & Classification', 'Data Analytics','Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras','Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask", 'Streamlit']
            rec_courses = recommend_courses(ds_course)
            break
        elif skill.lower() in web_keywords:
            reco_field = 'Web Development'
            recommended_skills = ['react', 'django', 'node js', 'react js']
            rec_courses = recommend_courses(web_course)
            break
        elif skill.lower() in android_keywords:
            reco_field = 'Android Development'
            recommended_skills = ['android', 'android development', 'flutter','html', 'css', 'javascript', 'wordpress']
            rec_courses = recommend_courses(android_course)
            break
        elif skill.lower() in ios_keywords:
            reco_field = 'IOS Development'
            recommended_skills = ['ios', 'ios development', 'swift']
            rec_courses = recommend_courses(ios_course)
            break
        elif skill.lower() in uiux_keywords:
            reco_field = 'UI-UX Development'
            recommended_skills = ['ux', 'adobe xd', 'figma','photoshop', 'illustrator', 'indesign', 'prototyping']
            rec_courses = recommend_courses(uiux_course)
            break

    return reco_field, recommended_skills, rec_courses

def score_resume(resume_text):
    score = 0
    
    # Check for the presence of an Objective section or similar terms
    if re.search(r'objective|career goal|professional summary', resume_text, re.IGNORECASE):
        score += 20
    
    # Check for Declaration section or related terms
    if re.search(r'declaration|certification|statement', resume_text, re.IGNORECASE):
        score += 20
    
    # Check for Hobbies, Interests, or similar terms
    if re.search(r'hobbies|interests|extracurricular', resume_text, re.IGNORECASE):
        score += 20
    
    # Check for Achievements, Awards, or similar terms
    if re.search(r'achievements|awards|recognition|accomplishments', resume_text, re.IGNORECASE):
        score += 20
    
    # Check for Projects, Work Experience, or similar terms
    if re.search(r'projects|project experience|work experience|professional experience|assignments', resume_text, re.IGNORECASE):
        score += 20

    return score


def display_resume_score(score):
    st.subheader("**Resume Score📝**")
    my_bar = st.progress(0)
    for percent_complete in range(score):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    st.success(f'**Your Resume Writing Score: {score}**')
    st.warning("**Note: This score is based on the content in your resume.**")
    st.balloons()

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    # If skills, recommended_skills, or courses are lists, join them into comma-separated strings
    skills_str = ', '.join(skills) if isinstance(skills, list) else skills
    recommended_skills_str = ', '.join(recommended_skills) if isinstance(recommended_skills, list) else recommended_skills
    courses_str = ', '.join(courses) if isinstance(courses, list) else courses

    # Handling empty values by replacing them with None (or a default email if email is missing)
    name = name if name else None
    email = email if email else "unknown@example.com"  # Use a default email if it's missing
    reco_field = reco_field if reco_field else "Unknown"
    cand_level = cand_level if cand_level else "Unknown"
    skills_str = skills_str if skills_str else "Unknown"
    recommended_skills_str = recommended_skills_str if recommended_skills_str else 'Unknown'
    courses_str = courses_str if courses_str else 'Unknown'

    # SQL insert query
    insert_sql = """INSERT INTO user_data 
                    (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # Values to be inserted
    rec_values = (name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills_str, recommended_skills_str, courses_str)

    # Execute the SQL query and commit changes
    cursor.execute(insert_sql, rec_values)
    connection.commit()


def analyze_resume_and_score(resume_text):
    score = 0
    feedback = []

    # Sections to check and the feedback/score to provide
    sections = {
        'objective|career goal|professional summary': ("Objective", 20, "Add your career objective to give career intention."),
        'declaration|certification|statement': ("Declaration", 20, "Add a declaration for authenticity."),
        'hobbies|interests|extracurricular': ("Hobbies", 20, "Include hobbies to show interests beyond work."),
        'achievements|awards|recognition|accomplishments': ("Achievements", 20, "Add achievements to show capability."),
        'projects|project experience|work experience|professional experience|assignments|Projects': ("Projects/Experience", 20, "Add projects or work experience relevant to the position.")
    }

    for pattern, (section, pts, message) in sections.items():
        if re.search(pattern, resume_text, re.IGNORECASE):
            score += pts
            feedback.append(f'<p style="color: green;">[+] Awesome! You have added {section}.</p>')
        else:
            feedback.append(f'<p style="color: red;">[-] According to our recommendation, please {message}</p>')

    return score, feedback




import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px


def run():
    st.title("Smart Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    img = Image.open(r'C:\Users\RAVI\OneDrive\Desktop\Smart_Resume_Analyser_App\Logo\SRA_Logo.jpg')
    img = img.resize((250, 250))
    st.image(img)

    # Create the DB and Table
    cursor.execute("CREATE DATABASE IF NOT EXISTS sra;")
    cursor.execute("USE sra")
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_data (
                        ID INT NOT NULL AUTO_INCREMENT,
                        Name VARCHAR(100) NOT NULL,
                        Email_ID VARCHAR(50) NOT NULL,
                        resume_score VARCHAR(8) NOT NULL,
                        Timestamp VARCHAR(50) NOT NULL,
                        Page_no VARCHAR(5) NOT NULL,
                        Predicted_Field VARCHAR(25) NOT NULL,
                        User_level VARCHAR(30) NOT NULL,
                        Actual_skills VARCHAR(300) NOT NULL,
                        Recommended_skills VARCHAR(300) NOT NULL,
                        Recommended_courses VARCHAR(600) NOT NULL,
                        PRIMARY KEY (ID)
                    );""")

    if choice == 'Normal User':
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            save_path = save_uploaded_file(pdf_file)
            display_pdf(save_path)
            resume_text, num_pages = pdf_reader(save_path)  # Receive the page count from pdf_reader
            resume_data = extract_resume_data(resume_text)
            resume_data['No_of_Pages'] = num_pages  # Add page count to resume data
        
            if resume_data:
                st.header("**Resume Analysis**")
                st.success(f"Hello {resume_data['Name']}")
                st.subheader("**Your Basic info**")
                st.text(f'Name: {resume_data.get("Name", "N/A")}')
                st.text(f'Email: {resume_data.get("Email", "N/A")}')
                st.text(f'Resume pages: {resume_data.get("No_of_Pages", "N/A")}')

                # Determine the career level message
                cand_level = determine_career_level(resume_data.get('No_of_Pages', 0))
                st.markdown(f'<h4 style="text-align: left; color: #1ed760;">{cand_level}</h4>', unsafe_allow_html=True)

                # Skills Recommendation Section
                reco_field, recommended_skills, rec_courses = recommend_skills(resume_data.get('Skills', []))

                st.subheader("**Skills Recommendation💡**")
                st_tags(label='### Skills that you have', text='See our skills recommendation', value=resume_data.get('Skills', []))

                # Recommended Skills Section
                st.subheader("**Recommended Skills**")
                st_tags(label='### Recommended skills for you.', text='Recommended skills generated from System', value=recommended_skills)

                # Courses Recommendation Section (added here)
                st.subheader("**Courses & Certificates🎓 Recommendations**")
                for course in rec_courses:
                    st.markdown(f"- {course}")  # Display course recommendations as markdown
                # Analyze the resume and score it
                score, feedback = analyze_resume_and_score(resume_text)
                st.subheader("**Resume Tips & Ideas 💡**")
                for tip in feedback:
                    st.markdown(tip, unsafe_allow_html=True)
                # Score the resume
                score = score_resume(resume_text)
                display_resume_score(score)

                # Insert the extracted data into the database
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_data(resume_data['Name'], resume_data['Email'], score, timestamp, resume_data.get('No_of_Pages', 0), reco_field, cand_level, ', '.join(resume_data.get('Skills', [])), ', '.join(recommended_skills), ', '.join(rec_courses))
                    ## Resume writing video
                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                res_vid_title = fetch_yt_video(resume_vid)
                st.subheader("✅ **" + res_vid_title + "**")
                st.video(resume_vid)

                ## Interview Preparation Video
                st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
                interview_vid = random.choice(interview_videos)
                int_vid_title = fetch_yt_video(interview_vid)
                st.subheader("✅ **" + int_vid_title + "**")
                st.video(interview_vid)

    else:
        ## Admin Side
        st.success('Welcome to Admin Side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'Gaurav' and ad_password == 'Gaurav123':
                st.success("Welcome Gaurav")
                # Display Data
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

            else:
                st.error("Wrong ID & Password Provided")


if __name__ == "__main__":
    run()
