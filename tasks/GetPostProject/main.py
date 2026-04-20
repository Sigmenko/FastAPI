from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

class Order(BaseModel):
    id: int
    item_name: str
    price: float
    quantity: int
    is_delivered: bool = False
    priority: str

class OrderCreate(BaseModel):
    item_name: str
    price: float
    quantity: int

orders_db = []

@app.post('/orders/new')
async def new_orders(order:OrderCreate) -> Order:
    total = order.price * order.quantity
    new_order_priority = "Low"
    if total > 5000:
        new_order_priority = "High"
    new_order_id = len(orders_db) + 1
    new_order_data = {'id': new_order_id, 'item_name': order.item_name, 'price':order.price, 'quantity': order.quantity, 'is_delivered': False,'priority': new_order_priority}
    orders_db.append(new_order_data)

    return Order(**new_order_data)

@app.get('/orders/stats')
async def stats() -> dict:
    count = len(orders_db)
    revenue = 0
    for order in orders_db:
        revenue += order['price'] * order['quantity']
    print(f'Count of orders {count}, genereal revenue {revenue}')
    return {
        "total_revenue": revenue,
        "orders_count": count
    }

@app.put('/orders/{order_id}/deliver')
async def status_deliver(order_id:int) -> Dict:
    for order in orders_db:
        if order['id'] == order_id:
            order['is_delivered'] = True
            return Order(**order)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='order not found ')






