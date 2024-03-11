from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class SemanticText(BaseModel):
    semantic_text: str


@app.post("/api/semantic_network", response_class=HTMLResponse)
def api_semantic_network(request: Request, semantic_text: SemanticText):
    print(semantic_text)
    return templates.TemplateResponse(
        request=request, name="fragments/semantic_network.html"
    )


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
