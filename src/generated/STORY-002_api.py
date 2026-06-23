from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import List
from datetime import datetime
import asyncio

app = FastAPI(title="Real-time Stock Updates")

class StockUpdate(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    change_percent: float

active_connections: List[WebSocket] = []

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "realtime-stocks"}

@app.websocket("/ws/stock-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            symbol = data.get("symbol")
            for connection in active_connections:
                await connection.send_json({
                    "symbol": symbol,
                    "message": f"Subscribed to {symbol}"
                })
    except Exception as e:
        active_connections.remove(websocket)
        await websocket.close()

@app.post("/stock/update")
async def update_stock(update: StockUpdate):
    for connection in active_connections:
        await connection.send_json(update.dict())
    return {"status": "broadcasted"}

@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    return {"symbol": symbol, "price": 100.0, "timestamp": datetime.now()}
