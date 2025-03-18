from pydantic import BaseModel


class ResponseItemSchema(BaseModel):
    position: str
    task_id: int
    message: str = 'ok'
