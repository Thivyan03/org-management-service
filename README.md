# Organization Management Service

A multi-tenant backend service built using FastAPI and MongoDB.
Each organization receives a dynamically created collection "org_<organization_name>".
A Master Database stores global metadata and admin credentials. JWT authentication is used for admin access.

### Features

* Multi-tenant architecture

* Dynamic MongoDB collection creation

* JWT Authentication

* Secure password hashing 

* Organization CRUD operations

* Master DB metadata storage

* Clean modular structure 

### Project Structure

app/

 ├── routes/
 
 ├── services/
 
 ├── schemas/
 
 ├── dependencies/
 
 ├── utils/
 
 ├── config.py
 
 
 ├── database.py
 
 └── main.py

### Tech Stack

* FastAPI

* MongoDB

* PyMongo

* bcrypt

* Python-Jose

* Pydantic

### Installation & Setup
1️. Clone the repository
  git clone <your-repo-url>
  cd <project-folder>

2️. Create virtual environment
  python -m venv venv
  venv\Scripts\activate    # Windows

3️. Install dependencies
  pip install -r requirements.txt

4️. Environment Variables

  Create a .env file:
  
  MONGO_URI=<your_mongodb_connection_string>
  JWT_SECRET=<your_secret_key>
  JWT_ALGORITHM=HS256

5️. Run the Server
  uvicorn app.main:app --reload

6️. API Docs

   http://localhost:8000/docs

### Authentication

Admins log in using /login to receive a JWT token.
Use the token for protected endpoints via:

Authorization: Bearer <token>


Protected routes:

/org/update

/org/delete

### Example Input/Output
### API Endpoints
1️. Create Organization

POST /org/create

Request

{
  "organization_name": "Alpha",
  "email": "admin@alpha.com",
  "password": "alpha123"
}


Response

{
  "message": "Organization created successfully",
  "organization_name": "alpha",
  "collection_name": "org_alpha",
  "admin_email": "admin@alpha.com"
}

2️. Get Organization

GET /org/get?organization_name=Alpha

Response

{
  "message": "Organization details fetched successfully",
  "organization_name": "alpha",
  "collection_name": "org_alpha",
  "admin_email": "admin@alpha.com"
}

3️. Update Organization (JWT Required)

PUT /org/update

Request

{
  "organization_name": "Alpha",
  "new_organization_name": "Beta",
  "email": "admin@beta.com",
  "password": "beta123"
}

4️. Delete Organization (JWT Required)

DELETE /org/delete?organization_name=Beta

Response

{
  "message": "Organization deleted successfully",
  "deleted_org": "beta"
}

5️. Admin Login

POST /login

Request

{
  "email": "admin@alpha.com",
  "password": "alpha123"
}

### Design Choices & Scalability Notes

* Simple and clear tenant isolation

* Dynamic collections reduce cross-tenant leakage

* Master DB allows fast organization lookup

### Modular Class-Based Architecture

This project follows a modular, class-based architecture:

* Routes handle HTTP input/output

* Service classes (OrgService, AuthService) contain business logic

* Schemas define request/response models

* Dependencies manage authentication

* Utils store helper functions (JWT, hashing)

* Database layer abstracts MongoDB interactions

### Trade-offs

* Many collections can grow large in very big systems

* Shared DB cluster means noisy-neighbor issues

* Better alternatives for large-scale systems

* Shared collection with tenant_id

* Dedicated database per tenant

* Sharded clusters

### Testing Guide

* Create organization

* Login to receive JWT

* Authorize using Swagger

* Test /org/update

* Test /org/delete

### Final Project Overview

* Passwords are hashed with bcrypt

* JWT stores admin_id and organization identifier

* Only authenticated org admins can update/delete organizations

* Clean, modular code using services, schemas, and routes
