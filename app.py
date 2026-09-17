from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sqlite3
import database
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

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    conn = sqlite3.connect(database.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT r.id, r.slug, r.title, r.chef, r.media_url, r.youtube_id,
           (SELECT COUNT(*) FROM ingredients WHERE group_id IN (SELECT id FROM ingredient_groups WHERE recipe_id = r.id)) as ing_count,
           (SELECT COUNT(*) FROM instructions WHERE recipe_id = r.id) as step_count
    FROM recipes r
    ORDER BY r.id DESC
    ''')
    recipes = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    total_ingredients = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM instructions")
    total_steps = cursor.fetchone()[0]
    conn.close()
    
    return templates.TemplateResponse(request=request, name="admin_dashboard.html", context={
        "recipes": recipes,
        "total_ingredients": total_ingredients,
        "total_steps": total_steps
    })

@app.get("/admin/edit/{recipe_id}", response_class=HTMLResponse)
async def admin_edit_recipe(request: Request, recipe_id: int):
    conn = sqlite3.connect(database.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    if not recipe:
        conn.close()
        raise HTTPException(status_code=404, detail="Recipe not found")
        
    recipe_dict = dict(recipe)
    cursor.execute("SELECT * FROM ingredient_groups WHERE recipe_id = ? ORDER BY sort_order", (recipe_id,))
    groups = cursor.fetchall()
    recipe_dict['ingredient_groups'] = []
    for g in groups:
        g_dict = dict(g)
        cursor.execute("SELECT * FROM ingredients WHERE group_id = ? ORDER BY sort_order", (g['id'],))
        g_dict['ingredients_list'] = [dict(i) for i in cursor.fetchall()]
        recipe_dict['ingredient_groups'].append(g_dict)
        
    cursor.execute("SELECT * FROM instructions WHERE recipe_id = ? ORDER BY step_number", (recipe_id,))
    recipe_dict['instructions'] = [dict(s) for s in cursor.fetchall()]
    conn.close()
    
    return templates.TemplateResponse(request=request, name="admin_edit.html", context={"recipe": recipe_dict})

@app.delete("/api/admin/recipe/{recipe_id}")
async def api_delete_recipe(recipe_id: int):
    conn = sqlite3.connect(database.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM ingredients WHERE group_id IN (SELECT id FROM ingredient_groups WHERE recipe_id = ?)", (recipe_id,))
    cursor.execute("DELETE FROM ingredient_groups WHERE recipe_id = ?", (recipe_id,))
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "deleted", "id": recipe_id})

@app.put("/api/admin/recipe/{recipe_id}")
async def api_update_recipe(recipe_id: int, request: Request):
    data = await request.json()
    conn = sqlite3.connect(database.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE recipes 
    SET title = ?, chef = ?, prep_time = ?, cook_time = ?, servings = ?, media_url = ?, description = ?
    WHERE id = ?
    ''', (
        data.get('title'), data.get('chef'), data.get('prep_time'), data.get('cook_time'),
        data.get('servings'), data.get('media_url'), data.get('description'), recipe_id
    ))
    
    # Refresh ingredients
    cursor.execute("SELECT id FROM ingredient_groups WHERE recipe_id = ?", (recipe_id,))
    g_row = cursor.fetchone()
    if g_row:
        g_id = g_row[0]
        cursor.execute("DELETE FROM ingredients WHERE group_id = ?", (g_id,))
    else:
        cursor.execute("INSERT INTO ingredient_groups (recipe_id, name, sort_order) VALUES (?, 'Daftar Bahan & Bumbu', 0)", (recipe_id,))
        g_id = cursor.lastrowid
        
    for idx, ing in enumerate(data.get('ingredients', [])):
        cursor.execute('''
        INSERT INTO ingredients (group_id, item, amount, unit, notes, sort_order)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (g_id, ing.get('item'), ing.get('amount'), ing.get('unit'), ing.get('notes'), idx))
        
    # Refresh steps
    cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (recipe_id,))
    for idx, st in enumerate(data.get('steps', [])):
        cursor.execute('''
        INSERT INTO instructions (recipe_id, step_number, title, detail, timer_seconds)
        VALUES (?, ?, ?, ?, ?)
        ''', (recipe_id, idx + 1, f"Langkah {idx + 1}", st.get('detail'), st.get('timer_seconds', 0)))
        
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "updated", "id": recipe_id})

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
