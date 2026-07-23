from pydantic import BaseModel
from datetime import datetime

class LessonProgressOut(BaseModel):
    id:int
    learner_id: int
    lesson_id:int
    completed:bool
    completed_at:datetime | None
    model_config = {"from_attributes": True}

class LessonProgressUpdate(BaseModel):
    completed: bool