from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ValidationError, validator, Field

from fastapi import Depends, APIRouter, Request, Response, HTTPException

print("-----------------schema.py-----------------------------")


class create_person(BaseModel):
    id: Optional[int]
    first_name: str = Field(regex="^[a-zA-Z]+$", min_length=2, max_length=20)
    middle_name: str | None = Field(regex="^[a-zA-Z ]+$", max_length=20)
    last_name: str | None = Field(regex="^[a-zA-Z]+$", max_length=20)
    country_code: str | None = Field(regex="(^[0-9+]+$)", min_length=2, max_length=6)  # 0 to 9 and +
    mobile_no: str | None = Field(regex="(^[0-9]+$)", min_length=6, max_length=15)  # 0 to 9
    email: str | None = None
    gender: str | None = Field(regex='(M|F)')  # accept only M or F
    dob: date | None = None
    city: str | None = None

    @validator('first_name', always=True)  # always= true means to check even if no data is received
    def FirstName(cls, v):
        if v is None or v == ' ' or v == '':
            # raise ValueError('Null Fields and Space not Allowed !')
            raise HTTPException(status_code=403, detail=f"Null Fields, Space and 0 not Allowed !")
        return v

    class Config:
        orm_mode = True
        validate_all = True

class update_person(BaseModel):
    id: Optional[int]
    first_name: str = Field(regex="^[a-zA-Z]+$", min_length=2, max_length=20)
    middle_name: str | None = Field(regex="^[a-zA-Z ]+$", max_length=20)
    last_name: str | None = Field(regex="^[a-zA-Z]+$", max_length=20)
    country_code: str | None = Field(regex="(^[0-9+]+$)", min_length=2, max_length=6)  # 0 to 9 and +
    gender: str | None = Field(regex='(M|F)')  # accept only M or F
    dob: date | None = None

    @validator('first_name', always=True)  # always= true means to check even if no data is received
    def FirstName(cls, v):
        if v is None or v == ' ' or v == '':
            # raise ValueError('Null Fields and Space not Allowed !')
            raise HTTPException(status_code=403, detail=f"Null Fields, Space and 0 not Allowed !")
        return v

    class Config:
        orm_mode = True
        validate_all = True


class user(BaseModel):
    person_id: str = Field(regex="(^[0-9]+$)")  # 0 to 9
    username: str = Field(regex="^[a-zA-Z0-9]+$", min_length=2, max_length=20)
    password: str = Field(regex="^[A-Za-z0-9`~!_$%*@.#&+-]*$", min_length=2, max_length=20)
    role_id: str = Field(regex="(^[0-9]+$)", max_length=6)  # 0 to 9


class log_in(BaseModel):
    username: str
    password: str


# //-----------------assign cultivator to persons start------------
class active_cultivator(BaseModel):
    id: str
    name: str


class assign_cultivator_to_persons(BaseModel):
    cultivator: active_cultivator
    persons: list


# //-----------------assign cultivator to persons end--------------

# //----------------pedantic Validator test----------------------------------------------
class test(BaseModel):
    name: str = ''
    role_id: int = 0
    test: str | None

    @validator('name', always=True)  # always= true means to check even if no data is received
    def Name(cls, v):
        if ' ' in v or v == '':
            # raise ValueError('Null Fields and Space not Allowed !')
            raise HTTPException(status_code=403, detail=f"Null Fields, Space and 0 not Allowed !")
        return v

    @validator('role_id', always=True)
    def Role_Id(cls, v):
        if v == 0:
            raise HTTPException(status_code=403, detail=f"Roll id 0 or null not Allowed !")
        return v

    class Config:
        orm_mode = True
        validate_all = True


class TestRegx(BaseModel):
    goi: str
    country_code: str | None = Field(regex="(^[0-9+]+$)")  # 0 to 9 and +
