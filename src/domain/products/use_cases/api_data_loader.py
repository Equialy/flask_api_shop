
import requests
import logging
from typing import Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.infrastructure.database.models import Category, Product, ProductParameter, ProductImage
from src.infrastructure.database.repositories.product_repository import ProductRepositoryImpl
from src.infrastructure.database.repositories.category_repository import CategoryRepositoryImpl
from src.infrastructure.database.repositories.product_parameter_repository import ProductParameterRepositoryImpl
from src.infrastructure.database.repositories.product_image_repository import ProductImageRepositoryImpl
from src.settings import settings

logger = logging.getLogger(__name__)


class ApiDataLoaderService:
    def __init__(self,
                 product_repo: ProductRepositoryImpl,
                 category_repo: CategoryRepositoryImpl,
                 parameter_repo: ProductParameterRepositoryImpl,
                 image_repo: ProductImageRepositoryImpl,
                 ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.parameter_repo = parameter_repo
        self.image_repo = image_repo
        self.base_url = settings.base_api

    def fetch_api_data(self, on_main: bool = None) -> dict[str, Any]:
        """Загрузить данные из API"""
        try:
            url = f"{self.base_url}"
            params = {}
            if on_main is not None:
                params['on_main'] = str(on_main).lower()

            logger.info(f"Загружаем данные из API: {url} с параметрами {params}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Успешно загружено данных: {len(data.get('products', []))} продуктов")
            return data

        except requests.RequestException as e:
            logger.error(f"Ошибка при загрузке данных из API: {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise

    def load_all_data(self) -> dict[str, int]:
        """Загружаются все данные из API on_main=true и on_main=false"""
        try:
            with ThreadPoolExecutor(max_workers=3) as executor:
                main_data = executor.submit(self.fetch_api_data,on_main=True )
                other_data = executor.submit(self.fetch_api_data, on_main=False)
            combined_data = self._combine_api_data(main_data.result(), other_data.result())
            return self._save_to_database(combined_data)
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise

    def _combine_api_data(self, main_data: dict[str, Any], other_data: dict[str, Any]) -> dict[str, Any]:
        """Объединить данные из двух API запросов"""
        combined = {
            'categories': [],
            'products': []
        }
        category_ids = set()
        for data in [main_data, other_data]:
            for category in data.get('categories', []):
                if category['Category_ID'] not in category_ids:
                    combined['categories'].append(category)
                    category_ids.add(category['Category_ID'])
        product_ids = set()
        for data in [main_data, other_data]:
            for product in data.get('products', []):
                if product['Product_ID'] not in product_ids:
                    combined['products'].append(product)
                    product_ids.add(product['Product_ID'])

        logger.info(f"Объединено: {len(combined['categories'])} категорий, {len(combined['products'])} продуктов")

        return combined

    def _save_to_database(self, data: dict[str, Any]) -> dict[str, int]:
        """Сохранить данные в базу данных"""
        try:
            deleted_counts = self._clear_existing_data()
            categories = self._save_categories(data.get('categories', []))
            products, parameters, images = self._prepare_products_params_images(data.get('products', []))
            self.product_repo.bulk_add(products)
            self.parameter_repo.bulk_add(parameters)
            self.image_repo.bulk_add(images)
            logger.info(
                f"Данные сохранены в БД: {len(categories)} категорий, {len(products)} продуктов, {len(parameters)} параметров, {len(images)} изображений")

            return {
                "categories_saved": len(categories),
                "products_saved": len(products),
                "parameters_saved": len(parameters),
                "images_saved": len(images),
                "categories_deleted": deleted_counts["categories_deleted"],
                "products_deleted": deleted_counts["products_deleted"]
            }

        except Exception as e:
            logger.error(f"Ошибка при сохранении данных в БД: {e}")
            raise

    def _clear_existing_data(self) -> dict[str, int]:
        """Очистить существующие данные"""
        parametrs_deleted = self.parameter_repo.clear_all()
        products_deleted = self.product_repo.clear_all()
        categories_deleted = self.category_repo.clear_all()

        return {
            "parametres_deleted": parametrs_deleted,
            "products_deleted": products_deleted,
            "categories_deleted": categories_deleted
        }

    def _save_categories(self, categories_data: list[dict[str, Any]]) -> list[Category]:
        """Сохранить категории"""
        categories = []
        for cat_data in categories_data:
            category = Category(
                id=cat_data['Category_ID'],
                name=cat_data['Category_Name'],
                image=cat_data.get('Category_Image'),
                sort_order=cat_data.get('sort_order', 0)
            )
            categories.append(category)

        return self.category_repo.bulk_add(categories)

    def _prepare_products_params_images(self, products_data: list[dict[str, Any]]):
        products = []
        parameters = []
        images = []
        for product_data in products_data:
            product = Product(
                id=product_data['Product_ID'],
                name=product_data['Product_Name'],
                on_main=product_data.get('OnMain', False),
                importance_num=product_data.get('importance_num'),
                tags=product_data.get('tags'),
                created_at=self._parse_datetime(product_data.get('Created_At')),
                updated_at=self._parse_datetime(product_data.get('Updated_At'))
            )
            if product_data.get('categories'):
                category_id = product_data['categories'][0]['Category_ID']
                product.category_id = category_id
            products.append(product)
            for param in product_data.get('parameters', []):
                parameter = ProductParameter(
                    id=param['Parameter_ID'],
                    name=param.get('name'),
                    parameter_string=param.get('parameter_string'),
                    price=param.get('price', 0),
                    old_price=param.get('old_price'),
                    extra_field_image=param.get('extra_field_image'),
                    extra_field_color=param.get('extra_field_color'),
                    chosen=param.get('chosen'),
                    disabled=param.get('disabled', False),
                    sort_order=param.get('sort_order', 0),
                    product_id=product.id
                )
                parameters.append(parameter)
            for img in product_data.get('images', []):
                pos = img.get('position')
                try:
                    position = int(pos) if pos is not None and str(pos).isdigit() else None
                except (TypeError, ValueError):
                    position = None
                image = ProductImage(
                    id=img['Image_ID'],
                    image_url=img.get('Image_URL'),
                    main_image=img.get('MainImage'),
                    title=img.get('title'),
                    position=position,
                    sort_order=img.get('sort_order', 0),
                    product_id=product.id
                )
                images.append(image)
        return products, parameters, images

    def _parse_datetime(self, date_string: str) -> datetime:
        """Парсить дату из строки"""
        if not date_string:
            return datetime.now()

        try:
            return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            return datetime.now()
