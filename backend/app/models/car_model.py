from typing import Annotated, Any, Callable, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import core_schema


class _ObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


PydanticObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]


class MongoBaseModel(BaseModel):
    """
    Extend Pydantic's BaseModel with the PyObjectId that we just
    created and use it as the basis for all of our models
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")

    def dict(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        if exclude is None:
            exclude = set()
        return super().model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )


class CarBase(MongoBaseModel):
    """
    Inheriting from MongoBaseModel so it has the `id` field.
    Then we define other fields for the car data model
    """

    brand: str = Field(..., min_length=3)
    make: str = Field(..., min_length=3)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)


class CarUpdate(MongoBaseModel):
    """
    Used to update only a single provided field in the CarBase model
    """

    price: Optional[int] = None


class CarDB(CarBase):
    """
    A model that represents the instance in the database.
    For now it's identical to the `CarBase` model, but itcan be different later
    """

    pass
