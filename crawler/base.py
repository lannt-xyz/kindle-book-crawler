import random
import re

from typing import List
from playwright.sync_api import sync_playwright, Page
from playwright_stealth.stealth import Stealth
from tenacity import retry, stop_after_attempt, wait_random

from config import settings
from logger import logger

TIMEOUT = 90000

class BaseCrawler:
    def __init__(self):
        delay = random.randint(500, 1000)
        self.headless = settings.DEBUG == False
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=delay,
            args=[
                "--disable-webrtc",
                "--disable-features=WebRTC-HW-Decoding,WebRTC-HW-Encoding",
                "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-sandbox",
            ],
        )
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        self.page = self.context.new_page()
        self.page.set_default_timeout(TIMEOUT)
        stealth = Stealth()
        stealth.apply_stealth_sync(self.page)

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=3))
    def navigate(self, url: str):
        logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def get_page_content(self) -> str:
        logger.info("Extracting page content")
        return self.page.content()

    def extract_links(self, pattern: str) -> List[str]:
        content = self.get_page_content()
        return re.findall(pattern, content)

    def crawl(self, target_uri: str = "") -> str:
        raise NotImplementedError("Subclasses must implement this method")