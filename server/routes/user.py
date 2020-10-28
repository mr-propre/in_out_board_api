from fastapi import APIRouter, Body, Response
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
    UserResponseModel,
    UsersResponseModel,
    UserSchema,
    UpdateUserModel
)

router = APIRouter()


@router.post(
    "/",
    summary="Creates a user",
    response_description="User successfully created",
    status_code=201,
    response_model=UserResponseModel,
    response_model_exclude_unset=True
)
async def new_user(response: Response, user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    if await check_duplicate(user['email']) == 0:
        newUser = await add_user(user)
        return {
            'responseMessage': "New user successfully created.",
            'user': newUser
        }
    else:
        response.status_code = 422
        return {
            'responseMessage': "User's email already exist.",
            'user': user
        }


@router.get(
    "/",
    summary="Retrieves all users",
    response_description="Users successfully retrieved",
    status_code=200,
    response_model=UsersResponseModel,
    response_model_exclude_unset=True
)
async def get_all_users(response: Response):
    users = await retrieve_users()
    if users:
        return {
            'responseMessage': "Users successfully retrieved",
            'users': users
        }
    else:
        return {'responseMessage': "There is no user in the database"}


@router.get(
    "/{id}",
    summary="Retrieves a user by its ID",
    response_description="User successfully retrieved",
    status_code=200,
    response_model=UserResponseModel,
    response_model_exclude_unset=True
)
async def get_user_by_id(response: Response, id: str):
    user = await retrieve_user(id)
    if user:
        return {'responseMessage': "User successfully retrieved", 'user': user}
    else:
        response.status_code = 404
        return {'responseMessage': "User with id: {} doesn't exist.".format(id)}


@router.put(
    "/{id}",
    summary="Updates a user's data",
    response_description="User's data successfully updated",
    status_code=200,
    response_model=UserResponseModel,
    response_model_exclude_unset=True
)
async def put_user(
    response: Response,
    id: str,
    req: UpdateUserModel = Body(...)
):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updatedUser = await replace_user(id, req)
    if updatedUser:
        return {
            'responseMessage': "User successfully updated",
            'user': updatedUser
        }
    else:
        response.status_code = 404
        return {
            'responseMessage': "There was an error updating the user's data."
        }


@router.delete(
    "/{id}",
    summary="Deletes a user",
    response_description="User successfully deleted",
    status_code=200,
    response_model=UserResponseModel,
    response_model_exclude_unset=True
)
async def remove_user(response: Response, id: str):
    deletedUser = await delete_user(id)
    if deletedUser:
        return {
            'responseMessage': "User deleted successfully",
            'user': deletedUser
        }
    else:
        response.status_code = 404
        return {'responseMessage': "User doesn't exist"}
