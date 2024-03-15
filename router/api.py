from fastapi import Request
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from generator import SemanticNetworkGenerator, FamilyTreeGenerator

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/api",
)


@router.get("/semantic_network", response_class=HTMLResponse)
def api_semantic_network(request: Request, semantic_text: str):
    generator = SemanticNetworkGenerator(semantic_text)
    generator.generate()

    return templates.TemplateResponse(
        request=request,
        name="fragments/semantic_network.html",
        context={
            "mermaid_code": generator.mermaid_code,
            "objects_table": generator.objects_table,
            "semantic_network": generator.semantic_network,
            "code": generator.generated_code,
        },
    )


@router.get("/family_tree", response_class=HTMLResponse)
def api_family_tree(request: Request, semantic_text: str):
    generator = FamilyTreeGenerator(semantic_text)
    generator.generate()

    return templates.TemplateResponse(
        request=request,
        name="fragments/family_tree.html",
        context={
            "mermaid_code": generator.mermaid_code,
            "objects_table": generator.objects_table,
            "semantic_network": generator.semantic_network,
            "code": generator.generated_code,
        },
    )
