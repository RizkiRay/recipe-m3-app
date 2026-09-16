# Recipe CookBook M3 (One-Handed Cooking UI)

A Material Design 3 (M3) focused mobile-first recipe web application designed specifically for cooking with one hand.

## Features
- **Material Design 3 Token System**: Full M3 tonal palettes, semantic color roles, shape tokens, and elevation.
- **One-Handed Navigation**: Large touch targets located in the thumb zone at the bottom of the viewport + swipe gestures.
- **SQLite Database Backend**: Structured relational database for recipes, grouped ingredients, and step-by-step instructions.
- **Embedded Source Video**: YouTube video player attached to the recipe header.
- **Interactive Checklist**: Strike-through checklist for kitchen preparation.
- **Cooking Mode with Built-in Timers**: Large typography step cards with countdown timers for critical steps (steaming, frying, food processing).

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite3
- **Frontend**: Jinja2 HTML Templates, Vanilla JavaScript, Pure Material 3 CSS tokens

## Quick Start

```bash
# 1. Install dependencies
pip install fastapi uvicorn jinja2

# 2. Initialize Database & Run
python database.py
uvicorn app:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in browser.
