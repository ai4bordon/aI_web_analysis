import os
import requests
from bs4 import BeautifulSoup
import openai
from typing import List, Dict
import re

class OpenAIClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API ключ OpenAI не предоставлен")
        self.client = openai.OpenAI(api_key=api_key)

    def _get_text_from_url(self, url: str) -> str:
        """Получает и очищает текстовый контент со страницы"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text = re.sub(r'[^\x20-\x7E\n\r\t\u0400-\u04FF]+', ' ', text)
            
            return text[:4000]
        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении контента: {str(e)}")

    def _call_openai_api(self, system_prompt: str, user_content: str) -> str:
        """Выполняет запрос к OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Ошибка при вызове OpenAI API: {str(e)}")

    def generate_future_prompts_from_url(self, url: str) -> Dict[str, List[str]]:
        """Генерирует набор системных промптов для анализа контента"""
        text = self._get_text_from_url(url)
        
        system_prompt = """Ты создаёшь цепочку агентов для анализа сайта и генерации рекламы.
        
        Создай 5-6 специализированных системных промптов, каждый из которых будет анализировать отдельный аспект:
        - Целевая аудитория и её потребности
        - Уникальные преимущества продукта/услуги
        - Эмоциональные триггеры и мотивация
        - Конкурентные преимущества
        - Ценностное предложение
        
        Для каждого промпта:
        1. Укажи роль агента (например: "Ты эксперт по анализу целевой аудитории...")
        2. Добавь 2-3 конкретные задачи
        3. Укажи формат вывода
        
        Верни список в формате:
        [РОЛЬ #1]
        • Основная задача
        • Что нужно проанализировать
        • Как представить результат
        
        [РОЛЬ #2]
        ...и так далее"""
        
        result = self._call_openai_api(system_prompt, text)
        
        # Разбиваем результат на отдельные промпты
        sections = result.split('[РОЛЬ')
        prompts = []
        
        for section in sections:
            if section.strip():
                # Если секция начинается с #, добавляем [РОЛЬ обратно
                if section.strip().startswith('#'):
                    section = '[РОЛЬ' + section
                prompts.append(section.strip())
        
        return {"prompts": prompts}

    def query_with_custom_system_prompt(self, prompt: str, content: str) -> str:
        """Выполняет запрос с пользовательским системным промптом"""
        return self._call_openai_api(prompt, content)

    def generate_final_ad_post(self, all_results: List[str]) -> str:
        """Генерирует финальный рекламный пост на основе результатов анализа"""
        content = "\n\n".join(all_results)
        
        system_prompt = """Ты опытный копирайтер. Твоя задача - создать рекламный пост, 
        строго следуя структуре и используя предоставленные результаты анализа. 
        Начинай сразу с заголовка, без вступительных слов и фраз вроде "Конечно" или "Хорошо".

        Обязательная структура поста:

        [ЗАГОЛОВОК]
        ⚡ Сразу начни с яркого заголовка
        ⚡ Используй главную выгоду или интригу
        ⚡ Добавь эмоциональный триггер

        [ОСНОВНОЙ ТЕКСТ]
        ⚡ 3-4 коротких параграфа
        ⚡ В каждом параграфе - одна ключевая мысль
        ⚡ Используй маркированные списки для преимуществ
        ⚡ Добавь эмодзи как разделители

        [ПРИЗЫВ К ДЕЙСТВИЮ]
        ⚡ Четкий призыв к действию
        ⚡ Элемент срочности
        ⚡ Конкретный следующий шаг

        [ХЕШТЕГИ]
        ⚡ 3-5 релевантных хештегов

        ВАЖНО: 
        1. Начинай сразу с заголовка
        2. Не используй вступительные фразы
        3. Пиши кратко и по делу
        4. Разделяй блоки пустой строкой"""
        
        return self._call_openai_api(system_prompt, content)
