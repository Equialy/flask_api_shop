from sqlalchemy.orm import Session
from typing import List
from src.infrastructure.database.models import ProductImage

class ProductImageRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session
        self.model = ProductImage

    def bulk_add(self, images: List[ProductImage]) -> List[ProductImage]:
        self.session.add_all(images)
        self.session.commit()
        return images

    def get_all(self) -> List[ProductImage]:
        return self.session.query(self.model).all() 