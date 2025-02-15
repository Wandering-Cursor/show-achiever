import pydantic


class Schema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        validate_default=True,
    )
