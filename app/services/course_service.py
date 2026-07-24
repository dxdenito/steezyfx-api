from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import (
    CourseCreate,
    CourseUpdate,
    CourseFlagAction,
    CourseReviewAction,
)
from app.models.course import Course


class CourseService:
    def __init__(self, repo: CourseRepository):
        self.repo = repo

    async def create_course(self, data: CourseCreate, tutor_id: int) -> Course: ...
    async def update_course(
        self, course_id: int, data: CourseUpdate, tutor_id: int
    ) -> Course: ...
    async def submit_for_review(self, course_id: int, tutor_id: int) -> Course: ...
    async def review_course(
        self, course_id: int, action: CourseReviewAction
    ) -> Course: ...
    async def flag_course(self, course_id: int, action: CourseFlagAction) -> Course: ...
    async def delete_course(self, course_id: int, tutor_id: int) -> None: ...
