from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.user import User
from app.task import Task
from app.schemas import UserCreate, UserResponse, TaskCreate, TaskResponce
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Проверяем, существует ли пользователь
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    token = create_access_token(data = {'sub': str(user.id)})
    return {'access_token': token, 'token_type':'bearer'}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user))->UserResponse:
    return current_user

@router.post("/createtask")
async def createtask(task_data: TaskCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    task = Task(title=task_data.title, description=task_data.description, owner_id = user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@router.patch("/tasks/{task_id}")
async def update_task(
    task_id: int, 
    is_completed: bool, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == user.id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_completed = is_completed
    
    await db.commit()
    await db.refresh(task)
    return task

@router.get("/", response_model=list[TaskResponce])
async def getalltask(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(user.id == Task.owner_id))
    return result.scalars().all()
