from pydantic import BaseModel


class ResponseItemSchema(BaseModel):
    position: str
    user_id: str
    message: str = 'ok'
