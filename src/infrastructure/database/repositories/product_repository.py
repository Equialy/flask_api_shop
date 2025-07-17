from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from src.domain.products.schemas import ProductSchemaBase
from src.infrastructure.database.models import Product
import sqlalchemy as sa


class ProductRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session
        self.model = Product

    def add(self, product: Product) -> Product:
        """Добавить продукт в базу данных"""
        self.session.add(product)
        self.session.commit()
        return product


    def get_all(self) -> List[ProductSchemaBase]:
        """Получить все продукты"""
        stmt = sa.select(self.model)
        execute = self.session.execute(stmt)
        profucts = execute.scalars().all()
        return [ProductSchemaBase.model_validate(product) for product in profucts]

    def get_by_category(self, category_id: int) -> List[ProductSchemaBase]:
        """Получить продукты по категории"""
        stmt = sa.select(self.model).where(self.model.category_id==category_id)
        execute = self.session.execute(stmt)
        products = execute.scalars().all()
        return [ProductSchemaBase.model_validate(product) for product in products]

    def get_main_products(self) -> List[ProductSchemaBase]:
        """Получить продукты для главной страницы"""
        stmt = sa.select(self.model).where(self.model.on_main==True)
        execute = self.session.execute(stmt)
        products = execute.scalars().all()
        return [ProductSchemaBase.model_validate(product) for product in products]




    def get_price_range(self) -> tuple[float, float]:
        """Получить диапазон цен"""
        result = self.session.query(
            func.min(self.model.price),
            func.max(self.model.price)
        ).first()
        
        min_price, max_price = result if result else (None, None)
        return (float(min_price) if min_price is not None else 0.0, 
                float(max_price) if max_price is not None else 0.0)



    def clear_all(self) -> int:
        """Очистить все продукты"""
        count = self.session.query(self.model).count()
        self.session.query(Product).delete()
        return count