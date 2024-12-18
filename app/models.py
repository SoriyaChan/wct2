from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


class User(Base):
    __tablename__ = "user"
    
    userID = Column(Integer, primary_key=True, index=True)
    userName = Column(String(30), nullable=False, unique=True)
    userEmail = Column(String(30), nullable=False, unique=True)
    password = Column(String, nullable=False)

class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String(20), nullable=False)
    created_by = Column(String, nullable=False)

    products = relationship("Product", back_populates="suppliers")

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_by = Column(String, nullable=False)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)

    suppliers = relationship("Supplier", back_populates="products")
    sales = relationship("Sale", back_populates="products")

class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True, index=True)
    sold_by = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    products = relationship("Product", back_populates="sales")