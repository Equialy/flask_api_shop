from sqlalchemy.orm import Session, joinedload
from typing import List

from src.domain.products.schemas import ProductSchemaBase
from src.infrastructure.database.models import Product
import sqlalchemy as sa


class ProductRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session
        self.model = Product

    def get_all(self) -> List[ProductSchemaBase]:
        """Получить все продукты"""
        stmt = sa.select(self.model)
        execute = self.session.execute(stmt)
        profucts = execute.scalars().all()
        return [ProductSchemaBase.model_validate(product) for product in profucts]

    def get_all_orm(self) -> List[Product]:
        return (self.session.query(self.model).options(
            joinedload(Product.category),
            joinedload(Product.parameters),
            joinedload(Product.images),
            joinedload(Product.colors),
            joinedload(Product.product_review_video),
            joinedload(Product.reviews),
        ).all())

    def clear_all(self) -> int:
        """Очистить все продукты"""
        count = self.session.query(self.model).count()
        self.session.query(self.model).delete()
        return count

    def bulk_add(self, products: List[Product]) -> List[Product]:
        """Добавить несколько продуктов"""
        self.session.add_all(products)
        self.session.commit()
        return products
