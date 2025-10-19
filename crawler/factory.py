
class CrawlerFactory:
  @staticmethod
  def create_crawler(url: str, *args, **kwargs):
      if "nhasachmienphi" in url:
          from crawler.nhasachmienphi import NhaSachMienPhi
          return NhaSachMienPhi(*args, **kwargs)
      # Add more crawler types here as needed
      raise ValueError(f"Unknown crawler type: {url}")
