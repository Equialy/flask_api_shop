


from pydantic import BaseModel, ConfigDict, Field, AliasGenerator
from pydantic.alias_generators import to_camel
from typing import Optional
from datetime import datetime
from decimal import Decimal



class ProductParametrSchemaRead(BaseModel):
    chosen: int | None = None
    disabled: bool | None = None
    extra_field_color: str | None = None
    extra_field_image: str | None = None
    name: str | None = None
    old_price: float | None = None
    parameter_string: str | None = None
    price: float | None = None
    sort_order: float | None = None
    product_id: int | None = None

    # model_config = ConfigDict(
    #     from_attributes=True,
    #     alias_generator=AliasGenerator(serialization_alias=to_camel),
    #     json_encoders={Decimal: str}
    # )

class ProductParametrSchemaBase( ProductParametrSchemaRead):
    id: int | None = None
