# -*- coding: utf-8 -*-
import random
from core.database import DICTIONARY, user_sessions

class QuizManager:
    def __init__(self):
        self.questions = list(DICTIONARY.items())
        random.shuffle(self.questions)
    
    def get_question(self, user_id):
        """Возвращает случайный вопрос"""
        if user_id not in user_sessions:
            user_sessions[user_id] = {"quiz_score": 0, "quiz_questions": 0}
        
        if not self.questions:
            self.questions = list(DICTIONARY.items())
            random.shuffle(self.questions)
        
        if self.questions:
            slang, normal = self.questions.pop()
            return {
                "question": f"Что означает <b>'{slang}'</b>?",
                "correct": normal,
                "options": self.generate_options(normal)
            }
        return None
    
    def generate_options(self, correct_answer):
        """Генерирует варианты ответов"""
        options = [correct_answer]
        other_words = random.sample(list(DICTIONARY.values()), min(3, len(DICTIONARY)))
        options.extend([w for w in other_words if w != correct_answer][:3])
        random.shuffle(options)
        return options
    
    def update_quiz_stats(self, user_id, is_correct):
        """Обновляет статистику викторины"""
        if user_id not in user_sessions:
            user_sessions[user_id] = {"quiz_score": 0, "quiz_questions": 0}
        
        user_sessions[user_id]["quiz_questions"] += 1
        if is_correct:
            user_sessions[user_id]["quiz_score"] += 1

# Глобальный экземпляр менеджера викторины
quiz_manager = QuizManager()