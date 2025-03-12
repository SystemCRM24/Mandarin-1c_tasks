from pydantic import BaseModel


class ResponseItemSchema(BaseModel):
    position: str
    task_id: str
    message: str = 'ok'
