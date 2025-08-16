from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .models.schemas import InsightRequest, InsightResponse, ErrorResponse
from .services.insight_service import InsightService
from .models.database import create_tables
import logging
import time
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Shopify Store Insights Fetcher",
    description="A comprehensive API for extracting insights from Shopify stores without using the official API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
insight_service = InsightService()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        # Try to create database tables (optional for development)
        create_tables()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.warning(f"Database initialization failed (this is OK for development): {e}")
    
    logging.info("Application started successfully")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Shopify Store Insights Fetcher API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "insights": "/api/insights"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/insights", response_model=InsightResponse)
async def get_store_insights(request: InsightRequest):
    """
    Extract comprehensive insights from a Shopify store
    
    This endpoint fetches:
    - Product catalog and hero products
    - Privacy, return, and refund policies
    - FAQs and brand information
    - Social media handles
    - Contact information
    - Important links
    - Competitor analysis (bonus feature)
    """
    start_time = time.time()
    
    try:
        # Validate the website URL
        if not insight_service.validate_website_url(str(request.website_url)):
            raise HTTPException(
                status_code=400,
                detail="Invalid website URL or not a Shopify store"
            )
        
        # Extract insights
        store_insights = await insight_service.get_store_insights(str(request.website_url))
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Return successful response
        return InsightResponse(
            success=True,
            data=store_insights,
            message="Insights extracted successfully",
            processing_time=processing_time
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error in insights endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while processing your request"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=exc.detail,
            message="Request failed",
            status_code=exc.status_code
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal server error",
            message="An unexpected error occurred",
            status_code=500
        ).dict()
    )

# Additional utility endpoints
@app.get("/api/validate-url")
async def validate_url(url: str):
    """Validate if a URL is a Shopify store"""
    try:
        is_valid = insight_service.validate_website_url(url)
        return {
            "url": url,
            "is_shopify_store": is_valid,
            "valid": is_valid
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error validating URL: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
