from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text, Boolean, DateTime
from src.infrastructure.database.engine import Base


class ProductReview(Base):
    __tablename__ = 'product_reviews'
    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=True)

    product: Mapped["Product"] = relationship('Product', back_populates='reviews')

