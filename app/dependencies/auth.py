from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..utils.jwt_handler import decode_access_token

bearer_scheme = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    decoded = decode_access_token(token)

    if not decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return decoded
