from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Mount static directory (even if empty)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# HTML pages router
pages_router = APIRouter()


@pages_router.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@pages_router.get("/about/", response_class=HTMLResponse, name="about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


app.include_router(pages_router)

# API routers
api_router = APIRouter(prefix="/api")


class BookBase(BaseModel):
    title: str
    author: str


class Book(BookBase):
    id: int


books: List[Book] = []
current_id = 1


books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/", response_model=List[Book])
async def list_books():
    return books


@books_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@books_router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookBase):
    global current_id
    new_book = Book(id=current_id, **book.dict())
    current_id += 1
    books.append(new_book)
    return new_book


api_router.include_router(books_router)
app.include_router(api_router)
