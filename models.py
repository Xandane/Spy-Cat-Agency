from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Cat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    years_experience: int
    breed: str
    salary: float

    missions: List["Mission"] = Relationship(back_populates="cat")


class Mission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    complete: bool = False

    cat_id: Optional[int] = Field(default=None, foreign_key="cat.id")
    cat: Optional[Cat] = Relationship(back_populates="missions")

    targets: List["Target"] = Relationship(back_populates="mission")


class Target(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country: str
    notes: str
    complete: bool = False

    mission_id: Optional[int] = Field(default=None, foreign_key="mission.id")
    mission: Optional[Mission] = Relationship(back_populates="targets")
