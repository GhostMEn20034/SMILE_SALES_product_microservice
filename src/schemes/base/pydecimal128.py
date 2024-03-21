from decimal import Decimal
from typing import Annotated, Any, Callable, Union

from bson.decimal128 import Decimal128
from pydantic_core import core_schema


class _Decimal128PydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_decimal(value: Union[Decimal, str, float]) -> Decimal128:
            return Decimal128(value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(Decimal128),
                core_schema.no_info_plain_validator_function(validate_from_decimal),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(lambda number: float(str(number))),
        )

PyDecimal128 = Annotated[
    Decimal128, _Decimal128PydanticAnnotation
]