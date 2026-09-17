from sqlalchemy import create_engine, String, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional

engine = create_engine("sqlite:///product_catalog.db", echo = True)

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__= "categories"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}')"

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_name: Mapped[str] = mapped_column(String(100))
    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, in_stock={self.in_stock}, category = {self.category_name})"

Base.metadata.create_all(engine)

with Session(engine) as session: 
    # Categories to add 
    electronics = Category(name="Electronics", description="Gadgets and devices")
    accessories = Category(name="Accessories", description="Add-ons and peripherals")
    storage = Category(name="Storage", description="Drives and memory devices")
   
    # Products to add
    mouse = Product(name="Wireless Mouse", price=29.99, in_stock=True, category_name="Accessories")
    keyboard = Product(name="Mechanical Keyboard", price=89.99, in_stock=True, category_name="Accessories")
    usbc = Product(name="USB-C Hub", price=34.99, in_stock=False, category_name="Accessories")
    monitor = Product(name="27-inch Monitor", price=299.99, in_stock=True, category_name="Electronics")
    flash_drive = Product(name="Flash Drive 64GB", price=12.99, in_stock=True, category_name="Storage")
    ssd = Product(name="External SSD 1TB", price=89.99, in_stock=True, category_name="Storage")
    # Staging for insert    
    session.add_all([electronics, accessories, storage, mouse, keyboard, usbc, monitor, flash_drive, ssd])
    session.commit()
    
#Querying
with Session(engine) as session: 
    print("\nAll Categories")
    categories = session.query(Category).all()
    for category in categories: 
        print(f" {category}")
    
    print("\n In Stock Products")
    products = session.query(Product).filter_by(in_stock =True)
    for product in products:
        print(f" {product}")

    print("\n Products under $50")
    product_price = session.query(Product).filter(Product.price < 50)
    for products in product_price: 
        print(f" {products}")


#Model Inspector
inspector = inspect(engine)

#List all tables
print("Tables:", inspector.get_table_names())

#Get column details for specific table 
for column in inspector.get_columns("products"):
    print(f" {column['name']}: {column['type']} (nullable={column['nullable']})")

