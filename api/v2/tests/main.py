from pydantic import BaseModel


class Item(BaseModel):
    value: int


class Base(BaseModel):
    data: list[Item]


dct = {
    '1': Item(value=1),
    '2': Item(value=2)
}

base = Base.model_validate({'data': })
