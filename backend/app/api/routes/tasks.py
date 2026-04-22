from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Task, User
from app.schemas.task import TaskActionResponse, TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

UNAUTHORIZED_RESPONSE = {
    401: {
        "description": "Authentication failed.",
        "content": {
            "application/json": {
                "example": {"detail": "Not authenticated."}
            }
        },
    }
}


def get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task


def ensure_task_owner(
    task: Task,
    current_user: User,
    detail: str = "You do not have access to this task.",
) -> None:
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


@router.post(
    "",
    response_model=TaskActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    responses={
        **UNAUTHORIZED_RESPONSE,
        201: {
            "description": "Task created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Task created successfully.",
                        "data": {
                            "id": 1,
                            "title": "Prepare sprint plan",
                            "description": "Review open items and finalize priorities.",
                            "completed": False,
                            "user_id": 1,
                        },
                    }
                }
            },
        },
    },
)
def create_task(
    payload: TaskCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> TaskActionResponse:
    task = Task(
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        user_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskActionResponse(
        message="Task created successfully.",
        data=TaskResponse.model_validate(task),
    )


@router.get(
    "",
    response_model=list[TaskResponse],
    summary="Get the authenticated user's tasks",
    responses={
        **UNAUTHORIZED_RESPONSE,
        200: {
            "description": "Tasks fetched successfully.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Prepare sprint plan",
                            "description": "Review open items and finalize priorities.",
                            "completed": False,
                            "user_id": 1,
                        }
                    ]
                }
            },
        },
    },
)
def list_tasks(db: DBSession, current_user: CurrentUser) -> list[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.id.desc())
    )
    return list(db.execute(statement).scalars().all())


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    responses={
        **UNAUTHORIZED_RESPONSE,
        403: {
            "description": "The task does not belong to the current user.",
            "content": {
                "application/json": {
                    "example": {"detail": "You do not have access to this task."}
                }
            },
        },
        404: {
            "description": "Task not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Task not found."}
                }
            },
        },
    },
)
def get_task(task_id: int, db: DBSession, current_user: CurrentUser) -> Task:
    task = get_task_or_404(db, task_id)
    ensure_task_owner(task, current_user)
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    responses={
        **UNAUTHORIZED_RESPONSE,
        403: {
            "description": "The task does not belong to the current user.",
            "content": {
                "application/json": {
                    "example": {"detail": "You can only update your own tasks."}
                }
            },
        },
        404: {
            "description": "Task not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Task not found."}
                }
            },
        },
    },
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> Task:
    task = get_task_or_404(db, task_id)
    ensure_task_owner(task, current_user, "You can only update your own tasks.")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        **UNAUTHORIZED_RESPONSE,
        204: {
            "description": "Task deleted successfully.",
        },
        403: {
            "description": "The task cannot be deleted by the current user.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You can only delete your own tasks unless you are an admin."
                    }
                }
            },
        },
        404: {
            "description": "Task not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Task not found."}
                }
            },
        },
    },
)
def delete_task(
    task_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> Response:
    task = get_task_or_404(db, task_id)
    if task.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own tasks unless you are an admin.",
        )

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
