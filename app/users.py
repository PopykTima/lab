from fastapi import APIRouter, HTTPException
from .schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

fake_db = {}
current_id = 1

@router.get("/", response_model=list[UserResponse])
def get_users():
    return list(fake_db.values())

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global current_id
    new_user = {"id": current_id, **user.model_dump()}
    fake_db[current_id] = new_user
    current_id += 1
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = {"id": user_id, **user.model_dump()}
    fake_db[user_id] = updated_user
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[user_id]
    return {"message": "User deleted"}