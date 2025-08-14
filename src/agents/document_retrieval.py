"""
Document Retrieval Agent

This agent handles the automated retrieval and processing of compliance documents
from vendor trust centers, public repositories, and uploaded files.
"""

import asyncio
import hashlib
import os
import re
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from urllib.parse import urljoin, urlparse

import aiohttp
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from loguru import logger

from ..config.settings import settings
from ..models.schemas import ComplianceDocumentCreate, DocumentType
from ..services.storage_service import StorageService


class DocumentRetrievalAgent:
    """Agent responsible for finding and retrieving compliance documents"""
    
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service
        self.session = None
        
        # Common document patterns
        self.document_patterns = {
            DocumentType.SOC2: [
                r'soc\s*2', r'soc\s*ii', r'service organization control',
                r'ssae\s*18', r'type\s*ii'
            ],
            DocumentType.PRIVACY_POLICY: [
                r'privacy\s*policy', r'privacy\s*statement', r'privacy\s*notice',
                r'data\s*protection\s*policy'
            ],
            DocumentType.DPA: [
                r'data\s*processing\s*agreement', r'dpa', r'data\s*processing\s*addendum'
            ],
            DocumentType.SECURITY_POLICY: [
                r'security\s*policy', r'information\s*security', r'cybersecurity'
            ],
            DocumentType.INCIDENT_RESPONSE: [
                r'incident\s*response', r'breach\s*notification', r'security\s*incident'
            ]
        }
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Vendor-Risk-Agent/1.0'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def retrieve_vendor_documents(
        self, 
        vendor_domain: str, 
        trust_center_url: Optional[str] = None
    ) -> List[ComplianceDocumentCreate]:
        """
        Main entry point for retrieving all compliance documents for a vendor
        
        Args:
            vendor_domain: The vendor's domain name
            trust_center_url: Optional direct URL to vendor's trust center
            
        Returns:
            List of document creation schemas
        """
        logger.info(f"Starting document retrieval for vendor: {vendor_domain}")
        
        documents = []
        
        try:
            # 1. Try trust center URL if provided
            if trust_center_url:
                trust_docs = await self._scrape_trust_center(trust_center_url)
                documents.extend(trust_docs)
            
            # 2. Attempt to find trust center automatically
            if not trust_center_url or not documents:
                discovered_url = await self._discover_trust_center(vendor_domain)
                if discovered_url:
                    trust_docs = await self._scrape_trust_center(discovered_url)
                    documents.extend(trust_docs)
            
            # 3. Search common document locations
            common_docs = await self._search_common_locations(vendor_domain)
            documents.extend(common_docs)
            
            # 4. Remove duplicates and validate
            documents = self._deduplicate_documents(documents)
            
            logger.info(f"Retrieved {len(documents)} documents for {vendor_domain}")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents for {vendor_domain}: {str(e)}")
            return []
    
    async def _discover_trust_center(self, domain: str) -> Optional[str]:
        """
        Attempt to discover a vendor's trust center URL
        
        Args:
            domain: Vendor domain to search
            
        Returns:
            Trust center URL if found
        """
        logger.info(f"Discovering trust center for {domain}")
        
        # Common trust center patterns
        trust_patterns = [
            f"https://trust.{domain}",
            f"https://security.{domain}",
            f"https://compliance.{domain}",
            f"https://{domain}/trust",
            f"https://{domain}/security",
            f"https://{domain}/compliance",
            f"https://{domain}/privacy",
            f"https://www.{domain}/trust",
            f"https://www.{domain}/security"
        ]
        
        for url in trust_patterns:
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        if self._is_trust_center_page(content):
                            logger.info(f"Found trust center: {url}")
                            return url
            except:
                continue
                
        # Search main website for trust center links
        try:
            main_urls = [f"https://{domain}", f"https://www.{domain}"]
            for main_url in main_urls:
                async with self.session.get(main_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        trust_url = self._extract_trust_center_link(content, main_url)
                        if trust_url:
                            logger.info(f"Found trust center link: {trust_url}")
                            return trust_url
        except:
            pass
            
        logger.warning(f"Could not discover trust center for {domain}")
        return None
    
    def _is_trust_center_page(self, html_content: str) -> bool:
        """Check if page appears to be a trust center"""
        trust_indicators = [
            'soc 2', 'soc ii', 'compliance', 'security certification',
            'privacy policy', 'data protection', 'gdpr', 'iso 27001',
            'trust center', 'security controls'
        ]
        
        content_lower = html_content.lower()
        return sum(1 for indicator in trust_indicators if indicator in content_lower) >= 3
    
    def _extract_trust_center_link(self, html_content: str, base_url: str) -> Optional[str]:
        """Extract trust center link from main website"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for links with trust/security/compliance keywords
        trust_keywords = ['trust', 'security', 'compliance', 'privacy', 'certifications']
        
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text().lower()
            
            for keyword in trust_keywords:
                if keyword in href or keyword in text:
                    full_url = urljoin(base_url, link['href'])
                    return full_url
                    
        return None
    
    async def _scrape_trust_center(self, url: str) -> List[ComplianceDocumentCreate]:
        """
        Scrape documents from a trust center page
        
        Args:
            url: Trust center URL to scrape
            
        Returns:
            List of document schemas
        """
        logger.info(f"Scraping trust center: {url}")
        documents = []
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return documents
                    
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find all links that might be documents
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    text = link.get_text().strip()
                    
                    # Skip empty or very short links
                    if not text or len(text) < 3:
                        continue
                    
                    # Determine document type
                    doc_type = self._classify_document(text, href)
                    if doc_type:
                        full_url = urljoin(url, href)
                        
                        document = ComplianceDocumentCreate(
                            vendor_id=0,  # Will be set by caller
                            document_type=doc_type,
                            title=text[:500],  # Truncate to fit schema
                            url=full_url
                        )
                        documents.append(document)
                        
        except Exception as e:
            logger.error(f"Error scraping trust center {url}: {str(e)}")
            
        return documents
    
    async def _search_common_locations(self, domain: str) -> List[ComplianceDocumentCreate]:
        """
        Search common document locations on vendor website
        
        Args:
            domain: Vendor domain to search
            
        Returns:
            List of document schemas
        """
        logger.info(f"Searching common locations for {domain}")
        documents = []
        
        # Common document paths
        common_paths = [
            '/privacy', '/privacy-policy', '/legal/privacy',
            '/security', '/security-policy', '/legal/security',
            '/compliance', '/certifications', '/legal/compliance',
            '/terms', '/legal/terms', '/gdpr', '/legal/gdpr'
        ]
        
        base_urls = [f"https://{domain}", f"https://www.{domain}"]
        
        for base_url in base_urls:
            for path in common_paths:
                try:
                    url = base_url + path
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            # Classify the page content
                            doc_type = self._classify_page_content(content, path)
                            if doc_type:
                                title = self._extract_page_title(content) or f"Document from {path}"
                                
                                document = ComplianceDocumentCreate(
                                    vendor_id=0,
                                    document_type=doc_type,
                                    title=title[:500],
                                    url=url
                                )
                                documents.append(document)
                                
                except:
                    continue
                    
        return documents
    
    def _classify_document(self, text: str, url: str) -> Optional[DocumentType]:
        """
        Classify document type based on text and URL
        
        Args:
            text: Link text or document title
            url: Document URL
            
        Returns:
            Document type if classified, None otherwise
        """
        combined_text = f"{text} {url}".lower()
        
        for doc_type, patterns in self.document_patterns.items():
            for pattern in patterns:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    return doc_type
                    
        # Check file extensions
        if url.lower().endswith('.pdf'):
            # Could be any type, default to OTHER
            return DocumentType.OTHER
            
        return None
    
    def _classify_page_content(self, html_content: str, path: str) -> Optional[DocumentType]:
        """Classify document type based on page content and path"""
        content_lower = html_content.lower()
        path_lower = path.lower()
        
        # Privacy-related
        if any(keyword in path_lower or keyword in content_lower 
               for keyword in ['privacy', 'gdpr', 'data protection']):
            return DocumentType.PRIVACY_POLICY
            
        # Security-related
        if any(keyword in path_lower or keyword in content_lower 
               for keyword in ['security', 'soc', 'compliance', 'certification']):
            return DocumentType.SECURITY_POLICY
            
        return None
    
    def _extract_page_title(self, html_content: str) -> Optional[str]:
        """Extract page title from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
            
        # Try h1 as fallback
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
            
        return None
    
    def _deduplicate_documents(self, documents: List[ComplianceDocumentCreate]) -> List[ComplianceDocumentCreate]:
        """Remove duplicate documents based on URL and title similarity"""
        seen_urls = set()
        unique_docs = []
        
        for doc in documents:
            # Normalize URL for comparison
            if doc.url:
                normalized_url = str(doc.url).lower().rstrip('/')
                if normalized_url not in seen_urls:
                    seen_urls.add(normalized_url)
                    unique_docs.append(doc)
            else:
                unique_docs.append(doc)
                
        return unique_docs
    
    async def download_document(self, url: str, vendor_id: int) -> Tuple[Optional[str], Optional[str]]:
        """
        Download document and save to storage
        
        Args:
            url: Document URL to download
            vendor_id: Vendor ID for file organization
            
        Returns:
            Tuple of (file_path, file_hash) if successful, (None, None) if failed
        """
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None, None
                    
                content = await response.read()
                
                # Generate file hash
                file_hash = hashlib.sha256(content).hexdigest()
                
                # Determine file extension
                parsed_url = urlparse(url)
                path = parsed_url.path
                if path.endswith('.pdf'):
                    ext = '.pdf'
                elif path.endswith('.html') or path.endswith('.htm'):
                    ext = '.html'
                else:
                    # Detect content type
                    content_type = response.headers.get('content-type', '').lower()
                    if 'pdf' in content_type:
                        ext = '.pdf'
                    elif 'html' in content_type:
                        ext = '.html'
                    else:
                        ext = '.txt'
                
                # Generate filename
                filename = f"{vendor_id}_{file_hash[:12]}{ext}"
                file_path = await self.storage_service.save_document(filename, content)
                
                return file_path, file_hash
                
        except Exception as e:
            logger.error(f"Error downloading document {url}: {str(e)}")
            return None, None
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return ""
    
    def extract_text_from_html(self, file_path: str) -> str:
        """Extract text content from HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text()
        except Exception as e:
            logger.error(f"Error extracting text from HTML {file_path}: {str(e)}")
            return ""


# Convenience function for standalone usage
async def retrieve_vendor_documents(vendor_domain: str, vendor_id: int, storage_service: StorageService) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve and process vendor documents
    
    Args:
        vendor_domain: Vendor domain to process
        vendor_id: Database vendor ID
        storage_service: Storage service instance
        
    Returns:
        List of processed document data
    """
    async with DocumentRetrievalAgent(storage_service) as agent:
        doc_schemas = await agent.retrieve_vendor_documents(vendor_domain)
        
        processed_docs = []
        for doc_schema in doc_schemas:
            # Set vendor_id
            doc_schema.vendor_id = vendor_id
            
            # Download document if it has a URL
            if doc_schema.url:
                file_path, file_hash = await agent.download_document(str(doc_schema.url), vendor_id)
                if file_path and file_hash:
                    # Extract text content
                    if file_path.endswith('.pdf'):
                        content = agent.extract_text_from_pdf(file_path)
                    elif file_path.endswith('.html'):
                        content = agent.extract_text_from_html(file_path)
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    
                    processed_docs.append({
                        'schema': doc_schema,
                        'file_path': file_path,
                        'file_hash': file_hash,
                        'content': content
                    })
                else:
                    processed_docs.append({
                        'schema': doc_schema,
                        'file_path': None,
                        'file_hash': None,
                        'content': None
                    })
            else:
                processed_docs.append({
                    'schema': doc_schema,
                    'file_path': None,
                    'file_hash': None,
                    'content': None
                })
        
        return processed_docs
