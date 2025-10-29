# core/database.py - минимальный файл
user_modes = {}
user_stats = {}
user_sessions = {}
DICTIONARY = {}

def load_dictionary():
    return True

def get_top_words():
    return [
        ("кринж", "стыд"), ("краш", "влюбленность"), ("рофл", "шутка"),
        ("агриться", "злиться"), ("чилить", "отдыхать"), ("вайб", "атмосфера"),
        ("имба", "круто"), ("го", "давай"), ("пруф", "доказательство")
    ]

def search_words(query):
    return []