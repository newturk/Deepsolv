from .base_scraper import BaseScraper
from ..models.schemas import SocialHandle, ContactInfo, ImportantLink
from typing import List, Optional, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class SocialScraper(BaseScraper):
    """Scraper for extracting social media handles and contact information"""
    
    def __init__(self):
        super().__init__()
    
    def get_social_handles(self, base_url: str) -> List[SocialHandle]:
        """Extract social media handles from a Shopify store"""
        social_handles = []
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return social_handles
            
            # Common social media platforms and their patterns
            social_patterns = {
                'instagram': [
                    r'instagram\.com/([a-zA-Z0-9._]+)',
                    r'@([a-zA-Z0-9._]+)',
                    r'instagram[:\s]*([a-zA-Z0-9._]+)'
                ],
                'facebook': [
                    r'facebook\.com/([a-zA-Z0-9._]+)',
                    r'fb\.com/([a-zA-Z0-9._]+)',
                    r'facebook[:\s]*([a-zA-Z0-9._]+)'
                ],
                'twitter': [
                    r'twitter\.com/([a-zA-Z0-9._]+)',
                    r'x\.com/([a-zA-Z0-9._]+)',
                    r'twitter[:\s]*([a-zA-Z0-9._]+)'
                ],
                'tiktok': [
                    r'tiktok\.com/@([a-zA-Z0-9._]+)',
                    r'tiktok[:\s]*([a-zA-Z0-9._]+)'
                ],
                'youtube': [
                    r'youtube\.com/([a-zA-Z0-9._]+)',
                    r'youtube\.com/channel/([a-zA-Z0-9._]+)',
                    r'youtube[:\s]*([a-zA-Z0-9._]+)'
                ],
                'linkedin': [
                    r'linkedin\.com/company/([a-zA-Z0-9._]+)',
                    r'linkedin\.com/in/([a-zA-Z0-9._]+)',
                    r'linkedin[:\s]*([a-zA-Z0-9._]+)'
                ],
                'pinterest': [
                    r'pinterest\.com/([a-zA-Z0-9._]+)',
                    r'pinterest[:\s]*([a-zA-Z0-9._]+)'
                ]
            }
            
            # Extract from HTML content
            html_content = str(soup)
            
            for platform, patterns in social_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, html_content, re.IGNORECASE)
                    for match in matches:
                        if match and len(match) > 2:  # Ensure meaningful handle
                            handle = match.strip()
                            
                            # Check if we already have this platform
                            if not any(sh.platform.lower() == platform.lower() for sh in social_handles):
                                # Construct URL
                                if platform == 'instagram':
                                    url = f"https://instagram.com/{handle}"
                                elif platform == 'facebook':
                                    url = f"https://facebook.com/{handle}"
                                elif platform == 'twitter':
                                    url = f"https://twitter.com/{handle}"
                                elif platform == 'tiktok':
                                    url = f"https://tiktok.com/@{handle}"
                                elif platform == 'youtube':
                                    url = f"https://youtube.com/{handle}"
                                elif platform == 'linkedin':
                                    url = f"https://linkedin.com/company/{handle}"
                                elif platform == 'pinterest':
                                    url = f"https://pinterest.com/{handle}"
                                else:
                                    url = None
                                
                                social_handles.append(SocialHandle(
                                    platform=platform.title(),
                                    handle=handle,
                                    url=url
                                ))
                                break  # Found this platform, move to next
            
            # Also look for social media links in navigation
            social_links = soup.find_all('a', href=re.compile(r'(instagram|facebook|twitter|tiktok|youtube|linkedin|pinterest)\.com'))
            for link in social_links:
                href = link.get('href', '')
                for platform in social_patterns.keys():
                    if platform in href.lower():
                        # Extract handle from URL
                        handle_match = re.search(r'/([a-zA-Z0-9._]+)', href)
                        if handle_match:
                            handle = handle_match.group(1)
                            if not any(sh.platform.lower() == platform.lower() for sh in social_handles):
                                social_handles.append(SocialHandle(
                                    platform=platform.title(),
                                    handle=handle,
                                    url=href
                                ))
            
            # Extract additional social media information from page content
            additional_handles = self._extract_additional_social_info(soup, base_url)
            for handle in additional_handles:
                if not any(sh.platform.lower() == handle.platform.lower() for sh in social_handles):
                    social_handles.append(handle)
            
            logger.info(f"Found {len(social_handles)} social media handles on {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting social handles from {base_url}: {e}")
        
        return social_handles

    def _extract_additional_social_info(self, soup, base_url: str) -> List[SocialHandle]:
        """Extract additional social media information from page content"""
        additional_handles = []
        
        try:
            # Look for social media mentions in text content
            page_text = self.extract_text(soup).lower()
            
            # Additional patterns for social media
            additional_patterns = {
                'whatsapp': [
                    r'whatsapp[:\s]*\+?([0-9]+)',
                    r'wa\.me/([0-9]+)'
                ],
                'telegram': [
                    r'telegram[:\s]*@?([a-zA-Z0-9._]+)',
                    r't\.me/([a-zA-Z0-9._]+)'
                ],
                'snapchat': [
                    r'snapchat[:\s]*@?([a-zA-Z0-9._]+)',
                    r'snap[:\s]*@?([a-zA-Z0-9._]+)'
                ],
                'discord': [
                    r'discord[:\s]*@?([a-zA-Z0-9._]+)',
                    r'discord\.gg/([a-zA-Z0-9._]+)'
                ]
            }
            
            for platform, patterns in additional_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        if match and len(match) > 2:
                            handle = match.strip()
                            
                            # Construct URL
                            if platform == 'whatsapp':
                                url = f"https://wa.me/{handle}"
                            elif platform == 'telegram':
                                url = f"https://t.me/{handle}"
                            elif platform == 'snapchat':
                                url = f"https://snapchat.com/add/{handle}"
                            elif platform == 'discord':
                                url = f"https://discord.gg/{handle}"
                            else:
                                url = None
                            
                            additional_handles.append(SocialHandle(
                                platform=platform.title(),
                                handle=handle,
                                url=url
                            ))
                            break
            
        except Exception as e:
            logger.error(f"Error extracting additional social info: {e}")
        
        return additional_handles
    
    def get_contact_info(self, base_url: str) -> ContactInfo:
        """Extract contact information from a Shopify store"""
        contact_info = ContactInfo()
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return contact_info
            
            # Extract emails
            emails = self._extract_emails(soup)
            contact_info.emails = emails
            
            # Extract phone numbers
            phone_numbers = self._extract_phone_numbers(soup)
            contact_info.phone_numbers = phone_numbers
            
            # Extract addresses
            addresses = self._extract_addresses(soup)
            contact_info.addresses = addresses
            
            # Find contact form URL
            contact_form_url = self._find_contact_form(soup, base_url)
            contact_info.contact_form_url = contact_form_url
            
            logger.info(f"Found {len(emails)} emails, {len(phone_numbers)} phone numbers on {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting contact info from {base_url}: {e}")
        
        return contact_info
    
    def get_important_links(self, base_url: str) -> List[ImportantLink]:
        """Extract important links from a Shopify store"""
        important_links = []
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return important_links
            
            # Common important link patterns
            link_patterns = [
                # Navigation links
                ('nav a', 'Navigation'),
                ('header a', 'Header'),
                ('footer a', 'Footer'),
                # Specific important pages
                ('.contact a, .contact-us a', 'Contact'),
                ('.about a, .about-us a', 'About'),
                ('.help a, .support a', 'Help/Support'),
                ('.track-order a, .order-tracking a', 'Order Tracking'),
                ('.blog a, .news a', 'Blog/News'),
                ('.shipping a, .delivery a', 'Shipping'),
                ('.returns a, .refunds a', 'Returns'),
                ('.size-guide a, .sizing a', 'Size Guide'),
                ('.faq a', 'FAQ'),
                ('.privacy a, .legal a', 'Legal')
            ]
            
            for selector, category in link_patterns:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    text = self.extract_text(link)
                    
                    if href and text and len(text.strip()) > 2:
                        # Normalize URL
                        full_url = self.normalize_url(base_url, href)
                        
                        # Skip external links and anchors
                        if not full_url.startswith('http') or full_url.startswith(base_url):
                            important_links.append(ImportantLink(
                                title=text.strip(),
                                url=full_url,
                                description=category
                            ))
            
            # Remove duplicates based on URL
            unique_links = []
            seen_urls = set()
            for link in important_links:
                if link.url not in seen_urls:
                    unique_links.append(link)
                    seen_urls.add(link.url)
            
            logger.info(f"Found {len(unique_links)} important links on {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting important links from {base_url}: {e}")
        
        return unique_links
    
    def _extract_emails(self, soup) -> List[str]:
        """Extract email addresses from HTML content"""
        emails = []
        
        try:
            # Look for email links
            email_links = soup.find_all('a', href=re.compile(r'^mailto:'))
            for link in email_links:
                href = link.get('href', '')
                email = href.replace('mailto:', '').split('?')[0]
                if email and '@' in email:
                    emails.append(email)
            
            # Look for email patterns in text
            text_content = str(soup)
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_matches = re.findall(email_pattern, text_content)
            
            for email in email_matches:
                if email not in emails:
                    emails.append(email)
            
        except Exception as e:
            logger.error(f"Error extracting emails: {e}")
        
        return emails
    
    def _extract_phone_numbers(self, soup) -> List[str]:
        """Extract phone numbers from HTML content"""
        phone_numbers = []
        
        try:
            # Look for phone links
            phone_links = soup.find_all('a', href=re.compile(r'^tel:'))
            for link in phone_links:
                href = link.get('href', '')
                phone = href.replace('tel:', '').strip()
                if phone:
                    phone_numbers.append(phone)
            
            # Look for phone patterns in text
            text_content = str(soup)
            
            # Various phone number patterns - more restrictive to avoid false positives
            phone_patterns = [
                r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',  # US format
                r'\+?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}',  # International
                r'\([0-9]{3}\)\s*[0-9]{3}-[0-9]{4}',  # (123) 456-7890
                r'[0-9]{3}-[0-9]{3}-[0-9]{4}',  # 123-456-7890
                r'[0-9]{3}\.[0-9]{3}\.[0-9]{4}',  # 123.456.7890
                r'\+?[0-9]{10,15}',  # Simple 10-15 digit numbers
                r'[0-9]{3}\s*[0-9]{3}\s*[0-9]{4}',  # 123 456 7890
                r'[0-9]{3}\s*[0-9]{4}\s*[0-9]{4}',  # 123 4567 8901
            ]
            
            for pattern in phone_patterns:
                matches = re.findall(pattern, text_content)
                for match in matches:
                    if isinstance(match, tuple):
                        phone = ''.join(match)
                    else:
                        phone = match
                    
                    # Validate phone number to avoid false positives
                    if phone and self._is_valid_phone_number(phone) and phone not in phone_numbers:
                        phone_numbers.append(phone)
            
        except Exception as e:
            logger.error(f"Error extracting phone numbers: {e}")
        
        return phone_numbers

    def _is_valid_phone_number(self, phone: str) -> bool:
        """Validate if a phone number is likely real and not a false positive"""
        try:
            # Remove all non-digit characters
            digits_only = re.sub(r'[^\d]', '', phone)
            
            # Basic validation
            if len(digits_only) < 10 or len(digits_only) > 15:
                return False
            
            # Check for common false positive patterns
            # Avoid numbers that are all the same digit
            if len(set(digits_only)) == 1:
                return False
            
            # Avoid numbers that are mostly zeros
            if digits_only.count('0') > len(digits_only) * 0.7:
                return False
            
            # Avoid numbers that are mostly ones
            if digits_only.count('1') > len(digits_only) * 0.7:
                return False
            
            # Check for sequential patterns (like 1234567890)
            if len(digits_only) >= 6:
                sequential_count = 0
                for i in range(len(digits_only) - 1):
                    if int(digits_only[i]) + 1 == int(digits_only[i + 1]):
                        sequential_count += 1
                    else:
                        sequential_count = 0
                    
                    if sequential_count >= 4:  # Too many sequential digits
                        return False
            
            return True
            
        except Exception:
            return False
    
    def _extract_addresses(self, soup) -> List[str]:
        """Extract addresses from HTML content"""
        addresses = []
        
        try:
            # Look for address elements
            address_elements = soup.find_all(['address', '.address', '[data-address]'])
            for elem in address_elements:
                address_text = self.extract_text(elem)
                if address_text and len(address_text.strip()) > 20:  # Ensure meaningful address
                    addresses.append(address_text.strip())
            
            # Look for address patterns in text
            text_content = str(soup)
            
            # Common address patterns
            address_patterns = [
                r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)',
                r'[A-Za-z\s]+,?\s+[A-Z]{2}\s+\d{5}',  # City, State ZIP
                r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2}\s+\d{5}',  # Full address
                r'[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)[,\s]+[A-Za-z\s]+[,\s]+[A-Z]{2}',  # Street + City + State
            ]
            
            for pattern in address_patterns:
                matches = re.findall(pattern, text_content)
                for match in matches:
                    if match and len(match.strip()) > 20 and match.strip() not in addresses:
                        addresses.append(match.strip())
            
            # If no addresses found, try to extract from main page content
            if not addresses:
                addresses = self._extract_addresses_from_content(text_content)
            
        except Exception as e:
            logger.error(f"Error extracting addresses: {e}")
        
        return addresses

    def _extract_addresses_from_content(self, text_content: str) -> List[str]:
        """Extract addresses from page content using pattern matching"""
        addresses = []
        
        try:
            # Look for address-like content in the text
            # Common patterns for business addresses
            content_patterns = [
                r'(?:Address|Location|Office|Store)[:\s]+([^.\n]{20,100})',
                r'(?:Located at|Find us at|Visit us at)[:\s]+([^.\n]{20,100})',
                r'([0-9]+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)[^.\n]{0,50})',
                r'([A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)[^.\n]{0,50})',
            ]
            
            for pattern in content_patterns:
                matches = re.findall(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    if match and len(match.strip()) > 20:
                        # Clean up the address
                        address = match.strip()
                        # Remove common prefixes
                        address = re.sub(r'^(?:Address|Location|Office|Store|Located at|Find us at|Visit us at)[:\s]*', '', address, flags=re.IGNORECASE)
                        address = address.strip()
                        
                        if len(address) > 20 and address not in addresses:
                            addresses.append(address)
            
        except Exception as e:
            logger.error(f"Error extracting addresses from content: {e}")
        
        return addresses
    
    def _find_contact_form(self, soup, base_url: str) -> Optional[str]:
        """Find contact form URL"""
        try:
            # Look for contact form links
            contact_selectors = [
                'a[href*="contact"]',
                'a[href*="contact-us"]',
                'a[href*="get-in-touch"]',
                'a[href*="reach-us"]',
                '.contact-form a',
                '.contact-us a'
            ]
            
            for selector in contact_selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = self.normalize_url(base_url, href)
                        if full_url.startswith(base_url):
                            return full_url
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding contact form: {e}")
            return None
