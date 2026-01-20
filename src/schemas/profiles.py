from datetime import date
from typing import Annotated

from fastapi import UploadFile, HTTPException, status
from pydantic import BaseModel, HttpUrl, BeforeValidator

from validation import (
    validate_name,
    validate_gender,
    validate_birth_date,
    validate_image,
)


def validate_name_field(value: str) -> str:
    validate_name(value)
    return value


def validate_gender_field(value: str) -> str:
    validate_gender(value)
    return value


def validate_birth_date_field(value: date) -> date:
    validate_birth_date(value)
    return value


def validate_info_field(value: str) -> str:
    if not value or value.strip() == "":
        raise ValueError("Info field cannot be empty or contain only spaces.")
    return value


def validate_avatar_field(value: UploadFile) -> None:
    try:
        validate_image(value)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


class ProfileCreateSchema(BaseModel):

    first_name: Annotated[str, BeforeValidator(validate_name_field)]
    last_name: Annotated[str, BeforeValidator(validate_name_field)]
    gender: Annotated[str, BeforeValidator(validate_gender_field)]
    date_of_birth: Annotated[date, BeforeValidator(validate_birth_date_field)]
    info: Annotated[str, BeforeValidator(validate_info_field)]
    avatar: Annotated[UploadFile, BeforeValidator(validate_avatar_field)]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "gender": "male",
                    "date_of_birth": "1990-01-01",
                    "info": "Software developer from New York"
                }
            ]
        }
    }

# class ProfileResponseSchema(BaseModel):
#     id: int
#     user_id: int
#     first_name: str
#     last_name: str
#     gender: str
#     date_of_birth: date
#     info: str
#     avatar: HttpUrl
#
# # Write your code here
#     model_config = {
#         "from_attributes": True
#     }
class ProfileResponseSchema(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    info: str
    avatar: HttpUrl

    model_config = {
        "from_attributes": True
    }
