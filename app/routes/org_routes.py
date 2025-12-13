from fastapi import APIRouter, Depends, Query
from ..services.org_service import OrgService
from ..schemas.org_schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    UpdateResponse,
    DeleteResponse
)
from ..dependencies.auth import get_current_admin

router = APIRouter()
service = OrgService()

@router.post("/org/create", response_model=OrganizationResponse, status_code=201)
def create_organization(data: OrganizationCreate):
    return service.create_org(data)

@router.get("/org/get", response_model=OrganizationResponse)
def get_org(organization_name: str = Query(...)):
    return service.get_org(organization_name)

@router.put("/org/update", response_model=UpdateResponse, status_code=200)
def update_org(
    data: OrganizationUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    return service.update_org(data, current_admin)

@router.delete("/org/delete", response_model=DeleteResponse, status_code=200)
def delete_org(
    organization_name: str = Query(...),
    current_admin: dict = Depends(get_current_admin)
):
    return service.delete_org(organization_name, current_admin)
