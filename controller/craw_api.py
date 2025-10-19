from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class CrawlRequest(BaseModel):
    craw_url: HttpUrl  # nếu muốn chấp nhận mọi string thì dùng str

def _do_crawl(craw_url: str):
    from crawl import crawl_and_send_email
    crawl_and_send_email(craw_url)

@router.post("")
def craw_submit(payload: CrawlRequest, bg: BackgroundTasks):
    craw_url = str(payload.craw_url).strip()
    if not craw_url:
        raise HTTPException(status_code=400, detail="craw_url is required")
    bg.add_task(_do_crawl, craw_url)
    return {"status": "accepted", "craw_url": craw_url}
