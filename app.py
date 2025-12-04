from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import sqlite3

import plotly.express as p

from database import initialize_db, get_tag_data

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
   get_tag_data(con, tag_id)

   return HTMLResponse(f"""
                        <h1>Plotting data for tag {tag_id}</h1>
                        <div id="plot"></div>
                        """)
