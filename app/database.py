from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.MONGO_URI)

master_db = client["master_db"]

org_db = client["organizations_db"]

def get_org_collection(collection_name: str):
    return org_db[collection_name]

master_db.organizations.create_index("org_name", unique=True)
