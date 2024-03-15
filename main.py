from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from router import api

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(api.router)


@app.get("/family-tree", response_class=HTMLResponse)
def family_tree(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="views/family_tree.html",
    )


@app.get("/semantic-network", response_class=HTMLResponse)
def semantic_network(request: Request):
    return templates.TemplateResponse(request=request, name="views/semantic_network.html")


@app.get("/", response_class=RedirectResponse)
async def root(_request: Request):
    return RedirectResponse("/semantic-network")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
