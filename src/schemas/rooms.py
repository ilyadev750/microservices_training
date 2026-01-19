from pydantic import BaseModel, Field, ConfigDict


class RoomPut(BaseModel):
    title: str
    description: str
    price: int
    quantity: int


class RoomAdd(RoomPut):
    hotel_id: int


class Room(RoomAdd):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
