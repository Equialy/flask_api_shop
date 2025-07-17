from flask import Blueprint, Response
import logging

from src.presentation.dependencies.product_di.product import get_product_repository, get_category_repository, \
    get_product_image_repository, get_product_parameter_repository
from src.settings import settings
logger = logging.getLogger(__name__)

product_api = Blueprint("product_api", __name__, url_prefix=settings.api.v1.prefix)


@product_api.route("/info", methods=["GET"])
def info_view():
    """Вывод всех данных из БД простым текстом"""
    try:
        products = get_product_repository().get_all_orm()
        categories = get_category_repository().get_all()
        parameters = get_product_parameter_repository().get_all()
        images = get_product_image_repository().get_all()
        text = []
        text.append(f"Всего товаров: {len(products)}")
        text.append(f"Всего категорий: {len(categories)}")
        text.append(f"Всего параметров: {len(parameters)}")
        text.append(f"Всего изображений: {len(images)}\n")
        text.append("Категории:")
        for c in categories:
            text.append(f"- {c.id}: {c.name}")

        text.append("\nТовары:")
        for p in products:
            text.append(f"- {p.id}: {p.name} | Категория: {p.category_id}")
        text.append("\nПараметры:")
        for param in parameters:
            text.append(f" - {param.id}: {param.extra_field_image}")
        text.append("\nИзображения:")

        return Response("\n".join(text), mimetype="text/plain; charset=utf-8")
    except Exception as e:
        logger.error(f"Ошибка при получении данных для /info: {e}")
        return f"Ошибка: {str(e)}"
