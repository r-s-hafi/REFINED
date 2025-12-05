from sqlite3 import Connection
import pandas as pd
from fastapi.responses import HTMLResponse
import plotly.express as px
import plotly.io as pio

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


def plot_tag_data(con: Connection, tag_id: str) -> HTMLResponse:
    tag_id = tag_id.upper()
    df = pd.read_sql(f"SELECT Time, {tag_id} FROM process_data", con)
    fig = px.line(df, x="Time", y=tag_id, title=f"{tag_id}", labels={'Time': 'Time', tag_id: 'Value'})
    fig.show()
    plot_html = pio.to_html(fig)     
    return plot_html      

