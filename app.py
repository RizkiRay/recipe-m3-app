from fastapi import FastAPI, Request, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sqlite3
import hashlib
import database
from database import get_recipe_by_slug, get_all_recipes, init_db

BASE_DIR = Path(__file__).parent
init_db()

app = FastAPI(title="M3 Recipe CookBook")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Database User & Roles Setup
def init_auth_db():
    conn = sqlite3.connect(database.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'editor', -- 'admin' or 'editor'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Hash helper
    def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
    
    # Seed default Admin & Editor if not exist
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES ('admin', ?, 'admin')", (hash_pw('admin123'),))
    cursor.execute("SELECT id FROM users WHERE username = 'editor'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES ('editor', ?, 'editor')", (hash_pw('editor123'),))
        
    conn.commit()
    conn.close()

init_auth_db()

# Auth Helpers
def get_current_user(request: Request):
    token = request.cookies.get("admin_session")
    if not token:
        return None
    try:
        username, role = token.split(":")
        conn = sqlite3.connect(database.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE username = ? AND role = ?", (username, role))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {"id": user[0], "username": user[1], "role": user[2]}
    except Exception:
        pass
    return None

# Public Routes
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

# Auth Routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse(request=request, name="admin_login.html", context={})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="admin_session")
    return response

@app.post("/api/auth/login")
async def api_login(request: Request, response: Response):
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(database.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE username = ? AND password_hash = ?", (username, pw_hash))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Username atau password salah."})
        
    session_token = f"{user[1]}:{user[2]}"
    res = JSONResponse(content={"status": "ok", "role": user[2]})
    res.set_cookie(key="admin_session", value=session_token, httponly=True, max_age=86400 * 7)
    return res

# Protected Admin Dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
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
        "total_steps": total_steps,
        "user": user
    })

@app.get("/admin/edit/{recipe_id}", response_class=HTMLResponse)
async def admin_edit_recipe(request: Request, recipe_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
        
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
    
    return templates.TemplateResponse(request=request, name="admin_edit.html", context={
        "recipe": recipe_dict,
        "user": user
    })

# Protected API Endpoints (Role-Based Access Control)
@app.delete("/api/admin/recipe/{recipe_id}")
async def api_delete_recipe(recipe_id: int, request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Hanya role Admin yang diizinkan menghapus resep.")
        
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
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Both 'admin' and 'editor' can update/edit recipes
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
