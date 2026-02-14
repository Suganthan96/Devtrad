"""
NinjaQuant - Injective Strategy Backtesting API

A modular, production-ready backtesting API built on Injective's market data.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from app.api import router
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include API routes
app.include_router(router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info(f"Starting {settings.APP_TITLE} v{settings.APP_VERSION}")
    logger.info(f"Injective Network: {settings.INJECTIVE_NETWORK}")
    logger.info(f"Data Mode: {'Real' if settings.USE_REAL_DATA else 'Synthetic'}")
    logger.info("API Documentation available at /docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down NinjaQuant API")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
