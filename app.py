from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import sqlite3

import plotly.express as p

from database import initialize_db, plot_tag_data

#create the fastapi instance, Jinja2 templates to return HTML, and initialize database
app = FastAPI()
templates = Jinja2Templates('./templates')
con = sqlite3.connect("process_data.db")
#counter for number of plots
plot_count = 0
#list of tags currently plotted
current_plots = []

@app.get("/")
async def initialize(request: Request) -> HTMLResponse:
   #initialize database and populate with the data from the csv
   initialize_db(con)
   #return homepage "index.html"
   return templates.TemplateResponse(request, "index.html")

@app.post("/get-tag-id")
async def get_tag_id(request: Request, tag_id: str = Form()) -> HTMLResponse:
   #declare plot count and current plots as global variables
   global plot_count, current_plots
   try:
      #call plot data to collect tag data and return html graph
      plot_html = plot_tag_data(con, tag_id)
   
   except Exception as e:
      return HTMLResponse(f"""
                        <h1>Error plotting data for tag {tag_id}</h1>
                        <p>{e}</p>
                        """)
   
   #check for repeat plots
   print(current_plots)
   if tag_id in current_plots:
      return HTMLResponse(f"""
                        <h1>Plot already exists for tag {tag_id}</h1>
                        <p>Please enter a different tag ID</p>
                        """)
   
   else:
      #if try block runs, add plot count to html response
      current_plots.append(tag_id)
      plot_count += 1

   return HTMLResponse(f"""
                        <h1>Plotting data for tag {tag_id}</h1>
                        <div id="plot">{plot_html}</div>
                        """)
