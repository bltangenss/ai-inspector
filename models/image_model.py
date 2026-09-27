import logging
import io
from PIL import Image

logger = logging.getLogger(__name__)

_pipeline = None
_model_status = "not_loaded"
_model_error = None

MODEL_ID = "umm-maybe/AI-image-detector"


def load_image_model():
    """Загружает ViT-модель для определения ИИ-изображений."""
    global _pipeline, _model_status, _model_error
    try:
        logger.info(f"Загрузка модели {MODEL_ID} ...")
        _model_status = "loading"
        from transformers import pipeline
        _pipeline = pipeline("image-classification", model=MODEL_ID)
        _model_status = "ready"
        logger.info("Модель успешно загружена.")
    except Exception as e:
        _model_error = str(e)
        _model_status = "error"
        logger.error(f"Ошибка загрузки модели: {e}")


def get_model_status() -> dict:
    return {"status": _model_status, "model": MODEL_ID, "error": _model_error}


def analyze_image(image_bytes: bytes) -> dict:
    """
    Принимает байты изображения, возвращает результат классификации.
    Returns:
        {
          "label": "AI" | "Real",
          "ai_probability": float,   # 0-100
          "real_probability": float, # 0-100
          "verdict": str,
          "confidence": str          # "Высокая" | "Средняя" | "Низкая"
        }
    """
    global _pipeline, _model_status

    if _model_status != "ready" or _pipeline is None:
        raise RuntimeError(f"Модель не готова. Статус: {_model_status}")

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = _pipeline(image)

    # Модель возвращает метки "artificial" и "real"
    scores = {r["label"].lower(): r["score"] for r in results}

    ai_prob   = round(scores.get("artificial", scores.get("ai", 0.0)) * 100, 2)
    real_prob = round(scores.get("real", 1 - ai_prob / 100) * 100, 2)

    # Нормализация на случай float-погрешностей
    total = ai_prob + real_prob
    if total > 0:
        ai_prob   = round(ai_prob   / total * 100, 2)
        real_prob = round(real_prob / total * 100, 2)

    label = "AI" if ai_prob >= 50 else "Real"

    max_p = max(ai_prob, real_prob)
    if max_p >= 85:
        confidence = "Высокая"
    elif max_p >= 65:
        confidence = "Средняя"
    else:
        confidence = "Низкая"

    if label == "AI":
        verdict = f"Изображение, скорее всего, создано искусственным интеллектом ({ai_prob:.1f}%)."
    else:
        verdict = f"Изображение, скорее всего, реальное ({real_prob:.1f}%)."

    return {
        "label":            label,
        "ai_probability":   ai_prob,
        "real_probability": real_prob,
        "verdict":          verdict,
        "confidence":       confidence,
    }
