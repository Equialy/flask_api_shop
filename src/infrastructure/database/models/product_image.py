from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean
from src.infrastructure.database.engine import Base


class ProductImage(Base):
    __tablename__ = 'product_images'
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    main_image: Mapped[bool] = mapped_column(Boolean,  nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=True)
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    sort_order: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)


    product: Mapped["Product"] = relationship('Product', back_populates='images')

    def __str__(self):
        return f"Image {self.id} for {self.product_id}" 