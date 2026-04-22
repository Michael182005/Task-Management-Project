from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        examples=["Prepare sprint plan"],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Review open items and finalize priorities for the week."],
    )
    completed: bool = Field(default=False, examples=[False])

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "title": "Prepare sprint plan",
                "description": "Review open items and finalize priorities for the week.",
                "completed": False,
            }
        },
    )


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = Field(default=None)

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "title": "Prepare sprint plan",
                "description": "Backlog reviewed and priorities updated.",
                "completed": True,
            }
        },
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Prepare sprint plan",
                "description": "Backlog reviewed and priorities updated.",
                "completed": False,
                "user_id": 1,
            }
        },
    )


class TaskActionResponse(BaseModel):
    message: str
    data: TaskResponse

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Task created successfully.",
                "data": {
                    "id": 1,
                    "title": "Prepare sprint plan",
                    "description": "Backlog reviewed and priorities updated.",
                    "completed": False,
                    "user_id": 1,
                },
            }
        }
    )
