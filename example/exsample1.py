from typing import Annotated
import json
from pydantic import (BaseModel, EmailStr, ValidationError, Field, ConfigDict, field_validator, model_validator)
from json_text_tests import tests

class Address(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,
                              str_min_length=2, )
    city: Annotated[str, Field(description="Name of the city")]
    street: Annotated[str, Field(min_length=3, description="Name of the street")]
    house_number: Annotated[int, Field(gt=0, description="Number of the house")]


class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True
                              , str_min_length=2, )
    name: Annotated[str, Field(description="Name of user")]
    age: Annotated[int, Field(ge=0, le=120, description="Age of user")]
    email: EmailStr
    is_employed: Annotated[bool, Field(description="Is the user employed?")]
    address: Address

    @field_validator("name")
    @classmethod
    def name_only_letters(cls, value: str) -> str:
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters")
        return value

    @model_validator(mode="after")
    def check_employment_age(self):
        if self.is_employed and not 18 <= self.age <= 65:
            raise ValueError("Employed user must be between 18 and 65 years old")
        return self


def register_user(data: str | dict) -> str:
    user = User.model_validate_json(data)
    #user = User.model_validate(data)
    #print(user)
    return user.model_dump_json(indent=4)


def load_tests(file_name: str):
    try:

        with open(file_name, 'r', encoding='utf-8') as f:
            tests = json.load(f)
            return tests

    except FileNotFoundError as err:
        print(f'File {file_name} was not found: {err}')


if __name__ == "__main__":

    #tests = load_tests("json_text_tests.json")

    for number, json_data in enumerate(tests, start=1):
        print(2 * "\n", 5 * "\t", f"========= TEST {number} =========")
        try:
            result = register_user(json_data)
            print("SUCCESS:")
            print(result)
        except ValidationError as e:
            print(f'ValidationError: {e}')
            # print(f'ValidationError: {e.json(indent=4)}')
