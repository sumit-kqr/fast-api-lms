import requests
import json

# Base URL of the FastAPI application
BASE_URL = "http://127.0.0.1:8000"

# Function to send POST request and handle response
def post_data(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print(f"Success: {endpoint} - {response.json()}")
        return response.json()["id"]  # Return the ID of the created record
    else:
        print(f"Failed: {endpoint} - Status: {response.status_code}, Message: {response.text}")
        return None

# Sample data for each table

# 1. Users Table (10 examples)
users_data = [
    {"email": "teacher1@example.com", "role": "teacher"},
    {"email": "teacher2@example.com", "role": "teacher"},
    {"email": "student1@example.com", "role": "student"},
    {"email": "student2@example.com", "role": "student"},
    {"email": "admin1@example.com", "role": "teacher"},
    {"email": "student3@example.com", "role": "student"},
    {"email": "teacher3@example.com", "role": "teacher"},
    {"email": "student4@example.com", "role": "student"},
    {"email": "teacher4@example.com", "role": "teacher"},
    {"email": "student5@example.com", "role": "student"}
]

user_ids = []
for user in users_data:
    user_id = post_data("/users", user)
    if user_id:
        user_ids.append(user_id)

# 2. Courses Table (10 examples, using user_ids)
courses_data = [
    {"title": "Introduction to Python", "description": "A beginner course on Python programming", "user_id": user_ids[0]},
    {"title": "Advanced Python", "description": "Deep dive into Python concepts", "user_id": user_ids[1]},
    {"title": "Web Development Basics", "description": "Introduction to web development", "user_id": user_ids[2]},
    {"title": "Data Science 101", "description": "Basics of data science with Python", "user_id": user_ids[3]},
    {"title": "Machine Learning Fundamentals", "description": "Introduction to ML algorithms", "user_id": user_ids[4]},
    {"title": "Database Design", "description": "Learn database concepts", "user_id": user_ids[5]},
    {"title": "Cloud Computing", "description": "Overview of cloud technologies", "user_id": user_ids[6]},
    {"title": "Cybersecurity Basics", "description": "Introduction to cybersecurity", "user_id": user_ids[7]},
    {"title": "DevOps Essentials", "description": "Basics of DevOps practices", "user_id": user_ids[8]},
    {"title": "AI for Beginners", "description": "Introduction to artificial intelligence", "user_id": user_ids[9]}
]

course_ids = []
for course in courses_data:
    course_id = post_data("/courses", course)
    if course_id:
        course_ids.append(course_id)

# 3. Sections Table (10 examples, using course_ids)
sections_data = [
    {"title": "Module 1: Python Basics", "description": "Introduction to Python basics", "course_id": course_ids[0]},
    {"title": "Module 2: Functions", "description": "Understanding Python functions", "course_id": course_ids[0]},
    {"title": "Module 1: HTML Basics", "description": "Introduction to HTML", "course_id": course_ids[2]},
    {"title": "Module 1: Data Analysis", "description": "Basics of data analysis", "course_id": course_ids[3]},
    {"title": "Module 1: ML Overview", "description": "Overview of machine learning", "course_id": course_ids[4]},
    {"title": "Module 1: Database Concepts", "description": "Introduction to databases", "course_id": course_ids[5]},
    {"title": "Module 1: Cloud Intro", "description": "Introduction to cloud computing", "course_id": course_ids[6]},
    {"title": "Module 1: Security Basics", "description": "Basics of cybersecurity", "course_id": course_ids[7]},
    {"title": "Module 1: DevOps Tools", "description": "Introduction to DevOps tools", "course_id": course_ids[8]},
    {"title": "Module 1: AI Concepts", "description": "Basic concepts of AI", "course_id": course_ids[9]}
]

section_ids = []
for section in sections_data:
    section_id = post_data("/sections/", section)
    if section_id:
        section_ids.append(section_id)

# 4. Content Blocks Table (10 examples, using section_ids)
content_blocks_data = [
    {"title": "Lesson 1: Variables", "description": "Learn about variables", "type": "lesson", "section_id": section_ids[0]},
    {"title": "Quiz 1: Variables", "description": "Quiz on variables", "type": "quiz", "section_id": section_ids[0]},
    {"title": "Lesson 1: HTML Tags", "description": "Learn HTML tags", "type": "lesson", "section_id": section_ids[2]},
    {"title": "Assignment 1: Data Analysis", "description": "Data analysis assignment", "type": "assignment", "section_id": section_ids[3]},
    {"title": "Lesson 1: ML Algorithms", "description": "Introduction to ML algorithms", "type": "lesson", "section_id": section_ids[4]},
    {"title": "Quiz 1: Databases", "description": "Quiz on database concepts", "type": "quiz", "section_id": section_ids[5]},
    {"title": "Lesson 1: Cloud Services", "description": "Learn cloud services", "type": "lesson", "section_id": section_ids[6]},
    {"title": "Assignment 1: Security", "description": "Security assignment", "type": "assignment", "section_id": section_ids[7]},
    {"title": "Lesson 1: DevOps Practices", "description": "Introduction to DevOps", "type": "lesson", "section_id": section_ids[8]},
    {"title": "Quiz 1: AI Basics", "description": "Quiz on AI basics", "type": "quiz", "section_id": section_ids[9]}
]

for content_block in content_blocks_data:
    post_data("/content-blocks/", content_block)

print("Sample data insertion with 10+ rows per table completed!")