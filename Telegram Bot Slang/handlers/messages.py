# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from core.huggingface_translator import hf_translator
from config.keyboards import get_main_keyboard, get_back_keyboard
from utils.formatters import format_welcome, format_help
from config.config import EMOJI

# Импортируем глобальные переменные через функцию
def get_global_vars():
    from main import user_modes, user_stats, user_sessions
    return user_modes, user_stats, user_sessions

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = format_welcome()
    await update.message.reply_text(
        welcome_text, 
        reply_markup=get_main_keyboard(),
        parse_mode='HTML'
    )

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = format_help()
    await update.message.reply_text(
        help_text,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )

async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    user_modes, user_stats, user_sessions = get_global_vars()
    user_id = update.message.from_user.id
    
    if user_id not in user_stats:
        stats_text = f"{EMOJI['stats']} <b>Статистика пуста</b>\n\nНачни использовать бота чтобы увидеть статистику! {EMOJI['rocket']}"
    else:
        stats = user_stats[user_id]
        stats_text = f"""
{EMOJI['chart']} <b>ВАША СТАТИСТИКА</b> {EMOJI['chart']}

{EMOJI['translate']} <b>Переводы:</b> {stats.get('total_translations', 0)}
{EMOJI['fire']} <b>Слов переведено:</b> {stats.get('words_translated', 0)}

{EMOJI['slang']} <b>Сленг → Норма:</b> {stats.get('slang_to_normal', 0)}
{EMOJI['normal']} <b>Норма → Сленг:</b> {stats.get('normal_to_slang', 0)}

{EMOJI['time']} <b>Активен с:</b> {stats.get('first_use', 'сегодня')}
"""
    
    await update.message.reply_text(
        stats_text,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )

async def handle_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускает викторину"""
    from config.keyboards import get_quiz_keyboard
    quiz_text = f"""
{EMOJI['brain']} <b>ВИКТОРИНА ПО СЛЕНГУ</b> {EMOJI['tada']}

🎯 <b>Проверь свои знания!</b>
• Угадай значение сленговых слов
• 10 случайных вопросов  
• Следи за своей точностью

{EMOJI['star']} <b>Готов начать?</b>
"""
    await update.message.reply_text(
        quiz_text,
        reply_markup=get_quiz_keyboard(),
        parse_mode='HTML'
    )

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает поиск слов"""
    query = update.message.text
    search_result = f"{EMOJI['mag']} <b>ПОИСК: '{query}'</b>\n\n"
    search_result += "🔍 Нейросеть работает в режиме перевода\n"
    search_result += "💡 Просто отправь фразу для перевода!"
    
    await update.message.reply_text(
        search_result,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )

async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает перевод текста с помощью нейросети"""
    user_modes, user_stats, user_sessions = get_global_vars()
    user_id = update.message.from_user.id
    text = update.message.text
    
    if user_id not in user_modes:
        await update.message.reply_text(
            f"{EMOJI['bulb']} <b>СНАЧАЛА ВЫБЕРИ РЕЖИМ!</b>\n\nИспользуй кнопки ниже для выбора режима перевода {EMOJI['zap']}",
            parse_mode='HTML'
        )
        return

    mode = user_modes[user_id]
    
    # Показываем что обрабатываем
    processing_msg = await update.message.reply_text(f"{EMOJI['brain']} Нейросеть обрабатывает запрос...")
    
    # Переводим с помощью Hugging Face
    translated_text = hf_translator.translate_with_ai(text, mode)
    
    # Обновляем статистику
    from main import update_stats
    update_stats(user_id, mode, 1)
    
    # Формируем ответ
    direction_emoji = EMOJI['slang'] if mode == "slang_to_normal" else EMOJI['normal']
    direction_text = "сленг → нормальный" if mode == "slang_to_normal" else "нормальный → сленг"
    
    response = f"""
{direction_emoji} <b>НЕЙРО-ПЕРЕВОД</b> {EMOJI['robot']}

📝 <b>Исходный текст:</b>
<code>{text}</code>

🔄 <b>Результат:</b>
<code>{translated_text}</code>

💫 <i>Режим: {direction_text}</i>
<i>Используется: Hugging Face (RUT5)</i>
"""
    
    # Удаляем сообщение "Обрабатываю" и отправляем результат
    await processing_msg.delete()
    await update.message.reply_text(
        response,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )

async def handle_random_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает возможности нейросети"""
    examples_text = f"""
{EMOJI['brain']} <b>ПРИМЕРЫ ДЛЯ НЕЙРОСЕТИ</b>

🤖 <b>Бот использует Hugging Face для умного перевода</b>

{EMOJI['flash']} <b>Примеры запросов:</b>
• <code>Этот видос просто кринжовый</code>
• <code>Го в дискорд чилить</code>  
• <code>У нас тут имбовый вайб</code>
• <code>Не агрись по пустякам</code>

{EMOJI['zap']} <b>Нейросеть умеет:</b>
• Понимать контекст
• Работать с любыми словами
• Сохранять смысл предложений
• Адаптировать стиль речи
"""
    await update.message.reply_text(
        examples_text,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )

async def handle_top_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает популярные запросы"""
    popular_text = f"""
{EMOJI['crown']} <b>ПОПУЛЯРНЫЕ ЗАПРОСЫ</b>

{EMOJI['fire']} <b>Часто переводят:</b>
• Кринж, рофл, краш
• Агриться, чилить, флексить  
• Вайб, имба, пруф
• Го, видос, чел

{EMOJI['bulb']} <b>Нейросеть понимает:</b>
• Любые сленговые выражения
• Контекстные фразы
• Сложные предложения
• Даже новые слова!
"""
    await update.message.reply_text(
        popular_text,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )

def register_handlers(application):
    """Регистрирует все обработчики сообщений"""
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("stats", handle_stats))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(CommandHandler("quiz", handle_quiz))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_translation))