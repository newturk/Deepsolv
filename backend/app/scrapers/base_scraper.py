import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import time
import random
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class BaseScraper:
    """Base class for all scrapers with common functionality"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_page(self, url: str, delay: float = 1.0) -> Optional[BeautifulSoup]:
        """Fetch a web page and return BeautifulSoup object"""
        try:
            # Add random delay to be respectful
            time.sleep(delay + random.uniform(0, 1))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html5lib')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def get_json(self, url: str, delay: float = 1.0) -> Optional[Dict[str, Any]]:
        """Fetch JSON data from a URL"""
        try:
            time.sleep(delay + random.uniform(0, 1))
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching JSON from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching JSON from {url}: {e}")
            return None
    
    def normalize_url(self, base_url: str, url: str) -> str:
        """Normalize relative URLs to absolute URLs"""
        if url.startswith('http'):
            return url
        return urljoin(base_url, url)
    
    def extract_text(self, element) -> str:
        """Extract clean text from a BeautifulSoup element"""
        if element is None:
            return ""
        
        # Remove script and style elements
        for script in element(["script", "style"]):
            script.decompose()
        
        text = element.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def is_shopify_store(self, url: str) -> bool:
        """Check if a URL is a Shopify store"""
        try:
            # Check for common Shopify indicators
            shopify_indicators = [
                '/products.json',
                'myshopify.com',
                'shopify',
                'cdn.shopify.com'
            ]
            
            # Check products.json endpoint
            products_url = url.rstrip('/') + '/products.json'
            response = self.session.get(products_url, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'products' in data:
                        return True
                except:
                    pass
            
            # Check HTML content for Shopify indicators
            soup = self.get_page(url)
            if soup:
                html_content = str(soup).lower()
                return any(indicator in html_content for indicator in shopify_indicators)
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking if {url} is Shopify store: {e}")
            return False
    
    def extract_meta_content(self, soup: BeautifulSoup, property_name: str) -> Optional[str]:
        """Extract content from meta tags"""
        meta = soup.find('meta', property=property_name)
        if meta:
            return meta.get('content')
        
        meta = soup.find('meta', attrs={'name': property_name})
        if meta:
            return meta.get('content')
        
        return None
