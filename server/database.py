import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config


MONGO_DETAILS = config('MONGO_DETAILS')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.in_out_board
usersCollection = db.get_collection("users")


# Helpers
def users_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "email": user["email"],
        "department": user["department"],
        "status": user["status"]
        }


# Retrieves all users present in the database
async def retrieve_users():
    users = []
    async for user in usersCollection.find():
        users.append(users_helper(user))
    return users


# Adds a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await usersCollection.insert_one(user_data)
    new_user = await usersCollection.find_one({"_id": user.inserted_id})
    return users_helper(new_user)


# Retrieves a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await usersCollection.find_one({"_id": ObjectId(id)})
    if user:
        return users_helper(user)


# Updates a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await usersCollection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await usersCollection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Deletes a user from the database
async def delete_user(id: str):
    user = await usersCollection.find_one({"_id": ObjectId(id)})
    if user:
        await usersCollection.delete_one({"_id": ObjectId(id)})
        return True
