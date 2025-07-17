from sqlalchemy.orm import Session
from typing import List
from src.infrastructure.database.models import ProductParameter

class ProductParameterRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session
        self.model = ProductParameter

    def bulk_add(self, parameters: List[ProductParameter]) -> List[ProductParameter]:
        self.session.add_all(parameters)
        self.session.commit()
        return parameters

    def get_all(self) -> List[ProductParameter]:
        return self.session.query(self.model).all() 