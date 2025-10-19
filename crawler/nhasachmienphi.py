import tempfile

from bs4 import BeautifulSoup
from crawler.base import BaseCrawler

from logger import logger
from utilities import saintize_vietnamese_text

class NhaSachMienPhi(BaseCrawler):
    BASE_URL = "https://nhasachmienphi.com"

    def __init__(self):
        super().__init__()
        self.book_name = ""
    
    def crawl(self, target_uri: str = "") -> str:
        full_content = self.crawl_detail(target_uri)
        # Write full content to file with UTF-8 encoding has named is {self.book_name}_{yyyymmdd_hhmmss}.txt
        book_name_sanitized = saintize_vietnamese_text(self.book_name)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".txt", prefix=book_name_sanitized + "_") as temp_file:
            temp_file.write(full_content)
            temp_file_path = temp_file.name

        self.close()
        
        return temp_file_path

    def crawl_detail(self, target_uri: str) -> str:
        uri = target_uri.replace(f"{self.BASE_URL}/", "")
        self.navigate(f"{self.BASE_URL}/{uri}")
        content_soup = BeautifulSoup(self.get_page_content(), "html.parser")
        full_content = ""
        if self.book_name == "":
            # Get name of book from XPath /html/body/div[2]/div[1]/div[1]/h1/a
            book_name_element = content_soup.select_one("body > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h1 > a")
            self.book_name = book_name_element.text.strip() if book_name_element else "No book name found"
            full_content += f"{self.book_name}\n\n"
            self.is_first_page = False
        
        # Extract title from XPath /html/body/div[2]/div[1]/div[1]/h2
        title_element = content_soup.select_one("body > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h2")
        title = title_element.text.strip() if title_element else "No title found"
        
        # Extract content from div has class `content_p`
        content_element_container = content_soup.select_one("div.content_p")
        # Find all html tag inside and get text content
        content_text = ""
        if content_element_container:
            for child in content_element_container.children:
                if child.name == "br":
                    content_text += "\n"
                elif child.name:
                    content_text += child.get_text(separator="\n").strip() + "\n"
                elif isinstance(child, str):
                    content_text += child.strip() + "\n"
            content_text = content_text.strip()
        
        full_content += f"{title}\n\n{content_text}\n\n"

        # Check if the next page link exists by XPath /html/body/div[2]/div[1]/div[7]/a
        next_page_elements = content_soup.select("body > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(7) > a")
        # get the element has content is i tag has class 'fa fa-long-arrow-right'
        next_page_element = None
        for element in next_page_elements:
            if element.find("i", class_="fa fa-long-arrow-right"):
                next_page_element = element
                break
        if next_page_element and 'href' in next_page_element.attrs:
            next_page_url = next_page_element['href']
            logger.info(f"Found next page: {next_page_url}")
            return full_content + self.crawl_detail(next_page_url)

        logger.info("Crawling completed. No more pages.")
        return full_content
