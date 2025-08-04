# services/dashboard-service
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = FastAPI(title="Dashboard Service")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Récupération des données
    price_data = await get_price_analytics()
    product_data = await get_product_analytics()
    
    # Création des graphiques
    price_chart = create_price_chart(price_data)
    volume_chart = create_volume_chart(product_data)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "price_chart": price_chart,
        "volume_chart": volume_chart,
        "stats": calculate_stats(price_data, product_data)
    })

def create_price_chart(data):
    """Création d'un graphique des prix"""
    df = pd.DataFrame(data)
    fig = px.line(df, x='date', y='price', color='product_name',
                  title='Évolution des Prix par Produit')
    return fig.to_html(include_plotlyjs=False)
