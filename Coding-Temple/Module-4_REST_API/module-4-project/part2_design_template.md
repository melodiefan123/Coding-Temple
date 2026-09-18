# Module 4 Project — Part 2: Pet Adoption Service

**Melodie Fan**
**Date: 05/07/2026**

---

## The App: Pet Adoption Service

Design a REST API for a Pet Adoption Service application. Users can:
- Browse available pets
- Submit adoption applications
- Track application and adoption statuses
- Manage user accounts and pet listings
---
# API Information

| Field | Value |
|---|---|
| API Name | Pet Adoption Service |
| Version | v1 |
| Base URL | `https://api.petadoptionservice.com/v1` |
| Authentication | Bearer Token (JWT) |
| Rate Limit | 60 requests per minute |

---

## Section 1 — Resources

| Resource | Key Attributes |
|----------|---------------|
| Pets | id, name, breed, age, animal_type, image, availability, description |
| Adoptions | id, pet_id, user_id, date, status, notes |
| Applications | id, user_id, pet_id, email, message, status |
| StatusHistory | id, application_id, status, updated_at |
| Users | id, username, email, password, role |

---

## Section 2 — Relationships

Describe how your resources relate to each other:

- **Pet ↔ Applications**  
  A pet can have many adoption applications (one-to-many).  
  One application belongs to one pet.

- **Pet ↔ StatusHistory**  
  A pet can have many status history records over time (one-to-many).

- **User ↔ Pets**  
  A user can save many pets, and a pet can be saved by many users (many-to-many).

- **User ↔ Applications**  
  A user can submit many applications (one-to-many).

- **User ↔ Adoptions**  
  A user can complete multiple adoptions over time (one-to-many).
---

## Section 3 — Endpoints

Design at least:
- Full CRUD for pets (5 endpoints)
- 3+ endpoints for related resources
- 1+ filtering endpoint

| Method | URI | Description | Auth Required? |
|--------|-----|-------------|----------------|
| POST | /pets | Register a new pet listing | Admin |
| GET | /pets | List all pets | No |
| GET | /pets/{id} | Get pet profile | No |
| PUT | /pets/{id} | Update an existing pet | Admin |
| DELETE | /pets/{id} | Remove a pet profile | Admin |
| POST | /adoptions | Create a new adoption record | Admin |
| GET | /adoptions | List all adoptions | Admin |
| GET | /adoptions/{id} | Get adoption details | Yes |
| PUT | /adoptions/{id} | Update adoption record | Admin |
| DELETE | /adoptions/{id} | Delete adoption record | Admin |
| GET | /applications | List all applications | Yes |
| POST | /applications | Create adoption application | Yes |
| GET | /applications/{id} | Get application details | Yes |
| PUT | /applications/{id} | Update application | Yes |
| DELETE | /applications/{id} | Delete application | Yes |
| GET | /applications/{id}/statuses | Get application status history | Yes |
| POST | /users | Register a new user | No |
| GET | /users/{id} | View user profile | Yes |
| PUT | /users/{id} | Update user profile | Admin |
| DELETE | /users/{id} | Delete user | Admin |
| POST | /auth/login | User login | No |
| GET | /pets?availability=true | Filter available pets | No |


---

## Section 4 — Request/Response Schemas


## POST /pets — Create a New Pet Listing

### Request Body

```json
{
  "name": "Buddy",
  "breed": "Golden Retriever",
  "age": 3,
  "animal_type": "Dog",
  "image": "buddy.jpg",
  "availability": true,
  "description": "Friendly and energetic family dog."
}
```

**Success response (201):**
```json
{
  "id": 101,
  "name": "Buddy",
  "breed": "Golden Retriever",
  "availability": true,
  "message": "Pet listing created successfully."
}
```

### GET /pets/{id}

**Response (200):**
```json
{
  "id": 12,
  "name": "Buddy",
  "breed": "Golden Retriever",
  "description": "Friendly and energetic family dog.",
  "status": "Available"
}
```

---

## Section 5 — Authentication
| Endpoint                        | Auth Required | Notes                         |
| ------------------------------- | ------------- | ----------------------------- |
| GET /pets                       | No            | Anyone can browse pets        |
| GET /pets/{id}                  | No            | Public pet profile            |
| POST /users                     | No            | User registration             |
| POST /auth/login                | No            | User login                    |
| GET /applications               | Yes           | Requires authenticated user   |
| POST /applications              | Yes           | User must be logged in        |
| GET /applications/{id}          | Yes           | User can view own application |
| GET /applications/{id}/statuses | Yes           | User can track status         |
| GET /adoptions/{id}             | Yes           | Authenticated users only      |
| POST /pets                      | Admin Only    | Admin privileges required     |
| PUT /pets/{id}                  | Admin Only    | Admin privileges required     |
| DELETE /pets/{id}               | Admin Only    | Admin privileges required     |
| GET /adoptions                  | Admin Only    | Restricted access             |
| DELETE /users/{id}              | Admin Only    | Restricted access             |

---
**Auth method and rationale:**
This API uses JWT Bearer Token authentication.
JWT tokens allow secure stateless authentication between clients and the server. Public endpoints are available without authentication, while sensitive actions such as creating pet listings or managing adoptions require authenticated or administrator access.



---

## Section 6 — Error Responses for POST /applications

| Status Code | When it Occurs                                      |
| ----------- | --------------------------------------------------- |
| 201         | Application submitted successfully                  |
| 400         | Application request body is missing required fields |
| 401         | User is not authenticated                           |
| 403         | User is authenticated but not allowed to apply      |
| 404         | Pet does not exist                                  |
| 409         | Duplicate application already exists                |
| 422         | Application data is semantically invalid            |
| 500         | Unexpected server error                             |

