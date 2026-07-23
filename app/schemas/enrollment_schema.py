from pydantic import BaseModel
from datetime import datetime


class EnrollmentOut(BaseModel):
    id: int
    learner_id: int
    course_id: int
    enrolled_at: datetime
    model_config = {"from_attributes": True}
