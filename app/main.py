from fastapi import FastAPI
from .routers import supplier, user, product, sale, order, websocket
from .database import engine, Base, SessionLocal
from .models import User
import hashlib
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(supplier.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(sale.router)
app.include_router(websocket.router)

def initialize_database():
    session = SessionLocal()
    try:
        user_email = 'admin@gmail.com'
        hash_password = hashlib.sha512('12345'.encode()).hexdigest()

        # Check if the user already exists
        if not session.query(User).filter(User.userEmail == user_email).first():
            # Add the admin user if not exists
            initial_user = User(
                userName='soriya',
                userEmail=user_email,
                password=hash_password,
                role='admin'
            )
            session.add(initial_user)
            session.commit()
            print("Admin user added successfully.")
        else:
            print(f"Admin user with email {user_email} already exists.")
    finally:
        session.close()

# Initialize the database with admin user
initialize_database()