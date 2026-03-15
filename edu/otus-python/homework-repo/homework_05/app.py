from pathlib import Path
from typing import List

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

app = FastAPI()

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# HTML routers
html_router = APIRouter()


@html_router.get("/", response_class=HTMLResponse, name="index")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@html_router.get("/about/", response_class=HTMLResponse, name="about")
def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {})


app.include_router(html_router)


# API routers
api_router = APIRouter(prefix="/api")


class Book(BaseModel):
    id: int
    title: str
    author: str


class BookCreate(BaseModel):
    title: str
    author: str


def _get_next_id() -> int:
    return max((book.id for book in books), default=0) + 1


books: List[Book] = []


@api_router.get("/books/", response_model=List[Book])
def list_books():
    return books


@api_router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@api_router.post("/books/", response_model=Book, status_code=201)
def create_book(book: BookCreate):
    new_book = Book(id=_get_next_id(), **book.model_dump())
    books.append(new_book)
    return new_book


app.include_router(api_router)

