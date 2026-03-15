from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import Base, engine, get_session
from .models import Note
from .schemas import NoteCreate, NoteOut

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/api/notes", response_model=list[NoteOut])
async def api_read_notes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note))
    return result.scalars().all()


@app.post("/api/notes", response_model=NoteOut)
async def api_create_note(note: NoteCreate, session: AsyncSession = Depends(get_session)):
    note_obj = Note(title=note.title, content=note.content)
    session.add(note_obj)
    await session.commit()
    await session.refresh(note_obj)
    return note_obj


@app.get("/", response_class=HTMLResponse)
async def read_notes_html(request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note))
    notes = result.scalars().all()
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})


@app.post("/", response_class=HTMLResponse)
async def create_note_html(
    request: Request,
    title: str = Form(...),
    content: str = Form(None),
    session: AsyncSession = Depends(get_session),
):
    note_obj = Note(title=title, content=content)
    session.add(note_obj)
    await session.commit()
    return RedirectResponse(url="/", status_code=303)
