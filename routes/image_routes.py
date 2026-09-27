import os
import logging
from flask import Blueprint, request, jsonify
from models.image_model import analyze_image, get_model_status
from models.database import save_analysis

logger = logging.getLogger(__name__)
image_bp = Blueprint("image", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif", "bmp"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@image_bp.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "Файл не передан. Используйте поле 'image'."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Имя файла пустое."}), 400
    if not _allowed(file.filename):
        return jsonify({"error": f"Недопустимый тип файла. Разрешены: {ALLOWED_EXTENSIONS}"}), 400

    try:
        image_bytes = file.read()
        result = analyze_image(image_bytes)
        try:
            save_analysis(file.filename, result)
        except Exception as db_err:
            logger.warning(f"Не удалось сохранить в БД: {db_err}")

        return jsonify({"success": True, "filename": file.filename, **result})

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        logger.exception("Ошибка анализа изображения")
        return jsonify({"error": f"Внутренняя ошибка: {str(e)}"}), 500


@image_bp.route("/status", methods=["GET"])
def status():
    return jsonify(get_model_status())
