from datetime import datetime
from pydantic import BaseModel

class TodoBase(BaseModel):
    title : str
    description : str
    tododate : datetime
    completed : bool | None = False
    
    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title : str
    description : str
    tododate : datetime
class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id : int