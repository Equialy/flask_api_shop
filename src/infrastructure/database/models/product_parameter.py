from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Numeric, Boolean
from src.infrastructure.database.engine import Base


class ProductParameter(Base):
    __tablename__ = 'product_parameters'
    id: Mapped[int] = mapped_column(primary_key=True)
    chosen: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    extra_field_color: Mapped[str | None] = mapped_column(String, nullable=True)
    extra_field_image: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    old_price: Mapped[float | None] = mapped_column(Numeric(precision=18, scale=2), nullable=True)
    parameter_string: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(precision=18, scale=2), nullable=True, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=True)


    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=True)

    product: Mapped["Product"] = relationship('Product', back_populates='parameters')

    def __str__(self):
        return f"{self.name}: {self.parameter_string} - {self.price}" 