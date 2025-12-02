from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import sqlite3

from database import initialize_db, import_data

#create the fastapi instance, Jinja2 templates to return HTML, and initialize database
app = FastAPI()
templates = Jinja2Templates('./templates')
con = sqlite3.connect("process_data.db")

@app.get("/")
async def initialize(request: Request) -> HTMLResponse:
   #initialize database and populate with the data from the csv
   initialize_db(con)
   #return homepage "index.html"
   return templates.TemplateResponse(request, "index.html")

@app.post("/get-tag-id")
async def get_tag_id(request: Request, tag_id: str = Form()) -> HTMLResponse:
   print(tag_id)
   return templates.TemplateResponse(request, "index.html", {"tag_id": tag_id})
