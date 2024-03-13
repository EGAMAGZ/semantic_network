from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from generator import SemanticNetworkGenerator


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/api/semantic_network", response_class=HTMLResponse)
def api_semantic_network(request: Request, semantic_text: str):
    generator = SemanticNetworkGenerator(semantic_text)
    generator.generate()

    return templates.TemplateResponse(
        request=request,
        name="fragments/semantic_network.html",
        context={
            "mermaid_code": generator.generated_code,
            "objects_table": generator.objects_table,
            "semantic_network": generator.semantic_network,
        },
    )


@app.get("/family-tree", response_class=HTMLResponse)
def family_tree(request: Request):
    return templates.TemplateResponse(request=request, name="family_tree.html")


@app.get("/semantic-network", response_class=HTMLResponse)
def semantic_network(request: Request):
    return templates.TemplateResponse(request=request, name="semantic_network.html")


@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse("/semantic-network")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
