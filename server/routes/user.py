from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()


@router.post("/", response_description="Create a new user")
async def new_user(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    newUser = await add_user(user)
    return ResponseModel(newUser, "New user created successfully.")


@router.get("/", response_description="Retrieve all users")
async def get_all_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users retrieved successfully")
    return ResponseModel(users, "No users found")


@router.get("/{id}", response_description="Retrieve a user by its ID")
async def get_user_by_id(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/{id}")
async def put_user(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updatedUser = await update_user(id, req)
    if updatedUser:
        return ResponseModel(
            "User with ID: {} update is successful".format(id),
            "Student  updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id}", response_description="Deletes user")
async def delete_student_data(id: str):
    deletedUser = await delete_user(id)
    if deletedUser:
        return ResponseModel(
            "Student with ID: {} removed".format(id),
            "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
