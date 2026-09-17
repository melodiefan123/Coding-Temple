from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import auth, invoice, receipt, rag, budget, income, metrics, card, subscription, statement
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="LedgeAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or explicitly ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(invoice.router)
app.include_router(receipt.router)
app.include_router(rag.router)
app.include_router(budget.router)
app.include_router(income.router)
app.include_router(metrics.router)
app.include_router(card.router)
app.include_router(subscription.router)
app.include_router(statement.router)



@app.get("/")
def read_root():
    return {"message": "LedgeAI API is running!"}