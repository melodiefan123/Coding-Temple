# LedgeAI: Freelance Budget Tracker & Financial Assistant

LedgeAI is an intelligent, local-first financial assistant and budget tracker engineered specifically for freelance professionals. It automates receipt parsing, client invoice generation, dynamic self-employment tax estimation, and real-time discretionary budget tracking.

---

## 1. Project Overview & Proposal

### Description

An intelligent financial assistant and budget tracker that automates invoice generation, receipt capture, tax estimations, and dynamic monthly runway calculations for freelance professionals.

### User Story

> "As a **freelance professional with fluctuating monthly income**, I want to **automatically track expenses, instantly generate invoices, and project my available tax-adjusted budget** so that **I can maintain consistent cash flow and avoid surprise tax liabilities without manual spreadsheet math.**"

### Required Components Checklist

- **FastAPI Backend (5 Endpoints):**
  - `POST /auth/token`: Handles user authentication and secure session token generation.
  - `POST /receipts/upload`: Receives receipt images/PDFs, triggers an LLM parsing pipeline, and extracts line items.
  - `POST /invoices/generate`: Accepts milestone parameters and builds structural schema for professional PDF generation.
  - `GET /budget/status`: Computes dynamic runway, calculating metrics based on pending invoices, current cash, and automated tax withholding logic.
  - `GET /documents`: Fetches chronological financial items (invoices and parsed receipts).
- **Vector Database (ChromaDB):**
  - Stores vectorized document embeddings of parsed receipts, historical invoices, and localized tax guidelines. Enables semantic querying (e.g., _"How much did I spend on software subscriptions last quarter?"_).
- **Streamlit Frontend:**
  - Provides a clean dashboard featuring an interactive file uploader for receipts, an intuitive invoice creation form, visual progress rings tracking annual budget goals, and an AI chat interface for ad-hoc financial questions.

### Tech Stack Confirmation

- **Backend Framework:** FastAPI (Python 3.11)
- **ORM & Database Layer:** SQLAlchemy connecting to a local SQLite database (storing structural tables for user profiles, baseline budgets, and transaction metadata).
- **Vector Search & Embeddings:** ChromaDB storing dense vector representations of textual financial documents.
- **Local AI Inference:** Ollama running localized models (`llama3` for conversational analysis and `nomic-embed-text` for embeddings).
- **User Interface:** Streamlit for a fast, responsive, and data-focused web application layer.
- **Containerization:** Docker & Docker Compose orchestrating individual services into an isolated ecosystem.

---

## 2. API Endpoint Directory

All endpoints (except authentication) require a valid JSON Web Token (JWT) sent in the HTTP Request Authorization header: `Authorization: Bearer <JWT_TOKEN>`.

| Method   | Endpoint             | Auth Required | Request Payload / Params                  | Response Summary                                                                                                                 |
| :------- | :------------------- | :-----------: | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **POST** | `/auth/token`        |     ❌ No     | Form Data: `username`, `password`         | Returns JWT access token and token type (`Bearer`).                                                                              |
| **POST** | `/receipts/upload`   |    🔒 Yes     | Multipart Form: `file: UploadFile`        | Automatically processes OCR, extracts pricing/merchant, inserts into ChromaDB + SQLite, returns structured receipt JSON.         |
| **POST** | `/invoices/generate` |    🔒 Yes     | JSON: `client_name`, `amount`, `due_date` | Generates a clean PDF invoice file, writes invoice record to DB, returns unique document identifiers.                            |
| **GET**  | `/budget/status`     |    🔒 Yes     | _None_                                    | Calculates and returns: `gross_income_received`, `tax_withholding_reserve`, `total_expenses_logged`, and `safe_spending_budget`. |
| **GET**  | `/documents`         |    🔒 Yes     | Query: `limit: int` (Optional)            | Returns a chronological feed stream of all receipt and invoice document metadata.                                                |

---

## 3. System Architecture Diagram

````ascii
                             +-------------------+
                             |   Client / Web    |
                             |  (React/Next.js)  |
                             +---------+---------+
                                       |
                                HTTP / REST
                                       |
                                       v
+-------------------------------------------------------------------------------+
| FastAPI Application                                                           |
|                                                                               |
|  +--------------------+  +----------------------+  +-----------------------+  |
|  |    Auth Router     |  |   Statement Router   |  |    Expense Router     |  |
|  | (/auth/token)      |  | (/statement/upload)  |  | (/expenses/...)       |  |
|  +---------+----------+  +----------+-----------+  +-----------+-----------+  |
|            |                        |                      |                  |
|            +------------------------+----------------------+                  |
|                                     |                                         |
|                 +-------------------+-------------------+                     |
|                 |                                       |                     |
|                 v                                       v                     |
|      +---------------------+                 +--------------------+           |
|      |   SQLAlchemy ORM    |                 |   ChromaDB Vector  |           |
|      +----------+----------+                 +----------+---------+           |
+-----------------|---------------------------------------|---------------------+
                  |                                       |                     |
              SQL / DB                                Embeddings                |
                  |                                       |                     |
                  v                                       v                     |
        +-------------------+                   +-------------------+           |
        |  SQLite Database  |                   | Local VectorStore |           |
        |    (ledgeai.db)   |                   |     (ChromaDB)    |           |
        +-------------------+                   +-------------------+           |
````
## 4. Entity-Relationship (ER) Diagram

Table users {
  id integer [primary key]
  email varchar [unique, not null]
  hashed_password varchar [not null]
  created_at timestamp [default: `now()`]
}

Table statements {
  id integer [primary key]
  user_id integer [not null, ref: > users.id]
  filename varchar [not null]
  file_type varchar [not null]
  uploaded_at timestamp [default: `now()`]
}

Table invoices {
  id integer [primary key]
  user_id integer [not null, ref: > users.id]
  statement_id integer [nullable, ref: > statements.id]
  client_name varchar [not null]
  amount float [not null]
  due_date date [not null]
  status varchar [default: 'pending']
  created_at timestamp [default: `now()`]
}

Table receipts {
  id integer [primary key]
  user_id integer [not null, ref: > users.id]
  statement_id integer [nullable, ref: > statements.id]
  merchant varchar [not null]
  amount float [not null]
  category varchar [not null]
  purchase_date date [not null]
  chroma_doc_id varchar [nullable]
  created_at timestamp [default: `now()`]
}

Table expenses {
  id integer [primary key]
  user_id integer [not null, ref: > users.id]
  card_id integer [nullable]
  amount float [not null]
  description varchar [not null]
  category varchar [not null]
  date date [not null]
  created_at timestamp [default: `now()`]
}

# LedgeAI: Quick Start Guide

This guide gets you up and running with LedgeAI—both locally or inside Docker containers.

---

## Prerequisites

Before starting, ensure you have the following installed on your host machine:

* **Python 3.11+**

* **Docker & Docker Compose** (if using containerized setup)

* **Ollama** (for local AI models)

---

## Configuration Variables

Create an `.env` file in your root project directory with the following variables:

```env

DATABASE_URL=sqlite:///./data/ledgeai.db

CHROMADB_PATH=./data/chroma

OLLAMA_HOST=http://localhost:11434

BACKEND_API_URL=http://localhost:8000

````
