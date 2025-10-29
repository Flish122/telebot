# -*- coding: utf-8 -*-
from config.config import EMOJI

# Временный словарь вместо импорта из database
DICTIONARY = {
    "го": "давай", "кринж": "стыд", "рофл": "шутка",
    "краш": "влюбленность", "агриться": "злиться",
    "чилить": "отдыхать", "вайб": "атмосфера",
    "имба": "круто", "пруф": "доказательство",
    "видос": "видео", "чел": "человек", "офк": "конечно"
}

def format_welcome():
    return f"""
{EMOJI['wave']} <b>ПРИВЕТСТВУЕМ В НЕЙРО-ПЕРЕВОДЧИКЕ!</b> {EMOJI['ai']}

{EMOJI['rocket']} <b>Умные возможности:</b>
• 🤖 Локальная нейросеть Hugging Face
• 🧠 Модель RUT5 для перефразирования  
• ⚡ Работает без интернета
• 💰 Полностью бесплатно

{EMOJI['cloud']} <b>Технологии:</b>
• Transformers от Hugging Face
• Модель: cointegrated/rut5-base-paraphraser
• Локальная обработка на вашем ПК

{EMOJI['bulb']} <b>Просто отправь фразу!</b>

<b>Выбери действие:</b>
"""

def format_translation_result(original, translated, mode, words_found):
    direction_emoji = EMOJI['slang'] if mode == "slang_to_normal" else EMOJI['normal']
    direction_text = "сленг → нормальный" if mode == "slang_to_normal" else "нормальный → сленг"
    
    words_info = ""
    if words_found:
        words_info = f"\n{EMOJI['mag']} <b>Найдено слов:</b> {len(words_found)}\n"
        for i, (orig, trans) in enumerate(words_found[:3]):
            words_info += f"• <code>{orig}</code> → <b>{trans}</b>\n"
    
    return f"""
{direction_emoji} <b>УСПЕШНЫЙ ПЕРЕВОД!</b> {EMOJI['tada']}

📝 <b>Исходный текст:</b>
<code>{original}</code>

🔄 <b>Результат:</b>
{translated}
{words_info}
💫 <i>Режим: {direction_text}</i>
"""

def format_no_translation(original, word_count):
    return f"""
{EMOJI['bulb']} <b>СОВЕТ ДЛЯ ПЕРЕВОДА</b>

📝 <b>Ваш текст:</b>
<code>{original}</code>

❌ <b>Не удалось найти сленговые слова</b>

💡 <b>Попробуй:</b>
• Использовать популярные слова
• Проверить написание
• Воспользоваться поиском

📚 <b>Доступно слов:</b> {word_count}
"""

def format_stats(stats):
    if not stats:
        return f"{EMOJI['stats']} <b>Статистика пуста</b>\n\nНачни использовать бота чтобы увидеть статистику! {EMOJI['rocket']}"
    
    return f"""
{EMOJI['chart']} <b>ВАША СТАТИСТИКА</b> {EMOJI['chart']}

{EMOJI['translate']} <b>Переводы:</b> {stats.get('total_translations', 0)}
{EMOJI['fire']} <b>Слов переведено:</b> {stats.get('words_translated', 0)}

{EMOJI['slang']} <b>Сленг → Норма:</b> {stats.get('slang_to_normal', 0)}
{EMOJI['normal']} <b>Норма → Сленг:</b> {stats.get('normal_to_slang', 0)}

{EMOJI['time']} <b>Активен с:</b> {stats.get('first_use', 'сегодня')}
"""

def format_help():
    return f"""
{EMOJI['help']} <b>ПОЛНОЕ РУКОВОДСТВО</b> {EMOJI['brain']}

{EMOJI['zap']} <b>Основные команды:</b>
/start - главное меню
/stats - ваша статистика
/quiz - начать викторину

{EMOJI['fire']} <b>Режимы перевода:</b>
• <b>Сленг → Норма</b> - переводит сленг на обычный язык
• <b>Норма → Сленг</b> - переводит обычную речь в сленг

{EMOJI['star']} <b>Дополнительные функции:</b>
• <b>Поиск</b> - найти слово в словаре
• <b>Словарь</b> - случайные слова
• <b>Статистика</b> - ваша активность
• <b>Топ слов</b> - популярные слова
• <b>Викторина</b> - проверить знания

{EMOJI['bulb']} <b>Нейросеть понимает разные формы слов!</b>
<code>Я испытываю кринж</code> → "Я испытываю <b>стыд</b>"
<code>От этого кринжа</code> → "От этого <b>стыда</b>"
<code>Не агрись по пустякам</code> → "Не <b>злись</b> по пустякам"
<code>Он агрится на всех</code> → "Он <b>злится</b> на всех"

{EMOJI['flash']} <b>Примеры для теста:</b>
<code>Этот видос просто кринж</code>
<code>Не агрись по пустякам</code>  
<code>Го играть в игры</code>
"""