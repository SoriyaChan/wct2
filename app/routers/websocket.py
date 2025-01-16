from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..models import Product_Inventory, Supplier, Product, Product_Category, OrderProductAssociation, SaleProductAssociation
from ..dependency import get_db
import json
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except (WebSocketDisconnect, RuntimeError):
                self.disconnect(connection)  # Remove the disconnected client

manager = ConnectionManager()

@router.websocket("/ws/inventory")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = db.query(Product_Inventory).all()
            inventory_data = [
                {
                    "product_inventory_id": item.product_inventory_id,
                    "product_id": item.product_id,
                    "stock": item.stock,
                    "last_updated": item.last_updated.isoformat()
                }
                for item in data
            ]
            await websocket.send_text(json.dumps(inventory_data))
            await asyncio.sleep(5)  # Broadcast every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError as e:
        if "Cannot call \"send\"" in str(e):
            # Log the error or handle it as needed
            manager.disconnect(websocket)

@router.websocket("/ws/suppliers")
async def websocket_supplier_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = db.query(Supplier).all()
            supplier_data = [
                {
                    "supplier_id": item.supplier_id,
                    "supplier_name": item.supplier_name,
                    "address": item.address,
                    "phone": item.phone
                }
                for item in data
            ]
            await websocket.send_text(json.dumps(supplier_data))
            await asyncio.sleep(5)  # Broadcast every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError as e:
        if "Cannot call \"send\"" in str(e):
            # Log the error or handle it as needed
            manager.disconnect(websocket)

@router.websocket("/ws/products")
async def websocket_product_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = db.query(Product).all()
            product_data = [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "unit_price": item.unit_price,
                    "description": item.description,
                    "min_threshold": item.min_threshold,
                    "max_threshold": item.max_threshold,
                    "supplier_id": item.supplier_id,
                    "category_id": item.category_id
                }
                for item in data
            ]
            await websocket.send_text(json.dumps(product_data))
            await asyncio.sleep(5)  # Broadcast every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError as e:
        if "Cannot call \"send\"" in str(e):
            # Log the error or handle it as needed
            manager.disconnect(websocket)

@router.websocket("/ws/categories")
async def websocket_category_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = db.query(Product_Category).all()
            category_data = [
                {
                    "category_id": item.category_id,
                    "category_name": item.category_name,
                    "description": item.description
                }
                for item in data
            ]
            await websocket.send_text(json.dumps(category_data))
            await asyncio.sleep(5)  # Broadcast every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError as e:
        if "Cannot call \"send\"" in str(e):
            # Log the error or handle it as needed
            manager.disconnect(websocket)

@router.websocket("/ws/orders")
async def websocket_order_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = db.query(OrderProductAssociation).all()
            order_data = [
                {
                    "order_id": item.order_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                }
                for item in data
            ]
            await websocket.send_text(json.dumps(order_data))
            await asyncio.sleep(5)  # Broadcast every 5 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError as e:
        if "Cannot call \"send\"" in str(e):
            # Log the error or handle it as needed
            manager.disconnect(websocket)


@router.websocket("/ws/sales")
async def websocket_sales_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            # Query all sale data from the database
            data = db.query(SaleProductAssociation).all()
            sale_data = [
                {
                    "sale_id": item.sale_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                }
                for item in data
            ]
            # Send the sale data as a JSON string to the connected WebSocket
            await websocket.send_text(json.dumps(sale_data))
            # Broadcast every 5 seconds
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except RuntimeError as e:
        if "Cannot call \"send\"" in str(e):
            # Log the error or handle it as needed
            manager.disconnect(websocket)