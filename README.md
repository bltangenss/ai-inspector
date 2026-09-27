# AI Инспектор

Веб-приложение, которое оценивает, было ли изображение создано искусственным интеллектом или является реальной фотографией.

Приложение использует модель [`umm-maybe/AI-image-detector`](https://huggingface.co/umm-maybe/AI-image-detector) на базе ViT. Результат содержит вероятности двух классов, текстовый вердикт и уровень уверенности. История проверок сохраняется локально в SQLite.

> Результат классификации является вероятностной оценкой, а не доказательством происхождения изображения.

## Возможности

- загрузка изображения через выбор файла или drag-and-drop;
- поддержка PNG, JPG, JPEG, WebP, GIF и BMP;
- оценка вероятности классов «ИИ» и «реальное»;
- отображение уровня уверенности модели;
- API для анализа, статуса модели и истории проверок;
- локальный запуск или запуск через Docker.

## Быстрый запуск

Требуется Python 3.10 или новее.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Linux и macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

После запуска откройте <http://localhost:5000>.

При первом запуске модель загружается с Hugging Face. Для этого требуется подключение к интернету; размер загрузки составляет примерно 350 МБ.

## Запуск через Docker

```bash
docker compose up --build
```

Приложение будет доступно по адресу <http://localhost:5000>.

Для рабочего окружения задайте собственный секретный ключ:

```bash
SECRET_KEY=replace-with-a-random-secret docker compose up --build
```

## API

| Метод | Маршрут | Назначение |
| --- | --- | --- |
| `GET` | `/` | Веб-интерфейс |
| `POST` | `/api/image/analyze` | Анализ файла из поля формы `image` |
| `GET` | `/api/image/status` | Состояние модели |
| `GET` | `/api/history` | Последние 50 результатов |

Пример запроса:

```bash
curl -X POST -F "image=@photo.jpg" http://localhost:5000/api/image/analyze
```

## Структура

```text
ai_inspector/
├── app.py                 # создание и запуск Flask-приложения
├── models/
│   ├── database.py        # SQLite и история анализов
│   └── image_model.py     # загрузка модели и классификация
├── routes/                # страницы и REST API
├── static/                # иконка и PWA-манифест
├── templates/index.html   # веб-интерфейс
├── Dockerfile
└── docker-compose.yml
```

Локальная база `inspector.db`, загруженные файлы, виртуальные окружения и секреты не включаются в Git.
