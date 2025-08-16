from .base_scraper import BaseScraper
from ..models.schemas import Product
from typing import List, Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class ProductScraper(BaseScraper):
    """Scraper for extracting product information from Shopify stores"""
    
    def __init__(self):
        super().__init__()
    
    def get_all_products(self, base_url: str) -> List[Product]:
        """Fetch all products from a Shopify store"""
        products = []
        
        try:
            # Try Shopify products endpoint first with pagination
            products = self._fetch_all_products_with_pagination(base_url)
            
            if products:
                logger.info(f"Successfully extracted {len(products)} products from products.json")
                return products
            
            # If products.json doesn't work, try to extract from main page
            logger.info(f"No products found at products.json, trying to extract from main page")
            products = self._extract_products_from_main_page(base_url)
            
        except Exception as e:
            logger.error(f"Error fetching products from {base_url}: {e}")
            # Fallback to main page extraction
            products = self._extract_products_from_main_page(base_url)
        
        return products

    def _fetch_all_products_with_pagination(self, base_url: str) -> List[Product]:
        """Fetch all products using pagination from Shopify products.json endpoint"""
        all_products = []
        page = 1
        limit = 250  # Shopify allows up to 250 products per page
        
        try:
            while True:
                # Construct URL with pagination parameters
                products_url = f"{base_url.rstrip('/')}/products.json?page={page}&limit={limit}"
                logger.info(f"Fetching products page {page} from {products_url}")
                
                products_data = self.get_json(products_url)
                
                if not products_data or 'products' not in products_data:
                    logger.info(f"No more products found at page {page}")
                    break
                
                page_products = products_data['products']
                if not page_products:
                    logger.info(f"No products in page {page}")
                    break
                
                logger.info(f"Found {len(page_products)} products on page {page}")
                
                # Parse products from this page
                for product_data in page_products:
                    try:
                        product = self._parse_product(product_data, base_url)
                        if product:
                            all_products.append(product)
                    except Exception as e:
                        logger.error(f"Error parsing product {product_data.get('id', 'unknown')}: {e}")
                        continue
                
                # Check if we've reached the end
                if len(page_products) < limit:
                    logger.info(f"Reached last page (page {page}) with {len(page_products)} products")
                    break
                
                page += 1
                
                # Safety check to prevent infinite loops
                if page > 100:  # Maximum 100 pages (25,000 products)
                    logger.warning(f"Reached maximum page limit ({page}), stopping pagination")
                    break
                
                # Add a small delay between requests to be respectful
                import time
                time.sleep(0.5)
            
            logger.info(f"Total products fetched: {len(all_products)}")
            return all_products
            
        except Exception as e:
            logger.error(f"Error during pagination: {e}")
            return all_products

    def _extract_products_from_main_page(self, base_url: str) -> List[Product]:
        """Extract products from the main page when products.json is not available"""
        products = []
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return products
            
            # Look for product-like elements
            product_elements = []
            
            # Common product selectors
            selectors = [
                '[class*="product"]',
                '[class*="item"]',
                '[class*="card"]',
                '[data-product-id]',
                '[data-product]',
                '.product',
                '.item',
                '.card',
                # Additional selectors for different store structures
                '[class*="grid"]',
                '[class*="collection"]',
                '[class*="catalog"]',
                '[class*="listing"]',
                '.grid-item',
                '.collection-item',
                '.catalog-item',
                # More specific Shopify selectors
                '.product-grid-item',
                '.collection-grid-item',
                '.product-tile',
                '.product-card',
                '.product-item',
                '.product-block',
                '.product-box',
                '.product-wrapper'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                product_elements.extend(elements)
            
            # Remove duplicates
            seen = set()
            unique_elements = []
            for elem in product_elements:
                if elem not in seen:
                    seen.add(elem)
                    unique_elements.append(elem)
            
            # Extract product info from each element
            for element in unique_elements[:50]:  # Increase limit to get more products
                try:
                    product = self._extract_hero_product(element, base_url)
                    if product and product.title and len(product.title.strip()) > 3:
                        # Check for duplicates more efficiently
                        title_lower = product.title.lower().strip()
                        if not any(p.title.lower().strip() == title_lower for p in products):
                            products.append(product)
                except Exception as e:
                    continue
            
            logger.info(f"Extracted {len(products)} products from main page")
            
        except Exception as e:
            logger.error(f"Error extracting products from main page: {e}")
        
        return products
    
    def get_hero_products(self, base_url: str) -> List[Product]:
        """Extract hero products from the homepage"""
        hero_products = []
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return hero_products
            
            # Common selectors for hero products
            hero_selectors = [
                '.hero-product',
                '.featured-product',
                '.main-product',
                '.hero .product',
                '.banner .product',
                '[data-product-id]',
                '.product-card',
                '.product-item',
                '.product',
                '.item',
                '[class*="product"]',
                '[class*="item"]'
            ]
            
            for selector in hero_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements[:10]:  # Increase limit to get more potential hero products
                        try:
                            product = self._extract_hero_product(element, base_url)
                            if product and product.title and len(product.title.strip()) > 3:
                                hero_products.append(product)
                        except Exception as e:
                            logger.error(f"Error extracting hero product: {e}")
                            continue
            
            # If no hero products found with selectors, try to find products in main content
            if not hero_products:
                hero_products = self._find_products_in_main_content(soup, base_url)
            
            # Filter and sort hero products to show the best ones on overview
            if hero_products:
                hero_products = self._filter_and_sort_hero_products(hero_products)
            
            logger.info(f"Found {len(hero_products)} high-quality hero products on {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting hero products from {base_url}: {e}")
        
        return hero_products

    def _filter_and_sort_hero_products(self, hero_products: List[Product]) -> List[Product]:
        """Filter and sort hero products to show the best ones on overview"""
        if not hero_products:
            return hero_products
        
        # Score each product based on quality indicators
        scored_products = []
        for product in hero_products:
            score = 0
            
            # Higher score for products with more complete information
            if product.title and len(product.title.strip()) > 5:
                score += 10
            
            if product.description and len(product.description.strip()) > 20:
                score += 8
            
            if product.image_url:
                score += 6
            
            if product.price:
                score += 4
            
            if product.product_url:
                score += 3
            
            # Bonus for products with tags or categories
            if product.tags and len(product.tags) > 0:
                score += 2
            
            if product.category:
                score += 2
            
            scored_products.append((product, score))
        
        # Sort by score (highest first) and return top products
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 8-12 products for overview (depending on quality)
        top_products = [p[0] for p in scored_products[:12]]
        
        # If we have many high-quality products, show more
        high_quality_count = sum(1 for _, score in scored_products if score >= 15)
        if high_quality_count > 8:
            top_products = [p[0] for p in scored_products[:high_quality_count]]
        
        logger.info(f"Filtered {len(hero_products)} hero products to {len(top_products)} high-quality products")
        return top_products

    def _parse_product(self, product_data: Dict[str, Any], base_url: str) -> Optional[Product]:
        """Parse product data from Shopify JSON response"""
        try:
            # Get main product image
            image_url = None
            if product_data.get('images'):
                image_url = self.normalize_url(base_url, product_data['images'][0]['src'])
            
            # Get product URL
            product_url = None
            if product_data.get('handle'):
                product_url = f"{base_url.rstrip('/')}/products/{product_data['handle']}"
            
            # Get price information
            price = None
            currency = None
            if product_data.get('variants'):
                variant = product_data['variants'][0]
                if variant.get('price'):
                    price = variant['price']
                    currency = variant.get('currency', 'USD')
            
            # Get tags
            tags = []
            if product_data.get('tags'):
                if isinstance(product_data['tags'], str):
                    tags = [tag.strip() for tag in product_data['tags'].split(',') if tag.strip()]
                elif isinstance(product_data['tags'], list):
                    tags = [str(tag).strip() for tag in product_data['tags'] if tag]
            
            # Get category from product type
            category = product_data.get('product_type')
            
            return Product(
                id=product_data.get('id'),
                title=product_data.get('title', ''),
                description=product_data.get('body_html', ''),
                price=price,
                currency=currency,
                image_url=image_url,
                product_url=product_url,
                available=product_data.get('published_at') is not None,
                tags=tags,
                category=category
            )
            
        except Exception as e:
            logger.error(f"Error parsing product data: {e}")
            return None
    
    def _extract_hero_product(self, element, base_url: str) -> Optional[Product]:
        """Extract product information from a hero product element"""
        try:
            # Try to find product title - be more flexible
            title_selectors = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                '.product-title', '.title', '.name', '.product-name',
                '[class*="title"]', '[class*="name"]', '[class*="product"]',
                # More specific title selectors
                '.product-title-text',
                '.product-name-text',
                '.item-title',
                '.card-title',
                '.grid-item-title',
                '.collection-item-title'
            ]
            
            title = ''
            for selector in title_selectors:
                title_elem = element.find(selector)
                if title_elem:
                    title = self.extract_text(title_elem)
                    if title and len(title.strip()) > 2:  # Ensure title is meaningful
                        break
            
            # If no title found, try to get text from the element itself
            if not title:
                title = self.extract_text(element)
                # Clean up the title
                title = title.split('\n')[0].strip()[:100]  # Take first line, limit length
            
            if not title or len(title.strip()) < 2:
                return None
            
            # Try to find product description
            desc_selectors = ['p', '.description', '.desc', '.product-desc', '[class*="desc"]']
            description = ''
            for selector in desc_selectors:
                desc_elem = element.find(selector)
                if desc_elem:
                    description = self.extract_text(desc_elem)
                    if description and len(description.strip()) > 10:
                        break
            
            # Try to find product image
            img_elem = element.find('img')
            image_url = None
            if img_elem and img_elem.get('src'):
                src = img_elem.get('src')
                if src and not src.startswith('data:'):  # Skip data URLs
                    image_url = self.normalize_url(base_url, src)
            
            # Try to find product link
            link_elem = element.find('a')
            product_url = None
            if link_elem and link_elem.get('href'):
                href = link_elem.get('href')
                if href and href != '#' and href != '/':
                    product_url = self.normalize_url(base_url, href)
            
            # Try to find price
            price_selectors = [
                '.price', '.product-price', '[data-price]', '[class*="price"]',
                '.cost', '.amount', '.value',
                # More specific price selectors
                '.product-price-amount',
                '.price-amount',
                '.price-value',
                '.product-cost',
                '.item-price',
                '.card-price',
                '.grid-item-price'
            ]
            price = None
            for selector in price_selectors:
                price_elem = element.find(selector)
                if price_elem:
                    price = self.extract_text(price_elem)
                    if price and any(char.isdigit() for char in price):
                        break
            
            return Product(
                title=title[:200],  # Limit title length
                description=description[:500],  # Limit description length
                image_url=image_url,
                product_url=product_url,
                price=price,
                available=True
            )
            
        except Exception as e:
            logger.error(f"Error extracting hero product: {e}")
            return None
    
    def _find_products_in_main_content(self, soup, base_url: str) -> List[Product]:
        """Find products in the main content area when specific selectors don't work"""
        products = []
        
        try:
            # Look for any elements that might contain product information
            potential_products = []
            
            # Find elements with product-like classes
            for selector in ['[class*="product"]', '[class*="item"]', '[class*="card"]']:
                elements = soup.select(selector)
                potential_products.extend(elements)
            
            # Find elements with product data attributes
            data_attrs = ['data-product-id', 'data-product', 'data-item']
            for attr in data_attrs:
                elements = soup.find_all(attrs={attr: True})
                potential_products.extend(elements)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_products = []
            for elem in potential_products:
                if elem not in seen:
                    seen.add(elem)
                    unique_products.append(elem)
            
            # Extract product info from each potential product
            for element in unique_products[:10]:  # Limit to first 10
                try:
                    product = self._extract_hero_product(element, base_url)
                    if product and product.title:  # Only add if we have a title
                        products.append(product)
                except Exception as e:
                    continue
            
        except Exception as e:
            logger.error(f"Error finding products in main content: {e}")
        

