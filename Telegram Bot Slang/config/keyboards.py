# -*- coding: utf-8 -*-
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import EMOJI

def get_main_keyboard():
    """Главная клавиатура меню"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['slang']} Сленг → Норма", callback_data="slang_to_normal"),
            InlineKeyboardButton(f"{EMOJI['normal']} Норма → Сленг", callback_data="normal_to_slang")
        ],
        [
            InlineKeyboardButton(f"{EMOJI['search']} Поиск", callback_data="search_word"),
            InlineKeyboardButton(f"{EMOJI['stats']} Статистика", callback_data="stats")
        ],
        [
            InlineKeyboardButton(f"{EMOJI['book']} Словарь", callback_data="random_words"),  # ИСПРАВИЛ 'words' на 'book'
            InlineKeyboardButton(f"{EMOJI['crown']} Топ слов", callback_data="top_words")
        ],
        [
            InlineKeyboardButton(f"{EMOJI['dice']} Викторина", callback_data="quiz"),  # ИСПРАВИЛ 'brain' на 'dice'
            InlineKeyboardButton(f"{EMOJI['help']} Помощь", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Клавиатура с кнопкой Назад"""
    keyboard = [
        [InlineKeyboardButton(f"{EMOJI['zap']} Назад в меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quiz_keyboard():
    """Клавиатура для викторины"""
    keyboard = [
        [
            InlineKeyboardButton("Начать викторину", callback_data="start_quiz"),
            InlineKeyboardButton(f"{EMOJI['zap']} Назад", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_mode_keyboard():
    """Клавиатура выбора режима"""
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJI['slang']} Сленг → Норма", callback_data="slang_to_normal"),
            InlineKeyboardButton(f"{EMOJI['normal']} Норма → Сленг", callback_data="normal_to_slang")
        ],
        [InlineKeyboardButton(f"{EMOJI['zap']} Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)