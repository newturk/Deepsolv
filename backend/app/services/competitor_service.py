import logging
import re
from typing import List, Dict, Any, Optional
from ..models.schemas import Competitor
from ..scrapers.base_scraper import BaseScraper
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

class CompetitorService:
    """Service for analyzing competitors of Shopify stores"""
    
    def __init__(self):
        self.scraper = BaseScraper()
        # Initialize Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not found, competitor analysis will be limited")
    
    def get_competitors(self, website_url: str, brand_name: str, category: str = None) -> List[Competitor]:
        """Get competitors for a given Shopify store"""
        competitors = []
        
        try:
            # Method 1: Use Gemini to find competitors
            if self.model:
                ai_competitors = self._get_competitors_from_gemini(website_url, brand_name, category)
                competitors.extend(ai_competitors)
            
            # Method 2: Scrape from top Shopify stores list
            top_store_competitors = self._get_competitors_from_top_stores(website_url, brand_name, category)
            competitors.extend(top_store_competitors)
            
            # Remove duplicates and limit results
            unique_competitors = self._deduplicate_competitors(competitors)
            
            logger.info(f"Found {len(unique_competitors)} unique competitors for {brand_name}")
            return unique_competitors[:10]  # Limit to top 10
            
        except Exception as e:
            logger.error(f"Error getting competitors: {e}")
            return []
    
    def _get_competitors_from_gemini(self, website_url: str, brand_name: str, category: str = None) -> List[Competitor]:
        """Use Gemini to find competitors"""
        try:
            prompt = f"""
            Analyze the Shopify store at {website_url} for brand "{brand_name}" and find 5-8 direct competitors.
            
            Consider:
            - Same product category or industry
            - Similar target audience
            - Comparable price points
            - Similar business model
            
            For each competitor, provide:
            - Company name
            - Website URL
            - Brief description of why they're a competitor
            - Main product category
            
            Format as JSON:
            {{
                "competitors": [
                    {{
                        "name": "Competitor Name",
                        "website_url": "https://competitor.com",
                        "description": "Why they compete",
                        "category": "Product category"
                    }}
                ]
            }}
            
            Only return valid JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            content = response.text
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                import json
                data = json.loads(json_match.group())
                
                competitors = []
                for comp_data in data.get('competitors', []):
                    competitor = Competitor(
                        name=comp_data.get('name', ''),
                        website_url=comp_data.get('website_url', ''),
                        description=comp_data.get('description', ''),
                        category=comp_data.get('category', '')
                    )
                    competitors.append(competitor)
                
                logger.info(f"Gemini found {len(competitors)} competitors")
                return competitors
                
        except Exception as e:
            logger.error(f"Error getting competitors from Gemini: {e}")
        
        return []
    
    def _get_competitors_from_top_stores(self, website_url: str, brand_name: str, category: str = None) -> List[Competitor]:
        """Scrape competitors from top Shopify stores list"""
        try:
            # Scrape from the top Shopify stores page
            top_stores_url = "https://webinopoly.com/blogs/news/top-100-most-successful-shopify-stores"
            
            soup = self.scraper.get_page(top_stores_url)
            if not soup:
                return []
            
            competitors = []
            
            # Extract store information from the table
            table_rows = soup.find_all('tr')
            
            for row in table_rows[1:]:  # Skip header row
                cells = row.find_all('td')
                if len(cells) >= 3:
                    try:
                        store_name = self.scraper.extract_text(cells[1]).strip()
                        store_url = cells[1].find('a')
                        store_url = store_url.get('href') if store_url else None
                        
                        # Skip if it's the same store
                        if store_url and store_url in website_url:
                            continue
                        
                        # Check if it's a relevant competitor based on category or name similarity
                        if self._is_relevant_competitor(store_name, category, brand_name):
                            competitor = Competitor(
                                name=store_name,
                                website_url=store_url or '',
                                description=f"Top performing Shopify store in similar category",
                                category=category or "E-commerce"
                            )
                            competitors.append(competitor)
                            
                    except Exception as e:
                        logger.error(f"Error parsing competitor row: {e}")
                        continue
            
            logger.info(f"Found {len(competitors)} competitors from top stores list")
            return competitors
            
        except Exception as e:
            logger.error(f"Error scraping top stores: {e}")
            return []
    
    def _is_relevant_competitor(self, store_name: str, category: str, brand_name: str) -> bool:
        """Check if a store is a relevant competitor"""
        if not store_name:
            return False
        
        # Check for category similarity
        if category:
            category_lower = category.lower()
            store_lower = store_name.lower()
            
            # Common category keywords
            category_keywords = {
                'fashion': ['fashion', 'clothing', 'apparel', 'style', 'wear', 'outfit'],
                'beauty': ['beauty', 'cosmetics', 'skincare', 'makeup', 'beauty'],
                'electronics': ['electronics', 'tech', 'gadget', 'device', 'electronic'],
                'home': ['home', 'furniture', 'decor', 'kitchen', 'garden'],
                'fitness': ['fitness', 'gym', 'sport', 'athletic', 'workout'],
                'food': ['food', 'beverage', 'snack', 'drink', 'nutrition']
            }
            
            for cat, keywords in category_keywords.items():
                if any(keyword in category_lower for keyword in keywords):
                    if any(keyword in store_lower for keyword in keywords):
                        return True
        
        # Check for name similarity (avoid exact matches)
        if brand_name.lower() in store_name.lower() or store_name.lower() in brand_name.lower():
            return False
        
        return True
    
    def _deduplicate_competitors(self, competitors: List[Competitor]) -> List[Competitor]:
        """Remove duplicate competitors based on URL"""
        seen_urls = set()
        unique_competitors = []
        
        for competitor in competitors:
            if competitor.website_url and competitor.website_url not in seen_urls:
                seen_urls.add(competitor.website_url)
                unique_competitors.append(competitor)
        
        return unique_competitors
    
    def analyze_competitor_products(self, competitor_url: str) -> Dict[str, Any]:
        """Analyze products from a competitor store"""
        try:
            # Basic product analysis from competitor store
            soup = self.scraper.get_page(competitor_url)
            if not soup:
                return {}
            
            # Extract basic store information
            store_info = {
                'title': '',
                'description': '',
                'product_count': 0,
                'main_categories': [],
                'pricing_info': {}
            }
            
            # Get store title
            title_elem = soup.find('title')
            if title_elem:
                store_info['title'] = self.scraper.extract_text(title_elem)
            
            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                store_info['description'] = meta_desc.get('content', '')
            
            # Count product-like elements
            product_elements = soup.find_all(['div', 'article'], class_=re.compile(r'product|item|card'))
            store_info['product_count'] = len(product_elements)
            
            # Extract main categories from navigation
            nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=re.compile(r'nav|menu|category'))
            categories = []
            for nav in nav_elements:
                links = nav.find_all('a')
                for link in links:
                    text = self.scraper.extract_text(link)
                    if text and len(text.strip()) > 2:
                        categories.append(text.strip())
            
            store_info['main_categories'] = list(set(categories))[:5]  # Top 5 categories
            
            return store_info
            
        except Exception as e:
            logger.error(f"Error analyzing competitor products: {e}")
            return {}
