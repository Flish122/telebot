# -*- coding: utf-8 -*-
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config.config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные
user_modes = {}
user_stats = {}
user_sessions = {}

def update_stats(user_id, direction, words_used=1):
    """Обновляет статистику пользователя"""
    from datetime import datetime
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            "slang_to_normal": 0,
            "normal_to_slang": 0,
            "total_translations": 0,
            "words_translated": 0,
            "first_use": datetime.now().isoformat()[:10]
        }
    
    stats = user_stats[user_id]
    stats[direction] = stats.get(direction, 0) + 1
    stats["total_translations"] = stats.get("total_translations", 0) + 1
    stats["words_translated"] = stats.get("words_translated", 0) + words_used

def main():
    """Главная функция бота"""
    print("🚀 НЕЙРО-БОТ ЗАПУЩЕН!")
    print("💫 Используется Hugging Face RUT5 модель")
    
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Импортируем здесь чтобы избежать циклических импортов
        from handlers.messages import register_handlers
        from handlers.callbacks import register_callbacks
        
        # Регистрируем обработчики
        register_handlers(application)
        register_callbacks(application)
        
        # Запускаем бота
        print("✅ Бот запущен и готов к работе!")
        application.run_polling(
            poll_interval=3.0,
            timeout=30,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()