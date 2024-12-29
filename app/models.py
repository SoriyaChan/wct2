from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Float
from sqlalchemy.orm import relationship
from .database import Base

OrderProductAssociation = Table(
    "Order_Product_Association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("Orderr.order_id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("Product.product_id"), primary_key=True),
    Column("quantity", Integer, nullable=False),  
    Column("unit_price", Float, nullable=False),
)

SaleProductAssociation = Table(
    "Sale_Product_Association",
    Base.metadata,
    Column("sale_id", Integer, ForeignKey("Sale.sale_id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("Product.product_id"), primary_key=True),
    Column("quantity", Integer, nullable=False),  
    Column("unit_price", Float, nullable=False),
)

class User(Base):
    __tablename__ = "User"
    
    userID = Column(Integer, primary_key=True, index=True)
    userName = Column(String(30), nullable=False, unique=True)
    userEmail = Column(String(30), nullable=False, unique=True)
    password = Column(String, nullable=False)

class Supplier(Base):
    __tablename__ = "Supplier"

    supplier_id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, index=True, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String(20), nullable=False)
    created_by = Column(String, nullable=False)

    products = relationship("Product", back_populates="suppliers")

class Product(Base):
    __tablename__ = "Product"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True, nullable=False)
    unit_price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    min_threshold = Column(Integer, nullable=False)
    max_threshold = Column(Integer, nullable=False)
    created_by = Column(String, nullable=False)
    supplier_id = Column(Integer, ForeignKey("Supplier.supplier_id"), nullable=False)

    suppliers = relationship("Supplier", back_populates="products")
    sales = relationship("Sale", secondary=SaleProductAssociation, back_populates="products")
    product_inventories = relationship("Product_Inventory", back_populates="products")

class Product_Inventory(Base):
    __tablename__ = "Product_Inventory"

    product_inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Product.product_id"), nullable=False)
    stock = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    products = relationship("Product", back_populates="product_inventories")

class Order(Base):
    __tablename__ = "Orderr"

    order_id = Column(Integer, primary_key=True, index=True)
    order_by = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)

class Sale(Base):
    __tablename__ = "Sale"

    sale_id = Column(Integer, primary_key=True, index=True)
    sold_by = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False)

    products = relationship("Product", secondary=SaleProductAssociation, back_populates="sales")