"""
وكيل التصفح الذكي لجمع أسعار الخضار والفواكه
"""
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional
from config import API_KEY, BROWSER_USE_URL, REQUEST_TIMEOUT, MAX_RETRIES

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartBrowserAgent:
    def __init__(self):
        self.api_key = API_KEY
        self.browser_url = BROWSER_USE_URL
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_page_content(self, url: str, options: Dict = None) -> Optional[str]:
        """
        جلب محتوى صفحة ويب باستخدام Browser API
        """
        if not options:
            options = {
                "wait_for": 5000,
                "scroll_to_bottom": True,
                "remove_ads": True
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "url": url,
            "render": {
                "html": True,
                "screenshot": False,
                "pdf": False
            },
            "options": options
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"محاولة {attempt + 1} لجلب الصفحة: {url}")
                
                async with self.session.post(
                    self.browser_url, 
                    json=data, 
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        html_content = result.get("html", "")
                        
                        if html_content:
                            logger.info(f"تم جلب المحتوى بنجاح من: {url}")
                            return html_content
                        else:
                            logger.warning(f"محتوى فارغ من: {url}")
                            
                    else:
                        logger.error(f"خطأ HTTP {response.status} من: {url}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"انتهت مهلة الاتصال للمحاولة {attempt + 1}")
                
            except Exception as e:
                logger.error(f"خطأ في المحاولة {attempt + 1}: {str(e)}")
                
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(2 ** attempt)  # تأخير تصاعدي
        
        logger.error(f"فشل في جلب المحتوى من: {url}")
        return None
    
    async def get_multiple_pages(self, urls: List[str]) -> Dict[str, Optional[str]]:
        """
        جلب محتوى عدة صفحات بشكل متزامن
        """
        tasks = []
        for url in urls:
            task = asyncio.create_task(self.get_page_content(url))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        page_contents = {}
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                logger.error(f"خطأ في جلب {url}: {str(result)}")
                page_contents[url] = None
            else:
                page_contents[url] = result
                
        return page_contents
    
    async def smart_facebook_scraper(self, facebook_url: str) -> Optional[str]:
        """
        كاشط ذكي خاص بصفحات الفيسبوك
        """
        fb_options = {
            "wait_for": 8000,
            "scroll_to_bottom": True,
            "remove_ads": True,
            "block_images": True,  # لتسريع التحميل
            "block_videos": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        return await self.get_page_content(facebook_url, fb_options)

# دالة مساعدة للاستخدام السريع
async def get_facebook_page_content(url: str) -> Optional[str]:
    """
    دالة مساعدة لجلب محتوى صفحة فيسبوك
    """
    async with SmartBrowserAgent() as agent:
        return await agent.smart_facebook_scraper(url)

async def get_multiple_facebook_pages(urls: List[str]) -> Dict[str, Optional[str]]:
    """
    دالة مساعدة لجلب محتوى عدة صفحات فيسبوك
    """
    async with SmartBrowserAgent() as agent:
        return await agent.get_multiple_pages(urls)
