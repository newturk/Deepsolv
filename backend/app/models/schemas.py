from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class InsightRequest(BaseModel):
    """Request model for fetching store insights"""
    website_url: HttpUrl = Field(..., description="Shopify store URL to analyze")

class Product(BaseModel):
    """Product information model"""
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    available: Optional[bool] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None

class Policy(BaseModel):
    """Policy information model"""
    privacy_policy: Optional[str] = None
    return_policy: Optional[str] = None
    refund_policy: Optional[str] = None
    shipping_policy: Optional[str] = None
    terms_of_service: Optional[str] = None

class FAQ(BaseModel):
    """FAQ item model"""
    question: str
    answer: str
    category: Optional[str] = None

class SocialHandle(BaseModel):
    """Social media handle model"""
    platform: str
    handle: str
    url: Optional[str] = None

class ContactInfo(BaseModel):
    """Contact information model"""
    emails: List[str] = []
    phone_numbers: List[str] = []
    addresses: List[str] = []
    contact_form_url: Optional[str] = None

class ImportantLink(BaseModel):
    """Important link model"""
    title: str
    url: str
    description: Optional[str] = None

class Competitor(BaseModel):
    """Competitor information model"""
    name: str
    website_url: str
    description: Optional[str] = None
    insights: Optional['StoreInsights'] = None

class StoreInsights(BaseModel):
    """Complete store insights model"""
    brand_name: str
    website_url: str
    products: List[Product] = []
    hero_products: List[Product] = []
    policies: Policy = Policy()
    faqs: List[FAQ] = []
    social_handles: List[SocialHandle] = []
    contact_info: ContactInfo = ContactInfo()
    brand_context: Optional[str] = None
    important_links: List[ImportantLink] = []
    competitors: List[Competitor] = []
    scraped_at: datetime = Field(default_factory=datetime.now)
    total_products: int = 0
    store_theme: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None

class InsightResponse(BaseModel):
    """API response model"""
    success: bool
    data: Optional[StoreInsights] = None
    error: Optional[str] = None
    message: Optional[str] = None
    processing_time: Optional[float] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    message: str
    status_code: int

# Update forward references
StoreInsights.model_rebuild()
