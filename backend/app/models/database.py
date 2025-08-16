from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database configuration - Use SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./shopify_insights.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Store(Base):
    """Store information table"""
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(255), nullable=False)
    website_url = Column(String(500), unique=True, nullable=False)
    store_theme = Column(String(100))
    currency = Column(String(10))
    language = Column(String(10))
    brand_context = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="store")
    policies = relationship("Policy", back_populates="store", uselist=False)
    faqs = relationship("FAQ", back_populates="store")
    social_handles = relationship("SocialHandle", back_populates="store")
    contact_info = relationship("ContactInfo", back_populates="store", uselist=False)
    important_links = relationship("ImportantLink", back_populates="store")
    competitors = relationship("Competitor", back_populates="store")

class Product(Base):
    """Product information table"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    shopify_id = Column(Integer)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    price = Column(String(50))
    currency = Column(String(10))
    image_url = Column(String(500))
    product_url = Column(String(500))
    available = Column(Boolean, default=True)
    tags = Column(Text)  # JSON string
    category = Column(String(100))
    is_hero_product = Column(Boolean, default=False)
    
    # Relationships
    store = relationship("Store", back_populates="products")

class Policy(Base):
    """Policy information table"""
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=True)
    privacy_policy = Column(Text)
    return_policy = Column(Text)
    refund_policy = Column(Text)
    shipping_policy = Column(Text)
    terms_of_service = Column(Text)
    
    # Relationships
    store = relationship("Store", back_populates="policies")

class FAQ(Base):
    """FAQ information table"""
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100))
    
    # Relationships
    store = relationship("Store", back_populates="faqs")

class SocialHandle(Base):
    """Social media handles table"""
    __tablename__ = "social_handles"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    platform = Column(String(50), nullable=False)
    handle = Column(String(100), nullable=False)
    url = Column(String(500))
    
    # Relationships
    store = relationship("Store", back_populates="social_handles")

class ContactInfo(Base):
    """Contact information table"""
    __tablename__ = "contact_info"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=True)
    emails = Column(Text)  # JSON string
    phone_numbers = Column(Text)  # JSON string
    addresses = Column(Text)  # JSON string
    contact_form_url = Column(String(500))
    
    # Relationships
    store = relationship("Store", back_populates="contact_info")

class ImportantLink(Base):
    """Important links table"""
    __tablename__ = "important_links"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text)
    
    # Relationships
    store = relationship("Store", back_populates="important_links")

class Competitor(Base):
    """Competitor information table"""
    __tablename__ = "competitors"
    
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    name = Column(String(200), nullable=False)
    website_url = Column(String(500), nullable=False)
    description = Column(Text)
    
    # Relationships
    store = relationship("Store", back_populates="competitors")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
