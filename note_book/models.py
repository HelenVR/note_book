from pydantic import BaseModel


class Contact(BaseModel):
    id: int
    name: str
    surname: str
    phone_number: str
    comment: str