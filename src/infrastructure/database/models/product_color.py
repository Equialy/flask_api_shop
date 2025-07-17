from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from src.infrastructure.database.engine import Base


class ProductColor(Base):
    __tablename__ = 'product_colors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=True)

    product: Mapped["Product"] = relationship('Product', back_populates='colors')

    def __str__(self):
        return f"{self.name}" 