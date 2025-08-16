from ..scrapers.product_scraper import ProductScraper
from ..scrapers.policy_scraper import PolicyScraper
from ..scrapers.social_scraper import SocialScraper
from ..scrapers.competitor_scraper import CompetitorScraper
from ..models.schemas import StoreInsights, Product, Policy, FAQ, SocialHandle, ContactInfo, ImportantLink, Competitor
from ..models.database import get_db
from typing import Optional, Dict, Any
import time
import logging
from urllib.parse import urlparse
import re

logger = logging.getLogger(__name__)

class InsightService:
    """Main service for orchestrating store insight extraction"""
    
    def __init__(self):
        self.product_scraper = ProductScraper()
        self.policy_scraper = PolicyScraper()
        self.social_scraper = SocialScraper()
        self.competitor_scraper = CompetitorScraper()
    
    async def get_store_insights(self, website_url: str) -> StoreInsights:
        """Get comprehensive insights from a Shopify store"""
        start_time = time.time()
        
        try:
            # Validate that it's a Shopify store
            if not self.product_scraper.is_shopify_store(website_url):
                raise ValueError("The provided URL does not appear to be a Shopify store")
            
            # Extract brand name from URL or page title
            brand_name = self._extract_brand_name(website_url)
            
            # Initialize store insights
            store_insights = StoreInsights(
                brand_name=brand_name,
                website_url=website_url
            )
            
            # Extract all insights in parallel (for better performance)
            logger.info(f"Starting insight extraction for {website_url}")
            
            # Extract products
            products = self.product_scraper.get_all_products(website_url)
            store_insights.products = products
            store_insights.total_products = len(products)
            
            # Extract hero products
            hero_products = self.product_scraper.get_hero_products(website_url)
            store_insights.hero_products = hero_products
            
            # Extract policies and FAQs
            policies = self.policy_scraper.get_policies(website_url)
            store_insights.policies = policies
            
            faqs = self.policy_scraper.get_faqs(website_url)
            store_insights.faqs = faqs
            
            # Extract social media and contact info
            social_handles = self.social_scraper.get_social_handles(website_url)
            store_insights.social_handles = social_handles
            
            contact_info = self.social_scraper.get_contact_info(website_url)
            store_insights.contact_info = contact_info
            
            # Extract important links
            important_links = self.social_scraper.get_important_links(website_url)
            store_insights.important_links = important_links
            
            # Extract brand context
            brand_context = self._extract_brand_context(website_url)
            store_insights.brand_context = brand_context
            
            # Extract store metadata
            store_metadata = self._extract_store_metadata(website_url)
            store_insights.store_theme = store_metadata.get('theme')
            store_insights.currency = store_metadata.get('currency')
            store_insights.language = store_metadata.get('language')
            
            # Find competitors (bonus feature)
            competitors = self.competitor_scraper.find_competitors(website_url, brand_name)
            store_insights.competitors = competitors
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            logger.info(f"Successfully extracted insights from {website_url} in {processing_time:.2f} seconds")
            logger.info(f"Found {len(products)} products, {len(faqs)} FAQs, {len(social_handles)} social handles")
            
            return store_insights
            
        except Exception as e:
            logger.error(f"Error extracting insights from {website_url}: {e}")
            raise
    
    def _extract_brand_name(self, website_url: str) -> str:
        """Extract brand name from website URL or page title"""
        try:
            # Try to get from page title first
            soup = self.product_scraper.get_page(website_url)
            if soup:
                title_elem = soup.find('title')
                if title_elem:
                    title = title_elem.get_text().strip()
                    # Clean up title to extract brand name
                    brand_name = self._clean_brand_name(title)
                    if brand_name:
                        return brand_name
            
            # Fallback to domain name
            domain = urlparse(website_url).netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Remove common TLDs and extract brand
            brand_name = domain.split('.')[0]
            return brand_name.title()
            
        except Exception as e:
            logger.error(f"Error extracting brand name: {e}")
            # Fallback to domain
            domain = urlparse(website_url).netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain.split('.')[0].title()
    
    def _clean_brand_name(self, title: str) -> str:
        """Clean up page title to extract brand name"""
        try:
            # Remove common suffixes
            suffixes = [
                ' - Home',
                ' | Home',
                ' - Welcome',
                ' | Welcome',
                ' - Official Store',
                ' | Official Store',
                ' - Online Store',
                ' | Online Store',
                ' - Shop',
                ' | Shop'
            ]
            
            cleaned_title = title
            for suffix in suffixes:
                if cleaned_title.endswith(suffix):
                    cleaned_title = cleaned_title[:-len(suffix)]
                    break
            
            # Remove extra whitespace
            cleaned_title = cleaned_title.strip()
            
            # If title is still too long, take first part
            if len(cleaned_title) > 50:
                cleaned_title = cleaned_title.split(' - ')[0].split(' | ')[0]
            
            return cleaned_title
            
        except Exception as e:
            logger.error(f"Error cleaning brand name: {e}")
            return title
    
    def _extract_brand_context(self, website_url: str) -> Optional[str]:
        """Extract brand context/about information"""
        try:
            # Common about page URLs
            about_urls = [
                '/about',
                '/about-us',
                '/about.html',
                '/pages/about',
                '/pages/about-us',
                '/company',
                '/our-story',
                '/story'
            ]
            
            for about_url in about_urls:
                try:
                    full_url = website_url.rstrip('/') + about_url
                    soup = self.product_scraper.get_page(full_url)
                    
                    if soup:
                        # Look for main content
                        content_selectors = [
                            'main',
                            '.main-content',
                            '.content',
                            '.about-content',
                            'article',
                            '.page-content'
                        ]
                        
                        content = None
                        for selector in content_selectors:
                            content = soup.select_one(selector)
                            if content:
                                break
                        
                        if not content:
                            content = soup.find('body')
                        
                        if content:
                            # Extract text and clean it
                            text = self.product_scraper.extract_text(content)
                            if text and len(text.strip()) > 100:
                                # Limit to first 500 characters
                                return text.strip()[:500] + "..." if len(text) > 500 else text.strip()
                                
                except Exception as e:
                    logger.debug(f"Error extracting from {about_url}: {e}")
                    continue
            
            # If no about page found, try to extract from homepage
            soup = self.product_scraper.get_page(website_url)
            if soup:
                # Look for about sections on homepage
                about_selectors = [
                    '.about',
                    '.about-us',
                    '.our-story',
                    '.story',
                    '.company',
                    '.brand'
                ]
                
                for selector in about_selectors:
                    element = soup.select_one(selector)
                    if element:
                        text = self.product_scraper.extract_text(element)
                        if text and len(text.strip()) > 50:
                            return text.strip()[:300] + "..." if len(text) > 300 else text.strip()
                
                # If no specific about sections found, try to extract from main content
                # Look for paragraphs that might contain brand information
                main_content = soup.find(['main', '#main', '.main', '.content', '#content'])
                if not main_content:
                    main_content = soup
                
                # Look for paragraphs with brand-related keywords
                brand_keywords = ['about', 'brand', 'company', 'story', 'mission', 'vision', 'values']
                paragraphs = main_content.find_all('p')
                
                for p in paragraphs:
                    text = self.product_scraper.extract_text(p)
                    if text and len(text.strip()) > 30:
                        text_lower = text.lower()
                        if any(keyword in text_lower for keyword in brand_keywords):
                            return text.strip()[:300] + "..." if len(text) > 300 else text.strip()
                
                # Look for headings that might contain brand information
                headings = main_content.find_all(['h1', 'h2', 'h3'])
                for heading in headings:
                    text = self.product_scraper.extract_text(heading)
                    if text and len(text.strip()) > 10:
                        text_lower = text.lower()
                        if any(keyword in text_lower for keyword in brand_keywords):
                            # Get the next paragraph or sibling element
                            next_elem = heading.find_next_sibling(['p', 'div'])
                            if next_elem:
                                content = self.product_scraper.extract_text(next_elem)
                                if content and len(content.strip()) > 20:
                                    return content.strip()[:300] + "..." if len(content) > 300 else content.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting brand context: {e}")
            return None
    
    def _extract_store_metadata(self, website_url: str) -> Dict[str, str]:
        """Extract store metadata like theme, currency, language"""
        metadata = {}
        
        try:
            soup = self.product_scraper.get_page(website_url)
            if not soup:
                return metadata
            
            # Extract theme information
            theme_indicators = [
                'data-theme',
                'data-shopify-theme',
                'class*="theme-',
                'id*="theme-'
            ]
            
            for indicator in theme_indicators:
                if 'class*=' in indicator:
                    attr, value = indicator.split('*=', 1)
                    elements = soup.find_all(attrs={attr: lambda x: x and value in x if x else False})
                    if elements:
                        for element in elements:
                            classes = element.get('class', [])
                            for cls in classes:
                                if 'theme-' in cls:
                                    metadata['theme'] = cls
                                    break
                        if 'theme' in metadata:
                            break
                else:
                    elements = soup.find_all(attrs={indicator: True})
                    if elements:
                        metadata['theme'] = elements[0].get(indicator)
                        break
            
            # Extract currency
            currency_elements = soup.find_all(text=re.compile(r'[\$€£¥₹]'))
            if currency_elements:
                for elem in currency_elements:
                    currency_match = re.search(r'([\$€£¥₹])', elem)
                    if currency_match:
                        metadata['currency'] = currency_match.group(1)
                        break
            
            # Extract language
            lang_elem = soup.find(attrs={'lang': True})
            if lang_elem:
                metadata['language'] = lang_elem.get('lang')
            
            # Also check meta tags
            meta_lang = soup.find('meta', attrs={'http-equiv': 'content-language'})
            if meta_lang:
                metadata['language'] = meta_lang.get('content')
            
        except Exception as e:
            logger.error(f"Error extracting store metadata: {e}")
        
        return metadata
    
    async def save_to_database(self, store_insights: StoreInsights) -> bool:
        """Save store insights to database"""
        try:
            # This would implement database persistence
            # For now, we'll return True as a placeholder
            logger.info(f"Would save insights for {store_insights.brand_name} to database")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return False
    
    def validate_website_url(self, website_url: str) -> bool:
        """Validate if the website URL is accessible and is a Shopify store"""
        try:
            # Basic URL validation
            if not website_url.startswith(('http://', 'https://')):
                return False
            
            # Check if it's a Shopify store
            return self.product_scraper.is_shopify_store(website_url)
            
        except Exception as e:
            logger.error(f"Error validating website URL: {e}")
            return False
