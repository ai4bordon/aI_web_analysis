import os
from flask import render_template, request, session
from app import app
from app.openai_module import OpenAIClient
from markupsafe import Markup

# Добавляем фильтр для преобразования переносов строк в <br>
@app.template_filter('nl2br')
def nl2br(value):
    if not value:
        return ""
    return Markup(value.replace('\n', '<br>\n'))

# Инициализация сессии
app.secret_key = os.urandom(24)

# Получаем ключ API из переменных окружения
api_key = os.environ.get('OPENAI_API_KEY')

# Создаем экземпляр клиента
try:
    client = OpenAIClient(api_key=api_key)
except ValueError as e:
    client = None
    startup_error = str(e)
    print(f"ОШИБКА ПРИ ЗАПУСКЕ: {startup_error}")

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    prompts = None
    analysis_results = None
    final_post = None

    if not client:
        error = startup_error
        return render_template('index.html', error=error)

    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            error = "Пожалуйста, введите URL."
        else:
            try:
                # Шаг 1: Получаем список промптов
                prompts_data = client.generate_future_prompts_from_url(url)
                prompts = prompts_data["prompts"]
                
                # Шаг 2: Получаем текст с URL для анализа
                page_text = client._get_text_from_url(url)
                
                # Шаг 3: Анализируем контент с каждым промптом
                analysis_results = []
                for prompt in prompts:
                    result = client.query_with_custom_system_prompt(prompt, page_text)
                    analysis_results.append(result)
                
                # Шаг 4: Генерируем финальный пост
                final_post = client.generate_final_ad_post(analysis_results)
                
                # Сохраняем результаты в сессии
                session['prompts'] = prompts
                session['analysis_results'] = analysis_results
                session['final_post'] = final_post
                
            except Exception as e:
                print(f"Произошла ошибка при анализе: {e}")
                error = f"Не удалось выполнить анализ. Ошибка: {e}"
    else:
        # Получаем сохраненные результаты из сессии
        prompts = session.get('prompts')
        analysis_results = session.get('analysis_results')
        final_post = session.get('final_post')
    
    return render_template('index.html', 
                         error=error,
                         prompts=prompts,
                         analysis_results=analysis_results,
                         final_post=final_post)