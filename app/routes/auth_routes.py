from fastapi import APIRouter
from ..schemas.auth_schemas import AdminLogin, LoginResponse
from ..services.auth_service import AuthService

router = APIRouter()
service = AuthService()

@router.post("/login", response_model=LoginResponse, status_code=200)
def login(data: AdminLogin):
    return service.login_admin(data)
