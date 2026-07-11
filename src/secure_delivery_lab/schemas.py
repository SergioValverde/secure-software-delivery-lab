from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    content: str = Field(min_length=1, max_length=200)


class MessageRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int = Field(gt=0)
    content: str = Field(min_length=1, max_length=200)
