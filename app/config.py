from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

settings = Settings()
