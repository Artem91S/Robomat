from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        orm_mod=True,
        from_attributes=True,
    )
