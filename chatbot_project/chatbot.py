from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import random
from datetime import datetime, timedelta
import re

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined responses
predefined_answers = {
    "hi": [
        "Hello! How can I assist you today?",
        "Hi! How can I help you today?",
        "Hey there! How can I be of service?"
    ],
    "tell me a joke": [
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "Why did the programmer quit his job? Because he didn’t get arrays!",
        "I told my computer I needed a break, now it won’t stop sending me Kit-Kats!",
        "Why do Java developers wear glasses? Because they don’t C#!",
        "I’m reading a book on anti-gravity. It’s impossible to put down!"
    ],
    "what is thi": [
        "Technische Hochschule Ingolstadt (THI) is a university located in Ingolstadt, Germany, offering various academic programs in engineering, business, computer science, and more."
    ],
    "what is the tuition fee": [
        "The tuition fees at THI vary depending on your nationality and program. International students typically pay tuition fees, while EU students may not have to pay them."
    ],
    "who is the president of thi": [
        "The current president of Technische Hochschule Ingolstadt is Prof. Dr. Walter O. L. Meißner."
    ],
    "what programs are available at thi": [
        "THI offers a variety of undergraduate and postgraduate programs including Engineering, Business Administration, Computer Science, and Artificial Intelligence."
    ],
    "what are the admission requirements": [
        "Admission requirements vary by program. Generally, you will need a recognized high school diploma or relevant bachelor's degree, and proof of language proficiency (usually English or German)."
    ],
    "what is the application process for thi": [
        "The application process involves submitting your documents online through the THI application portal. Be sure to check the specific program’s deadlines and requirements."
    ],
    "is thi a public university": [
        "Yes, Technische Hochschule Ingolstadt is a public university in Germany."
    ],
    "is english a language of instruction at thi": [
        "Yes, many programs at THI offer courses in English, especially at the postgraduate level."
    ],
    "is it difficult to get into thi": [
        "Admission to THI is competitive, especially for popular programs. Meeting the academic requirements and submitting strong application documents will increase your chances."
    ],
    "where is thi located": [
        "THI is located in Ingolstadt, Bavaria, Germany, which is about an hour's drive north of Munich."
    ],
    "how far is thi from munich": [
        "THI is approximately 80 kilometers (50 miles) from Munich, about an hour by car."
    ],
    "what is the campus like at thi": [
        "The THI campus is modern, with state-of-the-art facilities for students. It includes libraries, computer labs, lecture halls, and recreational spaces."
    ],
    "is there accommodation on campus at thi": [
        "THI does not provide on-campus housing, but there are plenty of student accommodations available in Ingolstadt and nearby areas."
    ],
    "what is the cost of living in ingolstadt": [
        "The cost of living in Ingolstadt can vary, but on average, students can expect to spend around €800 to €1,200 per month for rent, food, and other living expenses."
    ],
    "does thi offer scholarships": [
        "Yes, THI offers various scholarships for international and German students. Be sure to check the scholarship opportunities on their website."
    ],
    "how can I apply for a scholarship at thi": [
        "You can apply for scholarships through the THI scholarship portal. Be sure to check eligibility criteria and deadlines for each scholarship."
    ],
    "does thi accept international students": [
        "Yes, THI welcomes international students and offers a range of programs in English to support their studies."
    ],
    "how do I apply as an international student at thi": [
        "International students can apply online through the THI application portal, ensuring they meet the specific entry requirements for their chosen program."
    ],
    "what is the deadline for applications to thi": [
        "Application deadlines vary by program. It is important to check the specific deadlines for the program you are interested in. Generally, the application deadlines are in July for the winter semester and January for the summer semester."
    ],
    "what are the job opportunities after graduation from thi": [
        "THI graduates have strong job prospects, especially in industries like engineering, automotive, business, and IT. The university also provides career services to help students find jobs."
    ],
    "is thi a recognized university": [
        "Yes, Technische Hochschule Ingolstadt is a recognized public university in Germany, accredited by the German government."
    ],
    "is the degree from thi recognized internationally": [
        "Yes, degrees from THI are internationally recognized, particularly within the European Union and other countries that recognize German higher education institutions."
    ],
    "can I study in english at thi": [
        "Yes, many programs, particularly at the postgraduate level, are offered in English. Some undergraduate programs may require German proficiency."
    ],
    "does thi offer a master's program": [
        "Yes, THI offers several Master's programs in fields such as Engineering, Business Administration, Computer Science, and Artificial Intelligence."
    ],
    "does thi offer an MBA program": [
        "Yes, THI offers a Master of Business Administration (MBA) program designed to equip students with leadership and management skills."
    ],
    "can I do a PhD at thi": [
        "While THI doesn't offer standalone PhD programs, students can pursue doctoral research in collaboration with other universities or research institutions."
    ],
    "what is the language proficiency requirement for international students at thi": [
        "The language proficiency requirements for international students vary by program. Most programs require either English or German language proficiency, depending on the language of instruction."
    ],
    "what level of german is required for admission to thi": [
        "For programs taught in German, you will generally need to have a B2 or C1 level of German proficiency, but it varies by program."
    ],
    "do I need a visa to study at thi": [
        "Yes, international students from non-EU countries will need a student visa to study at THI. Make sure to apply for a visa well in advance of your program's start date."
    ],
    "how do I get a student visa for germany": [
        "To get a student visa for Germany, you will need to provide proof of admission to THI, financial support, health insurance, and other documents as specified by the German consulate."
    ],
    "what are the living costs in ingolstadt": [
        "Living costs in Ingolstadt are typically between €800 and €1,200 per month, depending on your lifestyle and accommodation choices."
    ],
    "how many students are there at thi": [
        "THI has around 7,000 students enrolled in various undergraduate and postgraduate programs."
    ],
    "does thi have a student union": [
        "Yes, THI has an active student union that represents students and organizes events and activities."
    ],
    "does thi have a campus restaurant": [
        "Yes, there are several campus restaurants and cafeterias offering a variety of meals to students."
    ],
    "how can I contact the admissions office at thi": [
        "You can contact the admissions office at THI through the contact information provided on their official website or by email."
    ],
    "does thi have sports facilities": [
        "Yes, THI has sports facilities, including gyms and sports fields, for students to use."
    ],
    "is there a library at thi": [
        "Yes, THI has a well-equipped library with a wide range of academic resources for students."
    ],
    "does thi have a career center": [
        "Yes, THI has a career center that helps students with job placement, internships, and career counseling."
    ],
    "what are the visa requirements for international students at thi": [
        "International students must provide proof of admission, financial support, and health insurance, and meet other visa requirements specific to their country of origin."
    ],
    "what is the grading system at thi": [
        "The grading system at THI follows the German grading scale, where 1.0 is the best grade (very good) and 5.0 is the lowest passing grade."
    ],
    "is there a student exchange program at thi": [
        "Yes, THI has student exchange programs with partner universities around the world, allowing students to gain international experience."
    ],
    "does thi offer online programs": [
        "Currently, THI offers limited online programs, primarily in postgraduate studies, but many programs are taught in person."
    ],
    "what is the workload like at thi": [
        "The workload at THI can be demanding, especially for engineering and computer science programs. Expect a mix of lectures, assignments, and exams."
    ],
    "can I work while studying at thi": [
        "Yes, international students can work part-time during their studies in Germany, up to 120 full days or 240 half days per year."
    ],
    "how can I get a part-time job in ingolstadt": [
        "You can find part-time jobs through university job portals, local businesses, or online job boards."
    ],
    "are there any student discounts available at thi": [
        "Yes, students at THI can access various discounts on transportation, shopping, and other services with their student ID."
    ],
    "is there a gym at thi": [
        "Yes, THI has a gym on campus where students can exercise and stay fit."
    ],
    "does thi have a student lounge": [
        "Yes, THI has student lounges where students can relax and study between classes."
    ],
    "what is the best way to get around ingolstadt": [
        "Ingolstadt has a well-developed public transport system, including buses and trains. Many students also use bicycles to get around the city."
    ],
    "can I bring my family to germany while studying at thi": [
        "Yes, international students can bring their spouse and children to Germany on a family reunion visa, but additional requirements must be met."
    ],
    "can I extend my student visa after graduation": [
        "Yes, you can extend your student visa after graduation if you are looking for a job in Germany. The visa extension allows you to stay for up to 18 months while seeking employment."
    ],
    "does thi have a buddy program": [
        "Yes, THI offers a buddy program that pairs international students with local students to help them adjust to life in Ingolstadt."
    ],
    "can I join clubs or societies at thi": [
        "Yes, THI has various student clubs and societies you can join, including cultural clubs, sports teams, and professional associations."
    ],
    "does thi have a career fair": [
        "Yes, THI organizes annual career fairs where students can meet potential employers and explore internship and job opportunities."
    ],
    "how do I get a transcript from thi": [
        "You can request a transcript from the THI student office or through their online portal."
    ],
    "how can I meet other students at thi": [
        "You can meet other students at THI through various events organized by the student union, clubs, and university activities."
    ],
    "does thi have a counseling service": [
        "Yes, THI offers counseling services to students who need support with personal, academic, or mental health issues."
    ],
    "is there a post-graduation employment rate for thi students": [
        "Yes, THI graduates have a high employment rate, especially in industries like engineering, IT, and business."
    ],
    "how can I find accommodation near thi": [
        "You can find accommodation near THI by searching on local housing platforms, student housing websites, or by contacting the THI housing office."
    ]
}

