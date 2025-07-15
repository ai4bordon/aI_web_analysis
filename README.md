# AI Ad Generator

Веб-приложение для автоматической генерации рекламных постов на основе анализа веб-страниц с использованием OpenAI API.

## Возможности

- 🔍 Анализ контента веб-страниц
- 🎯 Определение целевой аудитории
- 💡 Выявление уникальных преимуществ
- 📊 Анализ конкурентных преимуществ
- ✨ Генерация структурированных рекламных постов

## Технологии

- Python 3.12
- Flask
- OpenAI API
- Beautiful Soup 4
- Docker

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/ai-ad-generator.git
cd ai-ad-generator
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate     # Для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env:
```bash
OPENAI_API_KEY=your_api_key_here
PORT=5000
```

5. Запустите приложение:
```bash
python run.py
```

### Docker

1. Соберите образ:
```bash
docker build -t ai-ad-generator .
```

2. Запустите контейнер:
```bash
docker run -p 5000:5000 -e OPENAI_API_KEY=your_api_key_here ai-ad-generator
```

## Использование

1. Откройте браузер и перейдите по адресу `http://localhost:5000`
2. Введите URL страницы для анализа
3. Дождитесь результатов анализа и сгенерированного рекламного поста

## API Endpoints

- `GET /` - Главная страница
- `POST /` - Анализ URL и генерация рекламного поста

## Структура проекта

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── openai_module.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
├── Dockerfile
├── requirements.txt
├── run.py
└── README.md
```

## Развертывание

### DockerHub

1. Войдите в DockerHub:
```bash
docker login
```

2. Пометьте образ:
```bash
docker tag ai-ad-generator yourusername/ai-ad-generator:latest
```

3. Отправьте образ:
```bash
docker push yourusername/ai-ad-generator:latest
```

## Лицензия

MIT

## Автор

Ваше имя
