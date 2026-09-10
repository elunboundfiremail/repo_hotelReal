from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as room_router

app = FastAPI(
    title="Hotel Real API",
    description="Layered API for room management",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(room_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
