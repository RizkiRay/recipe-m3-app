from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from database import get_recipe_by_slug, get_all_recipes, init_db

BASE_DIR = Path(__file__).parent
init_db()

app = FastAPI(title="M3 Recipe CookBook")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    all_recipes = get_all_recipes()
    return templates.TemplateResponse(request=request, name="catalog.html", context={"all_recipes": all_recipes})

@app.get("/catalog", response_class=HTMLResponse)
async def catalog_view(request: Request):
    all_recipes = get_all_recipes()
    return templates.TemplateResponse(request=request, name="catalog.html", context={"all_recipes": all_recipes})

@app.get("/recipe/{slug}", response_class=HTMLResponse)
async def view_recipe(request: Request, slug: str):
    recipe = get_recipe_by_slug(slug)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    all_recipes = get_all_recipes()
    return templates.TemplateResponse(request=request, name="recipe.html", context={"recipe": recipe, "all_recipes": all_recipes})

@app.get("/api/recipes")
async def api_recipes():
    return JSONResponse(content={"recipes": get_all_recipes()})

@app.get("/api/recipes/{slug}")
async def api_recipe(slug: str):
    recipe = get_recipe_by_slug(slug)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return JSONResponse(content={"recipe": recipe})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
