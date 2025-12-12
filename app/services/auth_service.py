from ..database import master_db
from ..utils.hashing import verify_password
from ..utils.jwt_handler import create_access_token
from ..schemas.auth_schemas import AdminLogin

class AuthService:
    def login_admin(self, data: AdminLogin):
        # Check if admin exists in master_db
        org = master_db.organizations.find_one({"admin_email": data.email})

        if not org:
            return {"error": "Invalid credentials"}

        # Verify password
        is_valid = verify_password(data.password, org["admin_password"])
        if not is_valid:
            return {"error": "Invalid credentials"}

        # Create JWT token
        token = create_access_token({
            "admin_id": str(org["_id"]),
            "admin_email": data.email,
            "org_name": org["org_name"]
        })

        return {
            "message": "Login successful",
            "token": token,
            "org_name": org["org_name"]
        }
