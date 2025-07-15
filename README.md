# AI Web Analysis

Веб-приложение для автоматической генерации рекламных постов на основе анализа веб-страниц с использованием OpenAI API. Приложение использует "агентский" подход, где несколько промптов анализируют разные аспекты контента для создания комплексного результата.

## Технологии

- Python 3.10
- Flask
- OpenAI API (gpt-4.1-nano)
- Beautiful Soup 4

## Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/ai4bordon/aI_web_analysis.git
    cd aI_web_analysis
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    # Для Windows
    python -m venv venv
    venv\Scripts\activate
    
    # Для Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте переменные окружения:**
    Создайте файл `.env` в корне проекта и добавьте в него ваш API-ключ от OpenAI:
    ```
    OPENAI_API_KEY='ваш_ключ_здесь'
    ```

5.  **Запустите приложение:**
    ```bash
    python run.py
    ```
    Приложение будет доступно по адресу `http://localhost:5000`.

## Запуск с помощью Docker

1.  **Соберите Docker-образ:**
    ```bash
    docker build -t ai-web-analysis .
    ```

2.  **Запустите контейнер:**
    Не забудьте подставить свой `OPENAI_API_KEY`.
    ```bash
    docker run -p 5000:5000 -e OPENAI_API_KEY='ваш_ключ_здесь' ai-web-analysis
    ```

## Развертывание на Docker Hub

1.  **Войдите в Docker Hub:**
    ```bash
    docker login
    ```

2.  **Присвойте тег образу:**
    Замените `your-username` на ваш логин в Docker Hub.
    ```bash
    docker tag ai-web-analysis your-username/ai-web-analysis:latest
    ```

3.  **Загрузите образ:**
    ```bash
    docker push your-username/ai-web-analysis:latest
    ```

## Как использовать

1.  Откройте `http://localhost:5000` в вашем браузере.
2.  Введите URL сайта, который вы хотите проанализировать.
3.  Нажмите кнопку "Анализировать".
4.  Ниже на странице появятся результаты анализа и готовый рекламный пост.
