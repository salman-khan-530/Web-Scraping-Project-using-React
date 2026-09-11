from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from scraper.scraper_manager import ScraperManager


# Create FastAPI application
app = FastAPI(
    title="E-Commerce Product Scraper API",
    description="Backend API for the web scraping project",
    version="1.0.0"
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create scraper manager
scraper_manager = ScraperManager()


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "E-Commerce Product Scraper API is running!"
    }


# Product search endpoint
@app.get("/products")
def get_products(
    website: str = Query("test"),
    query: str = Query(...),
    max_products: int = Query(20, ge=1, le=100)
):
    # Check whether website is supported
    if scraper_manager.get_scraper(website) is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported website: '{website}'"
        )

    # Check whether query is empty
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    # Remove unnecessary spaces
    query = query.strip()

    try:
        # Search products using the selected scraper
        products = scraper_manager.search(
            website=website,
            query=query,
            max_products=max_products
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scraper error: {str(e)}"
        )

    # Return API response
    return {
        "website": website,
        "query": query,
        "count": len(products),
        "products": products
    }