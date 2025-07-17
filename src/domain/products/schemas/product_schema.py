from pydantic import BaseModel, ConfigDict, Field, AliasGenerator
from pydantic.alias_generators import to_camel
from typing import Optional
from datetime import datetime
from decimal import Decimal



class ProductSchemaRead(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название продукта")
    on_main: bool = Field(default=False, description="Отображать на главной странице")
    importance_num: Optional[int] = Field(None, ge=0, description="Приоритет продукта")
    tags: Optional[str] = Field(None, max_length=1000, description="Теги продукта")
    category_id: Optional[int] = Field(None, gt=0, description="ID категории")
    updated_at: datetime | None = None
    created_at: datetime | None = None
    moysklad_connector_products_data: int | None = None


    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
        json_encoders={Decimal: str}
    )

class ProductSchemaBase(BaseModel):
    id: int


class ProductSchemaCreate(ProductSchemaBase):
    """Схема для создания продукта"""
    pass



