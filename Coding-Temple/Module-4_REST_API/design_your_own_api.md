**Pet Adoption Service - list available pets, allow applications, track adoption status**
API Design: Pet Adoption Service
Version: v1
Base URL: https://api.petadoptionservice.com/v1

Authentication: Bearer Token (JWT)
Rate Limit: 60 requests per minute

Resources - List all the things in your system (minimum 3 resources)
   1. Pets
   2. Adoptions
   3. Applications
   4. StatusHistory
   5. User

Relationships - How do they connect? (at least one one-to-many and identify any many-to-many)
    1. A pet can have many adoption applications (one to many) 
        - one application belongs to one pet
    2. A pet can have many status history records over time (one to many)
    3. A user can save many pets, and a pet can be saved by many users. (many to many)


Endpoints - Full CRUD for your primary resource, plus at least 3 endpoints for related resources. Include the HTTP method and URI for each.
    - PETS
        - POST /pets -> register a new pet listing
        - GET /pets -> lists all pets
        - GET /pets/{id} -> get pet profile
        - PUT /pets/{id} -> updates an existing pet 
        - DELETE /pets/{id} -> remove a pet profile 
        
    - Adoptions 
        - POST /adoptions -> creates a new adoptions record
        - GET /adoptions/{id} -> get all adoption details 
        - GET /adoptions -> lists all adoptions
        - DELETE /adoptions/{id} -> deletes a specific adoption 
        - PUT /adoptions/{id} -> updates adoption record

    - Applications
        - GET /applications -> List all your applications
        - POST /applications -> Create a new adoption application
        - GET /applications/{id} -> Get application details 
        - PUT /applications/{id} -> Updated existing application
        - DELETE /applications/{id} -> Deletes applications  
    - Status
        - GET /applications/{id}/statuses -> lists the status of your applications
    - User
        - POST /users -> register a new user
        - GET /users/{id} -> view a user profile
        - DELETE /users/{id} -> delete a user 
        - PUT /users/{id} -> updates a user profile 
        - POST /auth/login -> logging in as user 

Schemas - Request and response schemas for at least 2 POST endpoints and 2 GET endpoints
    - POST /pets
        -{
            "name": "String (required)",
            "breed": "String (required)",
            "age": "integer",
            "animal_type": "string", 
            "image": "image upload",
            "availability": "bool",
            "description": "String (required)"
        }
    - POST /adoptions
        -{
            "pet_id": "integer", 
            "user_id": "integer",
            "date": "date",
            "status": "string", 
            "notes": "string"
        }
    - GET /pets/{id}
        -{
            "id": "integer",
            "name": "string",
            "breed": "string",
            "description": "string", 
            "status": "string"
        }
    -GET /applications
        - { "data": [
            {
            "id": "integer",
            "user_id": "integer", 
            "email": "string",
            "message": "string",
            "status": "pending", 
            "pet_id": "integer", 
            }
        ]
        "total": "integer",
        "page": "integer",
        "per_page": "integer",
            
        }


Authentication - Which endpoints are public? Which require login? Who can access what?
    - Public 
        -GET /pets 
        -GET /pets/{id} 
                - Anyone can view available pets
        - POST /users -> register a new user
        - POST auth/login
    
    - Authenticated Users
        - GET /applications
        - GET /users/{id} -> view a user profile
        - POST /applications -> Create a new adoption application
        - GET /applications/{id} -> Get application details 
        - PUT /applications/{id} -> Updated existing application
        - DELETE /applications/{id} -> Deletes applications  
        - GET /applications/{id}/statuses -> lists the status of your applications
        - GET /adoptions/{id} -> get all adoption details 

    - Admin-only endpoints require administrator privileges.
        - POST /pets
        - PUT /pets/{id}
        - DELETE /pets/{id}
        - GET /adoptions
        - DELETE /adoptions/{id} -> deletes a specific adoption 
        - POST /adoptions -> creates a new adoptions record
        - PUT /adoptions/{id} -> updates adoption record
        - DELETE /users/{id} -> delete a user 
        - PUT /users/{id} -> updates a user profile 


Error responses - For your most important endpoint, list all possible status codes and what they mean
    - POST /applications
        - 201: Applications submitted successfully. 
        - 400: Application is empty and not filled out completely. 
        - 401: Server doesn't know who you are. 
        - 403: the server knows exactly who you are, but you're not allowed to do apply for this pet. 
        - 404: Pet doesn't exist. 
        - 409: Duplicated application already exists. 
        - 422: Application content is semantically invalid. 
        - 500: Unexpected server error. 

