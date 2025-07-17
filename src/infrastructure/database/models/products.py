from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey,  Boolean, Integer, Text
from src.infrastructure.database.engine import Base


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)
    on_main: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime,default=datetime.now, onupdate=datetime.now, nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    importance_num: Mapped[int | None] = mapped_column(Integer, nullable=True)
    moysklad_connector_products_data: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)


    product_review_video: Mapped[list["ProductVideo"]] = relationship("ProductVideo", back_populates="product",  cascade="all, delete-orphan")
    category: Mapped["Category"] = relationship('Category', back_populates='products')
    parameters: Mapped[list["ProductParameter"]] = relationship('ProductParameter', back_populates='product', cascade="all, delete-orphan")
    images: Mapped[list["ProductImage"]] = relationship('ProductImage', back_populates='product', cascade="all, delete-orphan")
    colors: Mapped[list["ProductColor"]] = relationship('ProductColor', back_populates='product', cascade="all, delete-orphan")
    reviews: Mapped[list["ProductReview"]] = relationship('ProductReview', back_populates='product', cascade="all, delete-orphan")


    def __str__(self):
        return f"{self.name}"