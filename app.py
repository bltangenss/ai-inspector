import os
import threading
from flask import Flask
from routes.main_routes import main_bp
from routes.api_routes import api_bp
from routes.image_routes import image_bp
from models.database import init_db
from models.image_model import load_image_model
import logging


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    app.config['UPLOAD_FOLDER'] = 'uploads'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp,    url_prefix='/api')
    app.register_blueprint(image_bp,  url_prefix='/api/image')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.info("AI Inspector запущен")
    return app


if __name__ == '__main__':
    app = create_app()
    init_db()

    # Загружаем модель в фоновом потоке, чтобы не блокировать запуск сервера
    threading.Thread(target=load_image_model, daemon=True).start()

    base = os.path.dirname(os.path.abspath(__file__))
    print("=" * 55)
    print(f"  Папка проекта: {base}")
    print("-" * 55)
    print("  GET  /                   — главная страница")
    print("  POST /api/image/analyze  — анализ изображения")
    print("  GET  /api/image/status   — статус модели")
    print("  GET  /api/history        — история анализов")
    print("=" * 55)
    print("  Модель: umm-maybe/AI-image-detector (ViT)")
    print("  При первом запуске модель скачается (~350 МБ)")
    print("=" * 55)

    app.run(debug=False, host='0.0.0.0', port=5000)
