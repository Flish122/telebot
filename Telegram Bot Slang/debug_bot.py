# -*- coding: utf-8 -*-
import json
import os
import sys

print("🔍 ДИАГНОСТИКА БОТА")
print("=" * 50)

# 1. Проверяем структуру проекта
print("📁 СТРУКТУРА ПРОЕКТА:")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(BASE_DIR):
    level = root.replace(BASE_DIR, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py') or file.endswith('.json'):
            print(f'{subindent}{file}')

print("\n" + "=" * 50)

# 2. Проверяем пути
print("📍 ПРОВЕРКА ПУТЕЙ:")
DICTIONARY_PATH = os.path.join(BASE_DIR, "data", "slang_dictionary.json")
print(f"Ожидаемый путь: {DICTIONARY_PATH}")
print(f"Файл существует: {os.path.exists(DICTIONARY_PATH)}")

# 3. Ищем словарь
print("\n🔍 ПОИСК СЛОВАРЯ:")
found_dicts = []
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if 'dictionary' in file.lower() and file.endswith('.json'):
            full_path = os.path.join(root, file)
            found_dicts.append(full_path)
            print(f"Найден: {full_path}")

if found_dicts:
    # Берем первый найденный словарь
    ACTUAL_DICT_PATH = found_dicts[0]
    print(f"\n✅ Используем словарь: {ACTUAL_DICT_PATH}")
else:
    print("❌ Словарь не найден!")
    sys.exit(1)

# 4. Проверяем содержимое словаря
print("\n📖 ПРОВЕРКА СОДЕРЖИМОГО СЛОВАРЯ:")
try:
    with open(ACTUAL_DICT_PATH, "r", encoding="utf-8") as f:
        dictionary_data = json.load(f)
    
    print(f"✅ Словарь загружен: {len(dictionary_data)} слов")
    print("Примеры слов:")
    for i, (key, value) in enumerate(list(dictionary_data.items())[:10]):
        print(f"  {i+1}. '{key}' → '{value}'")
        
except Exception as e:
    print(f"❌ Ошибка загрузки: {e}")

# 5. Тестируем функцию перевода
print("\n🧪 ТЕСТ ПЕРЕВОДА:")
def test_translate(text, mode):
    """Тестовая функция перевода"""
    words_found = []
    
    if mode == "slang_to_normal":
        for slang, normal in dictionary_data.items():
            if slang in text.lower():
                words_found.append((slang, normal))
                text = text.replace(slang, f"**{normal}**")
    
    return text, len(words_found) > 0, words_found

# Тестовые фразы
test_phrases = ["го", "кринж", "агриться", "привет"]
for phrase in test_phrases:
    translated, found, words = test_translate(phrase, "slang_to_normal")
    status = "✅ НАЙДЕНО" if found else "❌ НЕ НАЙДЕНО"
    print(f"{status} '{phrase}' → {translated}")
    if words:
        print(f"   Найдены слова: {words}")

print("\n" + "=" * 50)
print("🎯 ДИАГНОСТИКА ЗАВЕРШЕНА")