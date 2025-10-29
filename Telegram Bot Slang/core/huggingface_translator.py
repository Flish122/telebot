# -*- coding: utf-8 -*-
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class YandexTranslator:
    def __init__(self):
        self.api_key = os.getenv("YANDEX_API_KEY")
        self.folder_id = os.getenv("YANDEX_FOLDER_ID")
        logger.info("🔧 Используем Yandex Translate API")
        
    def translate_with_ai(self, text, direction):
        """Перевод через Yandex API - РЕАЛЬНО РАБОТАЕТ"""
        if not self.api_key or not self.folder_id:
            return f"{text} ⚠️ (настрой API ключи)"
        
        try:
            # Yandex сам определяет язык и переводит
            target_lang = "ru"  # Оставляем русский, но меняем стиль
            
            url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Api-Key {self.api_key}"
            }
            
            data = {
                "texts": [text],
                "targetLanguageCode": target_lang,
                "folderId": self.folder_id,
                "speller": True,  # Исправляет опечатки
                "format": "PLAIN_TEXT"
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                translated = response.json()['translations'][0]['text']
                
                # Для сленга → нормальный добавляем небольшую обработку
                if direction == "slang_to_normal":
                    translated = self._make_more_formal(translated)
                else:
                    translated = self._make_more_slang(translated)
                    
                return translated
            else:
                logger.error(f"❌ API ошибка: {response.status_code}")
                return f"{text} ⚠️ (ошибка API)"
                
        except Exception as e:
            logger.error(f"❌ Ошибка Yandex API: {e}")
            return f"{text} ⚠️ (ошибка сети)"
    
    def _make_more_formal(self, text):
        """Делает текст более формальным (доп обработка)"""
        informal_to_formal = {
            "здарова": "привет", "ку": "привет", "хай": "привет",
            "го": "давай", "спс": "спасибо", "пасиб": "спасибо",
            "пж": "пожалуйста", "ок": "хорошо", "норм": "нормально",
            "щас": "сейчас", "чел": "человек", "офк": "конечно"
        }
        
        result = text.lower()
        for informal, formal in informal_to_formal.items():
            if informal in result:
                result = result.replace(informal, formal)
        
        # Восстанавливаем регистр
        if text and text[0].isupper():
            result = result.capitalize()
            
        return result
    
    def _make_more_slang(self, text):
        """Делает текст более неформальным (доп обработка)"""
        formal_to_informal = {
            "привет": "здарова", "давай": "го", "спасибо": "спс",
            "пожалуйста": "пж", "хорошо": "ок", "нормально": "норм",
            "сейчас": "щас", "человек": "чел", "конечно": "офк"
        }
        
        result = text.lower()
        for formal, informal in formal_to_informal.items():
            if formal in result:
                result = result.replace(formal, informal)
        
        if text and text[0].isupper():
            result = result.capitalize()
            
        return result

# Используем Yandex API
hf_translator = YandexTranslator()