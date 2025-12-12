from pydantic import BaseModel, EmailStr

class OrganizationCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrganizationUpdate(BaseModel):
    organization_name: str
    new_organization_name: str
    email: EmailStr
    password: str

class OrganizationResponse(BaseModel):
    _id: str
    org_name: str
    collection_name: str
    admin_email: str

class UpdateResponse(BaseModel):
    message: str
    old_name: str
    new_name: str
    new_collection: str


class DeleteResponse(BaseModel):
    message: str
    deleted_org: str
