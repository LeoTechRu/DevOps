from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from .database import SessionLocal, init_db

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    items = result.scalars().all()
    return templates.TemplateResponse("items.html", {"request": request, "items": items})


@app.get("/add", response_class=HTMLResponse)
async def add_item_form(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@app.post("/add", response_class=HTMLResponse)
async def create_item(
    name: str = Form(...),
    description: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
):
    item = models.Item(name=name, description=description)
    db.add(item)
    await db.commit()
    return RedirectResponse(url="/", status_code=302)
