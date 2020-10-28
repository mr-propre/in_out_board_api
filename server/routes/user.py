from fastapi import APIRouter, Body, Response, status
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    replace_user,
    check_duplicate
)
from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel
)

router = APIRouter()


@router.post(
    "/",
    summary="Creates a user",
    response_description="User successfully created",
    status_code=201
)
async def new_user(response: Response, user: UserSchema = Body(...)):
    if await check_duplicate(user.email) == 0:
        user = jsonable_encoder(user)
        newUser = await add_user(user)
        return ResponseModel(newUser, 201, "New user successfully created.")
    else:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ErrorResponseModel(user, 422, "User's email already exist.")


@router.get(
    "/",
    summary="Retrieves all users",
    response_description="Users successfully retrieved",
    status_code=200
)
async def get_all_users(response: Response):
    users = await retrieve_users()
    if users:
        return ResponseModel(users, 200, "Users successfully retrieved")
    response.status_code = status.HTTP_204_NO_CONTENT
    return ResponseModel(users, 204, "No users found")


@router.get(
    "/{id}",
    summary="Retrieves a user by its ID",
    response_description="User successfully retrieved",
    status_code=200
)
async def get_user_by_id(response: Response, id: str):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, 200, "User successfully retrieved")
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseModel("NOT FOUND", 404, "User doesn't exist.")


@router.put(
    "/{id}",
    summary="Updates a user's data",
    response_description="User's data successfully updated",
    status_code=200
)
async def put_user(
    response: Response,
    id: str,
    req: UpdateUserModel = Body(...)
):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updatedUser = await replace_user(id, req)
    if updatedUser:
        return ResponseModel(updatedUser, 200, "User successfully updated")
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseModel(
            "NOT FOUND",
            404,
            "There was an error updating the user's data."
        )


@router.delete(
    "/{id}",
    summary="Deletes a user",
    response_description="User successfully deleted",
    status_code=200
)
async def remove_user(response: Response, id: str):
    deletedUser = await delete_user(id)
    if deletedUser:
        return ResponseModel(deletedUser, 200, "User deleted successfully")
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseModel("NOT FOUND", 404, "User doesn't exist")
