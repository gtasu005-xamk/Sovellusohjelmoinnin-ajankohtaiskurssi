from pydantic import BaseModel, ConfigDict, Field


class UnitLinkIn(BaseModel):
    unit_type_id: int
    sort_order: int = 0
    is_required: bool = True
    per_set: bool = False


class ActivityTypeCreate(BaseModel):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    unit_links: list[UnitLinkIn] = []


class UnitTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    slug: str


class UnitLinkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    unit_type_id: int
    sort_order: int
    is_required: bool
    per_set: bool
    unit_type: UnitTypeOut


class ActivityTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    slug: str
    is_system: bool
    user_id: int | None
    unit_links: list[UnitLinkOut]
