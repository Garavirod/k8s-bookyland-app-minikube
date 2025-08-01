from motor.motor_asyncio import AsyncIOMotorClient
from environment import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD

# MongoDB connection
client = None
database = None

async def connect_to_mongo():
    global client, database
    # MongoDB connection string
    if DATABASE_USER and DATABASE_PASSWORD:
        mongo_url = f"mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}"
    else:
        mongo_url = f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}"
    
    client = AsyncIOMotorClient(mongo_url)
    database = client[DATABASE_NAME]
    return database

async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    return database
