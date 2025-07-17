from flask import Blueprint, render_template, Response
import logging

from src.presentation.dependencies.product_di.product import get_product_repository, get_category_repository, \
    get_product_parameter_repository, get_product_image_repository

logger = logging.getLogger(__name__)

index_app = Blueprint(
    "index_app",
    __name__,
    template_folder="templates"
)

app = index_app

@app.route("/", endpoint="index")
def index_view():
    try:
        products = get_product_repository().get_all_orm()
        categories = get_category_repository().get_all()
        parameters = get_product_parameter_repository().get_all()
        images = get_product_image_repository().get_all()

        return render_template("index.html",  products=products,
            categories=categories,
            parameters=parameters,
            images=images)

    except Exception as e:
        logger.error(f"Ошибка при получении данных из бд {e}")
        return f"Ошибка: {str(e)}"
