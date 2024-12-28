from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..models import Product_Inventory
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
