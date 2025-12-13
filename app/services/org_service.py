from ..database import master_db, get_org_collection
from ..utils.hashing import hash_password
from ..schemas.org_schemas import OrganizationCreate, OrganizationUpdate
from bson import ObjectId
from fastapi import HTTPException, status


class OrgService:

    def create_org(self, data: OrganizationCreate):
        org_name = data.organization_name.lower()

        existing_org = master_db.organizations.find_one({"org_name": org_name})
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization already exists"
            )

        collection_name = f"org_{org_name}"
        org_collection = get_org_collection(collection_name)

        admin_user = {
            "_id": str(ObjectId()),
            "email": data.email,
            "password": hash_password(data.password)
        }

        org_collection.insert_one({"admin": admin_user})

        master_db.organizations.insert_one({
            "org_name": org_name,
            "collection_name": collection_name,
            "admin_email": data.email,
            "admin_password": admin_user["password"]
        })

        return {
            "message": "Organization created successfully",
            "organization_name": org_name,
            "collection_name": collection_name,
            "admin_email": data.email
        }

    def get_org(self, organization_name: str):
        org_name = organization_name.lower()

        org = master_db.organizations.find_one({"org_name": org_name})
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )

        org["_id"] = str(org["_id"])
        if "admin_password" in org:
            del org["admin_password"]

        return org

    def update_org(self, data: OrganizationUpdate, current_admin: dict):
        """
        Expects:
         - data.organization_name = current org name (lowercased inside)
         - data.new_organization_name = new name to rename to
         - data.email / data.password = optional new admin credentials
         - current_admin = decoded JWT payload (must contain 'org_name')
        """
        old_name = data.organization_name.lower()
        new_name = data.new_organization_name.lower()

        if current_admin.get("org_name") != old_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update another organization"
            )

        existing_org = master_db.organizations.find_one({"org_name": old_name})
        if not existing_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )

        if new_name != old_name:
            conflict = master_db.organizations.find_one({"org_name": new_name})
            if conflict:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New organization name already exists"
                )

        old_collection_name = existing_org["collection_name"]
        new_collection_name = f"org_{new_name}"

        old_collection = get_org_collection(old_collection_name)
        new_collection = get_org_collection(new_collection_name)

        if new_name != old_name:
            docs_cursor = old_collection.find({})
            docs = []
            for doc in docs_cursor:
                doc.pop("_id", None)
                docs.append(doc)
            if docs:
                new_collection.insert_many(docs)
            old_collection.drop()

        existing_admin_pwd = existing_org.get("admin_password")
        hashed_pwd = existing_admin_pwd
        if getattr(data, "password", None):
            hashed_pwd = existing_org["admin_password"] if not data.password else hash_password(data.password)


        master_db.organizations.update_one(
            {"_id": existing_org["_id"]},
            {
                "$set": {
                    "org_name": new_name,
                    "collection_name": new_collection_name,
                    "admin_email": data.email if data.email else existing_org.get("admin_email"),
                    "admin_password": hashed_pwd
                }
            }
        )

        update_fields = {}
        if data.email:
            update_fields["admin.email"] = data.email
        if getattr(data, "password", None):
            update_fields["admin.password"] = hashed_pwd

        if update_fields:
            new_collection.update_one({}, {"$set": update_fields})

        return {
            "message": "Organization updated successfully",
            "old_name": old_name,
            "new_name": new_name,
            "new_collection": new_collection_name
        }

    def delete_org(self, organization_name: str, current_admin: dict):
        organization_name = organization_name.lower()

        if current_admin.get("org_name") != organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot delete another organization"
            )

        org = master_db.organizations.find_one({"org_name": organization_name})
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )

        collection_name = org["collection_name"]
        collection = get_org_collection(collection_name)
        collection.drop()

        master_db.organizations.delete_one({"_id": org["_id"]})

        return {
            "message": "Organization deleted successfully",
            "deleted_org": organization_name
        }