db_path = "chatbot.db"
last_scraped = None
website_content_cache = ""

# Initialize Database
def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                answer TEXT
            )
        ''')
        conn.commit()

# Scrape TH Ingolstadt website and return relevant content
def scrape_thi(query):
    global last_scraped, website_content_cache

    # Check if content is older than 24 hours
    if last_scraped and datetime.now() - last_scraped < timedelta(hours=24):
        return website_content_cache

    url = "https://www.thi.de"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        website_content_cache = response.text
        last_scraped = datetime.now()

        # Search for the query in the cached content
        if query.lower() in website_content_cache.lower():
            match = re.search(r'([^.]*?{}[^.]*\.)'.format(re.escape(query.lower())), website_content_cache.lower())
            if match:
                return match.group(0)

        return "Sorry, I could not find any relevant information on the website."

    except requests.RequestException as e:
        return f"Error fetching website data: {e}"

# Function to get a random response from predefined answers
def get_random_response(query):
    if query.lower() in predefined_answers:
        return random.choice(predefined_answers[query.lower()])
    return "Sorry, I don't have an answer for that."

# Ask chatbot API
@app.get("/ask")
def ask_chatbot(query: str):
    # First check for predefined answers
    response = get_random_response(query)
    if response != "Sorry, I don't have an answer for that.":
        return {"response": response}

    # If no predefined answer, scrape the website content
    website_response = scrape_thi(query)
    return {"response": website_response}

# Add Manual Q&A API
@app.post("/add_qa")
def add_qa(question: str, answer: str):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO faq (question, answer) VALUES (?, ?)", (question, answer))
            conn.commit()
            return {"message": "Q&A added successfully."}
        except sqlite3.IntegrityError:
            return {"error": "This question already exists."}
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

# Initialize the database when the app starts
@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)







