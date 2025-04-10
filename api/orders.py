from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from middleware.dependencies import get_db, get_current_user
from services.order import OrderService, OrderCreate, OrderUpdate
from validators.orders import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

# Endpoint: Create a new order for the logged-in customer
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = OrderService(db)
    # The order is created under the currently logged-in customer's ID
    order = service.create_order(current_user.id, order_data)
    return order

# Endpoint: List orders placed by the currently logged-in customer
@router.get("/me", response_model=list[OrderResponse])
def list_my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = OrderService(db)
    # Fetch orders placed by the currently logged-in user (using current_user.id)
    orders = service.list_orders_by_user(current_user.id)
    return orders

# Endpoint: List orders placed by a specific user (Admin only)
@router.get("/users/{user_id}", response_model=list[OrderResponse])
def list_orders_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    service = OrderService(db)
    orders = service.list_orders_by_user(user_id)
    return orders

# Endpoint: List all orders (Admin only)
@router.get("/", response_model=list[OrderResponse])
def list_all_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    service = OrderService(db)
    orders = service.list_all_orders()  # Returns a list of orders from the DB
    return orders

# Endpoint: Retrieve order details by ID (Admin or customer who owns the order)
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Allow access if the user is an admin or if they own the order
    if current_user.role != "admin" and current_user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return order

# Endpoint: Update order details by ID (Admin or the owner)
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and current_user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_order = service.update_order(order_id, order_data)
    return updated_order

# Endpoint: Delete an order by ID (Admin or the owner)
@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and current_user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    success = service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not delete order")
    return {"message": f"Order with ID: {order_id} has been deleted"}