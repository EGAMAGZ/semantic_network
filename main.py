from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/family-tree", response_class=HTMLResponse)
def family_tree(request: Request):
    return templates.TemplateResponse(request=request, name="family_tree.html")


@app.get("/semantic-network", response_class=HTMLResponse)
def semantic_network(request: Request):
    return templates.TemplateResponse(request=request, name="semantic_network.html")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
