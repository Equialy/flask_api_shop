from typing import List, Optional, Dict, Any

from src.domain.products.schemas import ProductSchemaBase
from src.infrastructure.database.repositories.product_repository import ProductRepositoryImpl
from src.infrastructure.database.repositories.category_repository import CategoryRepositoryImpl


class ProductServiceImpl:
    def __init__(self,
                 product_repo: ProductRepositoryImpl,
                 category_repo: CategoryRepositoryImpl,
                 ):
        self.product_repo = product_repo
        self.category_repo = category_repo

    def get_all_products(self) -> List[ProductSchemaBase]:
        """Получить все продукты"""
        return self.product_repo.get_all()
