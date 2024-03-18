# Приложение для консультации по маркетплейсу daribar.kz

Приложение с использованием FastAPI и OpenAI GPT-4 
для обработки запросов пользователей и предоставления информации по услугам маркетплейса daribar.kz.

## Установка

Для запуска приложения вам понадобится Python 3.8 или выше. 
Следуйте этим шагам для установки и запуска приложения:

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ValentinKim531/GPT4_call_center_chat_helper.git
```

2. Перейдите в каталог проекта:
```bash
cd <название вашего проекта>
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Для использования API OpenAI вам необходимо установить 
переменную окружения OPENAI_API_KEY со своим ключом API. 
Для этого вы можете искользовать файл `.env.example` (необходимо переименовать файл в `.env`).

## Запуск приложения

1. Запустите сервер FastAPI:

```bash
uvicorn app:app --reload
```
После этого приложение будет доступно по адресу `http://127.0.0.1:8000/docs`



## Работа с приложением

1. Загрузка текстового файла c информацией, 
необходимой для предоставления ответов пользователю:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload-text-file/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'text_file=@path/to/your/file.txt;type=text/plain'
```

2. Направление запроса (вопроса пользователя):
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/ask-question/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"question":"<ваш вопрос здесь>"}'
```

Ответ будет возвращен в формате JSON с ключом `answer`.





























