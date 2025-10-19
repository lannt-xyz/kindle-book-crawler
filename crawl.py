import os
from config import settings
from crawler.base import BaseCrawler
from crawler.factory import CrawlerFactory
from mailer.smtp_sender import SmtpSender

def crawl_and_send_email(url: str):
    crawler: BaseCrawler = CrawlerFactory.create_crawler(url)
    book_file = crawler.crawl(url)
    print(f"Crawled book content saved to: {book_file}")

    sender = SmtpSender.init()
    sender.send_email_with_attachment(
        from_addr=settings.EMAIL_FROM,
        to_addrs=[settings.EMAIL_TO],
        subject="Crawled Book Content",
        body="Please find the crawled book content attached.",
        attachment_path=book_file
    )

    # Delete the temporary book file after sending email
    os.remove(book_file)
