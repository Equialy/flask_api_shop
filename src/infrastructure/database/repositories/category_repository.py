from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.infrastructure.database.models import Category


class CategoryRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session
        self.model = Category


    def bulk_add(self, categories: List[Category]) -> List[Category]:
        """Добавить несколько категорий"""
        self.session.add_all(categories)
        self.session.commit()
        return categories

    def clear_all(self) -> int:
        """Очистить все категории"""
        count = self.session.query(Category).count()
        self.session.query(Category).delete()
        self.session.commit()
        return count 

    def get_all(self) -> List[Category]:
        return self.session.query(self.model).all() 