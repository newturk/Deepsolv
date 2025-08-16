from .base_scraper import BaseScraper
from ..models.schemas import Policy, FAQ
from typing import List, Optional, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class PolicyScraper(BaseScraper):
    """Scraper for extracting policy information and FAQs from Shopify stores"""
    
    def __init__(self):
        super().__init__()
    
    def get_policies(self, base_url: str) -> Policy:
        """Extract all policy information from a Shopify store"""
        policy = Policy()
        
        try:
            # Common policy page URLs
            policy_urls = {
                'privacy_policy': [
                    '/privacy-policy',
                    '/privacy',
                    '/privacy-policy.html',
                    '/pages/privacy-policy',
                    '/legal/privacy-policy'
                ],
                'return_policy': [
                    '/return-policy',
                    '/returns',
                    '/return-policy.html',
                    '/pages/return-policy',
                    '/shipping-returns',
                    '/shipping-and-returns'
                ],
                'refund_policy': [
                    '/refund-policy',
                    '/refunds',
                    '/refund-policy.html',
                    '/pages/refund-policy'
                ],
                'shipping_policy': [
                    '/shipping-policy',
                    '/shipping',
                    '/shipping-policy.html',
                    '/pages/shipping-policy'
                ],
                'terms_of_service': [
                    '/terms-of-service',
                    '/terms',
                    '/terms-of-service.html',
                    '/pages/terms-of-service',
                    '/legal/terms-of-service'
                ]
            }
            
            # Extract each policy type
            for policy_type, urls in policy_urls.items():
                content = self._extract_policy_content(base_url, urls)
                if content:
                    setattr(policy, policy_type, content)
            
            # If no policies found, try to extract from main page
            if not any([policy.privacy_policy, policy.return_policy, policy.refund_policy, 
                       policy.shipping_policy, policy.terms_of_service]):
                logger.info("No dedicated policy pages found, trying to extract from main page")
                self._extract_policies_from_main_page(base_url, policy)
            
            logger.info(f"Successfully extracted policies from {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting policies from {base_url}: {e}")
        
        return policy

    def _extract_policies_from_main_page(self, base_url: str, policy: Policy):
        """Extract policy information from the main page content"""
        try:
            soup = self.get_page(base_url)
            if not soup:
                return
            
            # Look for policy-related content in the main page
            page_text = self.extract_text(soup).lower()
            
            # Privacy policy patterns
            privacy_patterns = [
                r'privacy\s+policy[:\s]+([^.!?]+[.!?])',
                r'data\s+protection[:\s]+([^.!?]+[.!?])',
                r'information\s+collection[:\s]+([^.!?]+[.!?])',
                # More flexible patterns
                r'privacy[:\s]+([^.!?\n]{20,200})',
                r'data\s+protection[:\s]+([^.!?\n]{20,200})',
                r'information\s+collection[:\s]+([^.!?\n]{20,200})'
            ]
            
            for pattern in privacy_patterns:
                match = re.search(pattern, page_text)
                if match and not policy.privacy_policy:
                    policy.privacy_policy = match.group(1).strip()
                    break
            
            # Return policy patterns
            return_patterns = [
                r'return\s+policy[:\s]+([^.!?]+[.!?])',
                r'returns[:\s]+([^.!?]+[.!?])',
                r'refund[:\s]+([^.!?]+[.!?])',
                # More flexible patterns
                r'return[:\s]+([^.!?\n]{20,200})',
                r'refund[:\s]+([^.!?\n]{20,200})',
                r'return\s+policy[:\s]+([^.!?\n]{20,200})'
            ]
            
            for pattern in return_patterns:
                match = re.search(pattern, page_text)
                if match and not policy.return_policy:
                    policy.return_policy = match.group(1).strip()
                    break
            
            # Shipping policy patterns
            shipping_patterns = [
                r'shipping[:\s]+([^.!?]+[.!?])',
                r'delivery[:\s]+([^.!?]+[.!?])',
                r'free\s+shipping[:\s]+([^.!?]+[.!?])'
            ]
            
            for pattern in shipping_patterns:
                match = re.search(pattern, page_text)
                if match and not policy.shipping_policy:
                    policy.shipping_policy = match.group(1).strip()
                    break
            
            # Terms patterns
            terms_patterns = [
                r'terms[:\s]+([^.!?]+[.!?])',
                r'conditions[:\s]+([^.!?]+[.!?])',
                r'agreement[:\s]+([^.!?]+[.!?])'
            ]
            
            for pattern in terms_patterns:
                match = re.search(pattern, page_text)
                if match and not policy.terms_of_service:
                    policy.terms_of_service = match.group(1).strip()
                    break
            
        except Exception as e:
            logger.error(f"Error extracting policies from main page: {e}")
    
    def get_faqs(self, base_url: str) -> List[FAQ]:
        """Extract FAQs from a Shopify store"""
        faqs = []
        
        try:
            # Common FAQ page URLs
            faq_urls = [
                '/faq',
                '/faqs',
                '/frequently-asked-questions',
                '/help',
                '/support',
                '/pages/faq',
                '/pages/faqs',
                '/pages/frequently-asked-questions'
            ]
            
            # Try to find FAQs on the main page first
            main_page_faqs = self._extract_faqs_from_main_page(base_url)
            if main_page_faqs:
                faqs.extend(main_page_faqs)
            
            # Try dedicated FAQ pages
            for faq_url in faq_urls:
                page_faqs = self._extract_faqs_from_page(base_url + faq_url)
                if page_faqs:
                    faqs.extend(page_faqs)
                    break  # Found FAQs, no need to check other URLs
            
            # If still no FAQs, try to extract from main page content more aggressively
            if not faqs:
                logger.info("No FAQs found on dedicated pages, trying to extract from main page content")
                main_page_faqs = self._extract_faqs_from_main_content(base_url)
                if main_page_faqs:
                    faqs.extend(main_page_faqs)
            
            # Remove duplicates based on question
            unique_faqs = []
            seen_questions = set()
            for faq in faqs:
                if faq.question.lower() not in seen_questions:
                    unique_faqs.append(faq)
                    seen_questions.add(faq.question.lower())
            
            logger.info(f"Found {len(unique_faqs)} unique FAQs on {base_url}")
            
        except Exception as e:
            logger.error(f"Error extracting FAQs from {base_url}: {e}")
        
        return unique_faqs
    
    def _extract_policy_content(self, base_url: str, urls: List[str]) -> Optional[str]:
        """Extract policy content from a list of possible URLs"""
        for url in urls:
            try:
                full_url = base_url.rstrip('/') + url
                soup = self.get_page(full_url)
                
                if soup:
                    content = self._extract_policy_text(soup)
                    if content and len(content.strip()) > 100:  # Ensure meaningful content
                        return content
                        
            except Exception as e:
                logger.debug(f"Error extracting from {url}: {e}")
                continue
        
        return None
    
    def _extract_policy_text(self, soup) -> str:
        """Extract policy text from a BeautifulSoup object"""
        try:
            # Remove navigation, header, footer
            for element in soup(['nav', 'header', 'footer', '.nav', '.header', '.footer']):
                element.decompose()
            
            # Look for main content areas
            content_selectors = [
                'main',
                '.main-content',
                '.content',
                '.policy-content',
                '.legal-content',
                'article',
                '.page-content'
            ]
            
            content = None
            for selector in content_selectors:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                # Fallback to body content
                content = soup.find('body')
            
            if content:
                return self.extract_text(content)
            
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting policy text: {e}")
            return ""
    
    def _extract_faqs_from_main_page(self, base_url: str) -> List[FAQ]:
        """Extract FAQs from the main page"""
        faqs = []
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return faqs
            
            # Look for FAQ sections on the main page
            faq_selectors = [
                '.faq',
                '.faqs',
                '.frequently-asked-questions',
                '.help',
                '.support',
                '[data-faq]',
                '.accordion'
            ]
            
            for selector in faq_selectors:
                faq_section = soup.select_one(selector)
                if faq_section:
                    page_faqs = self._parse_faq_section(faq_section)
                    if page_faqs:
                        faqs.extend(page_faqs)
                        break
            
        except Exception as e:
            logger.error(f"Error extracting FAQs from main page: {e}")
        
        return faqs
    
    def _extract_faqs_from_page(self, url: str) -> List[FAQ]:
        """Extract FAQs from a specific page"""
        faqs = []
        
        try:
            soup = self.get_page(url)
            if not soup:
                return faqs
            
            # Look for FAQ content
            faq_content = soup.select_one('.faq, .faqs, .frequently-asked-questions, .help, .support')
            if faq_content:
                faqs = self._parse_faq_section(faq_content)
            
        except Exception as e:
            logger.error(f"Error extracting FAQs from {url}: {e}")
        
        return faqs
    
    def _parse_faq_section(self, faq_section) -> List[FAQ]:
        """Parse FAQ section and extract Q&A pairs"""
        faqs = []
        
        try:
            # Common FAQ patterns
            patterns = [
                # Pattern 1: Question and answer in separate elements
                {
                    'question': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', '.question', '.faq-question'],
                    'answer': ['p', '.answer', '.faq-answer', '.faq-content']
                },
                # Pattern 2: FAQ items with data attributes
                {
                    'item': '[data-faq], .faq-item, .faq-entry'
                },
                # Pattern 3: Accordion style FAQs
                {
                    'item': '.accordion-item, .collapse-item, .faq-accordion'
                }
            ]
            
            for pattern in patterns:
                if 'item' in pattern:
                    # Pattern with FAQ items
                    items = faq_section.select(pattern['item'])
                    for item in items:
                        faq = self._extract_faq_from_item(item)
                        if faq:
                            faqs.append(faq)
                else:
                    # Pattern with separate question/answer selectors
                    questions = faq_section.select(pattern['question'])
                    answers = faq_section.select(pattern['answer'])
                    
                    # Try to match questions with answers
                    for i, question in enumerate(questions):
                        if i < len(answers):
                            question_text = self.extract_text(question)
                            answer_text = self.extract_text(answers[i])
                            
                            if question_text and answer_text:
                                faqs.append(FAQ(
                                    question=question_text,
                                    answer=answer_text
                                ))
            
            # If no structured FAQs found, try to find Q&A patterns in text
            if not faqs:
                faqs = self._extract_faqs_from_text(faq_section)
            
        except Exception as e:
            logger.error(f"Error parsing FAQ section: {e}")
        
        return faqs
    
    def _extract_faq_from_item(self, item) -> Optional[FAQ]:
        """Extract FAQ from a single FAQ item"""
        try:
            # Look for question and answer within the item
            question_elem = item.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', '.question', '.faq-question'])
            answer_elem = item.find(['p', '.answer', '.faq-answer', '.faq-content'])
            
            if question_elem and answer_elem:
                question = self.extract_text(question_elem)
                answer = self.extract_text(answer_elem)
                
                if question and answer:
                    return FAQ(question=question, answer=answer)
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting FAQ from item: {e}")
            return None
    
    def _extract_faqs_from_text(self, element) -> List[FAQ]:
        """Extract FAQs from text content using regex patterns"""
        faqs = []
        
        try:
            text = self.extract_text(element)
            
            # Common Q&A patterns
            patterns = [
                r'Q[:\s]*([^A]+)A[:\s]*(.+)',
                r'Question[:\s]*([^A]+)Answer[:\s]*(.+)',
                r'([^?]+\?)\s*([^?]+)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    if len(match) == 2:
                        question = match[0].strip()
                        answer = match[1].strip()
                        
                        if len(question) > 10 and len(answer) > 10:  # Ensure meaningful content
                            faqs.append(FAQ(question=question, answer=answer))
            
        except Exception as e:
            logger.error(f"Error extracting FAQs from text: {e}")
        
        return faqs

    def _extract_faqs_from_main_content(self, base_url: str) -> List[FAQ]:
        """Extract FAQs from main page content using pattern matching"""
        faqs = []
        
        try:
            soup = self.get_page(base_url)
            if not soup:
                return faqs
            
            page_text = self.extract_text(soup)
            
            # Look for FAQ-like patterns in the text
            # Common patterns: "Q:", "A:", "Question:", "Answer:", etc.
            faq_patterns = [
                r'(?:Q|Question|FAQ)[:\s]+([^?\n]+)\?[:\s]*(?:A|Answer)[:\s]+([^.\n]+)',
                r'([^?\n]+\?)[:\s]*(?:A|Answer)[:\s]+([^.\n]+)',
                r'(?:FAQ|Frequently Asked Question)[:\s]+([^?\n]+)\?[:\s]*([^.\n]+)',
                # More flexible patterns
                r'([^?\n]+\?)[:\s]*([^.!?\n]{10,200})',
                r'(?:Q[:\s]*|Question[:\s]*)([^?\n]+\?)[:\s]*(?:A[:\s]*|Answer[:\s]*)([^.!?\n]{10,200})',
                r'([^?\n]+\?)[\s\n]+([^.!?\n]{10,200})'
            ]
            
            for pattern in faq_patterns:
                matches = re.finditer(pattern, page_text, re.IGNORECASE)
                for match in matches:
                    question = match.group(1).strip()
                    answer = match.group(2).strip()
                    
                    # Clean up the question and answer
                    question = re.sub(r'^[QA]:\s*', '', question)
                    answer = re.sub(r'^[QA]:\s*', '', answer)
                    
                    if len(question) > 10 and len(answer) > 10:  # Ensure meaningful content
                        faq = FAQ(
                            question=question[:200],  # Limit length
                            answer=answer[:500],     # Limit length
                            category='General'
                        )
                        faqs.append(faq)
            
            # Also look for FAQ sections in HTML
            faq_sections = soup.find_all(['div', 'section'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['faq', 'question', 'help']
            ))
            
            for section in faq_sections:
                section_faqs = self._parse_faq_section(section)
                faqs.extend(section_faqs)
            
            logger.info(f"Extracted {len(faqs)} FAQs from main page content")
            
        except Exception as e:
            logger.error(f"Error extracting FAQs from main content: {e}")
        
        return faqs
