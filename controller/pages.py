from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

jinja_templates: Jinja2Templates = Jinja2Templates(directory="templates")

@router.get("/")
def crawler(request: Request):
  return jinja_templates.TemplateResponse("craw.html", {"request": request})
