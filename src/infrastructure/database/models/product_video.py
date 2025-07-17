from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,  ForeignKey, Integer
from src.infrastructure.database.engine import Base


class ProductVideo(Base):

    __tablename__ = "product_video"
    id: Mapped[int] = mapped_column(Integer, index=True, unique=True, primary_key=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=True)

    product: Mapped["Product"] = relationship('Product', back_populates='product_review_video')