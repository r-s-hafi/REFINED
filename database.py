from sqlite3 import Connection
import pandas as pd
from fastapi.responses import HTMLResponse
import plotly.express as px
import plotly.io as pio

#creates process data database and populates with data from data.csv
def initialize_db(con: Connection) -> None:
    try:
        #read the data.csv file into a pandas dataframe
        df = pd.read_csv("data.csv")

        #insert the data into the database
        df.to_sql("process_data", con, if_exists="replace", index=False)

        #print the data from the database, currently just a test
        with con:
            cur = con.cursor()
            res = cur.execute("SELECT * FROM process_data")
            print(res.fetchall())
    
    except Exception as e:
        print(f"Unable to import data: {e}")

#plots data for given tag id and returns html
def generate_plots(con: Connection, tag_id: str, current_plots: list) -> HTMLResponse:
    #initialize string to store html for all plots
    wrapped_html = ""
    stored_plot_html = ""

    #generate html for queried tag id
    df = pd.read_sql(f"SELECT Time, {tag_id} FROM process_data", con)
    fig = px.line(df, x="Time", y=tag_id, title=f"{tag_id}", labels={'Time': 'Time', tag_id: 'Value'})
    plot_html = pio.to_html(fig, config={'responsive': True})     
    wrapped_html += f'<div id="plot">{plot_html}</div>'

    #generate html for all tags currently plotted
    for stored_tags in current_plots:
        df = pd.read_sql(f"SELECT Time, {stored_tags} FROM process_data", con)
        fig = px.line(df, x="Time", y=stored_tags, title=f"{stored_tags}", labels={'Time': 'Time', stored_tags: 'Value'})
        stored_plot_html = pio.to_html(fig, config={'responsive': True})
        wrapped_html += f'<div id="plot">{stored_plot_html}</div>'

    return wrapped_html
