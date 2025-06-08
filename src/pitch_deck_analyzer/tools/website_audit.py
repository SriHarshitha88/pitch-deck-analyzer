from crewai.tools import BaseTool
from typing import Any, Optional
import requests
from urllib.parse import urlparse

class WebsiteAuditTool(BaseTool):
    name: str = "website_audit"
    description: str = "Audit company websites for digital presence analysis"
    
    def _run(self, url: str) -> str:
        """Audit a website and return basic information."""
        try:
            if not url or not url.startswith(('http://', 'https://')):
                return "Error: Invalid URL provided"
            
            # Basic URL validation
            parsed_url = urlparse(url)
            if not parsed_url.netloc:
                return "Error: Invalid URL format"
            
            # Try to fetch basic information
            try:
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                status_code = response.status_code
                response_time = response.elapsed.total_seconds()
                content_length = len(response.content)
                
                # Basic content analysis
                content = response.text.lower()
                has_ssl = url.startswith('https://')
                
                result = f"""
WEBSITE AUDIT RESULTS:
=====================
URL: {url}
Status Code: {status_code}
Response Time: {response_time:.2f} seconds
Content Length: {content_length} bytes
SSL/HTTPS: {'Yes' if has_ssl else 'No'}

BASIC SEO ANALYSIS:
==================
- Title tag: {'Found' if '<title>' in content else 'Missing'}
- Meta description: {'Found' if 'meta name="description"' in content else 'Missing'}
- Responsive design: {'Likely' if 'viewport' in content else 'Unknown'}

CONTENT INDICATORS:
==================
- Contact information: {'Found' if any(word in content for word in ['contact', 'email', 'phone']) else 'Not found'}
- About section: {'Found' if 'about' in content else 'Not found'}
- Product information: {'Found' if any(word in content for word in ['product', 'service', 'solution']) else 'Not found'}

RECOMMENDATIONS:
===============
- Website is {'accessible' if status_code == 200 else 'not accessible'}
- Response time is {'good' if response_time < 3 else 'needs improvement'}
- {'SSL is properly configured' if has_ssl else 'Consider implementing SSL/HTTPS'}
                """
                
                return result.strip()
                
            except requests.RequestException as e:
                return f"Website audit failed: Unable to access {url}. Error: {str(e)}"
                
        except Exception as e:
            return f"Website audit error: {str(e)}"