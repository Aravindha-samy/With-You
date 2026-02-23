from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from app.model import User, MoodCheckIn, MemoryCard, EmergencyContact, AgentInteraction, CognitiveInsight, CaregiverAlert
from app.api import users, mood_checkins, memory_cards, emergency_contacts, agent_interactions, cognitive_insights, caregiver_alerts, agents
from settings import APP_TITLE, APP_DESCRIPTION, APP_VERSION

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(mood_checkins.router)
app.include_router(memory_cards.router)
app.include_router(emergency_contacts.router)
app.include_router(agent_interactions.router)
app.include_router(cognitive_insights.router)
app.include_router(caregiver_alerts.router)
app.include_router(agents.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to WithYou API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
