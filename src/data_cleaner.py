import re
from typing import List, Set
from urllib.parse import urlparse, urljoin

class DataCleaner:
    @staticmethod
    def normalize_github_url(url: str) -> str:
        """Normalize GitHub URLs to a standard format."""
        # Remove trailing slashes and fragments
        url = url.rstrip('/').split('#')[0]
        
        # Ensure https protocol
        if url.startswith('http://'):
            url = url.replace('http://', 'https://')
        elif not url.startswith('https://'):
            url = 'https://' + url
        
        # Normalize github.com URLs
        if 'github.com' in url:
            # Extract username and ensure proper format
            match = re.search(r'github\.com/([A-Za-z0-9_-]+)', url)
            if match:
                username = match.group(1)
                return f'https://github.com/{username}'
        
        return url

    @staticmethod
    def remove_duplicates(links: List[str]) -> List[str]:
        """Remove duplicate links while preserving order."""
        seen: Set[str] = set()
        unique_links = []
        
        for link in links:
            normalized = DataCleaner.normalize_github_url(link)
            if normalized not in seen:
                seen.add(normalized)
                unique_links.append(normalized)
        
        return unique_links

    @staticmethod
    def filter_valid_github_links(links: List[str]) -> List[str]:
        """Filter out invalid GitHub links."""
        valid_links = []
        for link in links:
            normalized = DataCleaner.normalize_github_url(link)
            if re.match(r'^https://github\.com/[A-Za-z0-9_-]+$', normalized):
                valid_links.append(normalized)
        return valid_links

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text content."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common unwanted characters
        text = re.sub(r'[^\w\s\-\.\/\:]', '', text)
        
        return text

    @staticmethod
    def extract_links_from_text(text: str) -> List[str]:
        """Extract GitHub links from text content."""
        # Find all URLs in text
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        
        # Filter for GitHub links
        github_links = []
        for url in urls:
            if 'github.com' in url:
                normalized = DataCleaner.normalize_github_url(url)
                if re.match(r'^https://github\.com/[A-Za-z0-9_-]+$', normalized):
                    github_links.append(normalized)
        
        return DataCleaner.remove_duplicates(github_links)
