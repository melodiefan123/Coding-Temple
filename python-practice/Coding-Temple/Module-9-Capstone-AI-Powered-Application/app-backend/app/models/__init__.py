# Import the base and every model so SQLAlchemy registers them completely
from app.database import Base
from .user import User
from .invoice import Invoice
from .receipt import Receipt
from .budget import Budget
from .income import Income

# Explicitly expose them for easy backend importing
__all__ = ["Base", "User", "Invoice", "Receipt", "Budget", "Income"]