from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.infrastructure.database.models import Category


class CategoryRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session
        self.model = Category

    def add(self, category: Category) -> Category:
        """Добавить категорию в базу данных"""
        self.session.add(category)
        self.session.commit()
        return category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """Получить категорию по ID"""
        return self.session.query(Category).filter(Category.id == category_id).first()


    def count(self) -> int:
        """Получить количество категорий"""
        return self.session.query(Category).count()

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