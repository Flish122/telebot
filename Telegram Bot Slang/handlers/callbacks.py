# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from config.keyboards import get_main_keyboard, get_back_keyboard
from config.config import EMOJI

def get_global_vars():
    from main import user_modes, user_sessions
    return user_modes, user_sessions

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает callback запросы"""
    query = update.callback_query
    await query.answer()
    
    user_modes, user_sessions = get_global_vars()
    user_id = query.from_user.id
    data = query.data

    if data == "back_to_main":
        from handlers.messages import handle_start
        await handle_start(update, context)
    
    elif data in ["slang_to_normal", "normal_to_slang"]:
        # Сохраняем режим
        user_modes[user_id] = data
        user_sessions[user_id] = None
        
        mode_text = "сленг → нормальный" if data == "slang_to_normal" else "нормальный → сленг"
        
        await query.edit_message_text(
            f"{EMOJI['zap']} <b>РЕЖИМ АКТИВИРОВАН:</b> {mode_text}\n\nОтправь текст для перевода! {EMOJI['rocket']}",
            reply_markup=get_back_keyboard(),
            parse_mode='HTML'
        )
    
    elif data == "search_word":
        user_sessions[user_id] = "searching"
        await query.edit_message_text(
            f"{EMOJI['search']} <b>РЕЖИМ ПОИСКА</b>\n\nВведи слово для поиска в словаре:",
            reply_markup=get_back_keyboard(),
            parse_mode='HTML'
        )
    
    elif data == "stats":
        from handlers.messages import handle_stats
        await handle_stats(update, context)
    
    elif data == "random_words":
        from handlers.messages import handle_random_words
        await handle_random_words(update, context)
    
    elif data == "top_words":
        from handlers.messages import handle_top_words
        await handle_top_words(update, context)
    
    elif data == "quiz":
        from handlers.messages import handle_quiz
        await handle_quiz(update, context)
    
    elif data == "help":
        from handlers.messages import handle_help
        await handle_help(update, context)

def register_callbacks(application):
    """Регистрирует обработчики callback'ов"""
    application.add_handler(CallbackQueryHandler(handle_callback))