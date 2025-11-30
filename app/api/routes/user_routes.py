from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.service.user_service import UserService
from app.dependencies import get_user_service
from app.schemas.user_schemas import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user_api(
    user: UserCreateRequest, 
    user_service: UserService = Depends(get_user_service)
):
    try:
        created_user = user_service.create_user(user.name, user.email)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[UserResponse])
async def get_all_users_api(
    user_service: UserService = Depends(get_user_service)
):
    try:
        users = user_service.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{email}", response_model=UserResponse)
async def get_user_api(
    email: str, 
    user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_api(
    user_id: int, 
    user_update: UserUpdateRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        updated_user = user_service.update_user(
            user_id, 
            name=user_update.name
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{email}")
async def delete_user_api(
    email: str,
    user_service: UserService = Depends(get_user_service)
):
    try:
        success = user_service.delete_user_by_email(email)
        if success:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete user")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")