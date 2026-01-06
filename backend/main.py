from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from enum import Enum
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# تنظیمات
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# دیتابیس
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# مدل دیتابیس
class RequestStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class ProjectRequest(Base):
    __tablename__ = "project_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    project_type = Column(String, nullable=True)
    budget = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic Models
class ProjectRequestCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    project_type: Optional[str] = None
    budget: Optional[str] = None
    description: str

class ProjectRequestResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    project_type: Optional[str]
    budget: Optional[str]
    description: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class StatusUpdate(BaseModel):
    status: RequestStatus

# FastAPI App
app = FastAPI(title="Resume Backend API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production محدود کنید
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.broadcast_count()
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast_count(self):
        count = len(self.active_connections)
        message = {"type": "online_count", "count": count}
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/")
async def root():
    return {"message": "Resume Backend API", "docs": "/docs"}

@app.post("/api/requests", response_model=ProjectRequestResponse)
async def create_request(request: ProjectRequestCreate, db: Session = Depends(get_db)):
    db_request = ProjectRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@app.get("/api/requests", response_model=List[ProjectRequestResponse])
async def get_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    requests = db.query(ProjectRequest).offset(skip).limit(limit).all()
    return requests

@app.get("/api/requests/{request_id}", response_model=ProjectRequestResponse)
async def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    request = db.query(ProjectRequest).filter(ProjectRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@app.patch("/api/requests/{request_id}/status", response_model=ProjectRequestResponse)
async def update_status(
    request_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    request = db.query(ProjectRequest).filter(ProjectRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = status_update.status
    db.commit()
    db.refresh(request)
    return request

@app.delete("/api/requests/{request_id}")
async def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    request = db.query(ProjectRequest).filter(ProjectRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(request)
    db.commit()
    return {"message": "Request deleted successfully"}

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    if login_data.username == ADMIN_USERNAME and login_data.password == ADMIN_PASSWORD:
        token = jwt.encode({"sub": login_data.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/online-count")
async def get_online_count():
    return {"count": len(manager.active_connections)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_count()

# Admin Page
@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    import os
    admin_path = os.path.join(os.path.dirname(__file__), "admin.html")
    with open(admin_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

